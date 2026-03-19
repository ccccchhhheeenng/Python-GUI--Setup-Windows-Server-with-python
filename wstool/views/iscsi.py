from __future__ import annotations

import os
from tkinter import filedialog, ttk

from ..powershell import CommandStep, ps_quote
from ..validators import require_text


def build(app) -> None:
    route = app.state.route
    if "AddVirtualDisk" in route:
        build_add_disk(app)
        return
    if "ShareVirtualDisk" in route:
        build_share_disk(app)
        return

    app.set_window_size(500, 230)
    app.render_header()
    ttk.Button(app.content, text="Add Virtual Disk", command=app.guard(lambda: app.navigate("AddVirtualDisk")), style="Custom.TButton").grid(row=1, column=0, columnspan=3, sticky="ew", pady=4)
    ttk.Button(app.content, text="Share Virtual Disk by iSCSI", command=app.guard(lambda: app.navigate("ShareVirtualDisk")), style="Custom.TButton").grid(row=2, column=0, columnspan=3, sticky="ew", pady=4)
    app.add_back_button().grid(row=3, column=0, columnspan=3, sticky="ew", pady=(8, 0))


def build_add_disk(app) -> None:
    app.set_window_size(640, 260)
    app.render_header()
    path_entry = app.add_labeled_entry("Virtual Disk Folder", row=1, width=40)
    name_entry = app.add_labeled_entry("Disk Name", row=2, width=40)
    size_entry = app.add_labeled_entry("Disk Size", row=3, width=40)

    def select_folder() -> None:
        path = filedialog.askdirectory()
        if not path:
            return
        path_entry.delete(0, "end")
        path_entry.insert(0, path)

    ttk.Button(app.content, text="Select", command=app.guard(select_folder), style="Green.TButton").grid(row=1, column=2, padx=(8, 0), pady=6, sticky="ew")

    def submit() -> None:
        folder = require_text(path_entry.get(), "Virtual disk folder")
        name = require_text(name_entry.get(), "Disk name")
        size = require_text(size_entry.get(), "Disk size")
        disk_path = os.path.join(folder, name)
        app.run_steps(
            "Creating iSCSI virtual disk...",
            [CommandStep("Create virtual disk", f"New-IscsiVirtualDisk -Path {ps_quote(disk_path)} -Size {ps_quote(size)}")],
        )

    app.add_form_actions(row=4, submit_text="Finish", submit=submit)


def build_share_disk(app) -> None:
    app.set_window_size(680, 320)
    app.render_header()
    target_entry = app.add_labeled_entry("Target Name", row=1, width=42)
    disk_entry = app.add_labeled_entry("Disk Path", row=2, width=42)
    user_entry = app.add_labeled_entry("User Name", row=3, width=42)
    password_entry = app.add_labeled_entry("Password", row=4, width=42, show="*")

    def select_file() -> None:
        path = filedialog.askopenfilename()
        if not path:
            return
        disk_entry.delete(0, "end")
        disk_entry.insert(0, path)

    ttk.Button(app.content, text="Select", command=app.guard(select_file), style="Green.TButton").grid(row=2, column=2, padx=(8, 0), pady=6, sticky="ew")

    def submit() -> None:
        target = require_text(target_entry.get(), "Target name")
        disk_path = require_text(disk_entry.get(), "Disk path")
        username = require_text(user_entry.get(), "User name")
        password = require_text(password_entry.get(), "Password")
        credential_script = (
            f"$User={ps_quote(username)};"
            f"$PWord=ConvertTo-SecureString -String {ps_quote(password)} -AsPlainText -Force;"
            "$Credential=New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User, $PWord;"
            f"Set-IscsiServerTarget -TargetName {ps_quote(target)} -EnableChap $True -Chap $Credential"
        )
        app.run_steps(
            "Sharing virtual disk over iSCSI...",
            [
                CommandStep("Create iSCSI target", f"New-IscsiServerTarget -TargetName {ps_quote(target)} -InitiatorId {ps_quote('Iqn:*')}"),
                CommandStep("Map virtual disk", f"Add-IscsiVirtualDiskTargetMapping -TargetName {ps_quote(target)} -DevicePath {ps_quote(disk_path)}"),
                CommandStep("Enable CHAP", credential_script),
            ],
        )

    app.add_form_actions(row=5, submit_text="Finish", submit=submit)
