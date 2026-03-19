from __future__ import annotations

from tkinter import ttk

from ..powershell import CommandStep


def build(app) -> None:
    app.set_window_size(440, 600)
    app.render_header()

    feature_buttons = [
        ("Install DHCP Feature", "Installing DHCP feature...", [CommandStep("Install DHCP", "Install-WindowsFeature -Name DHCP -IncludeManagementTools")]),
        ("Uninstall DHCP Feature", "Removing DHCP feature...", [CommandStep("Uninstall DHCP", "Uninstall-WindowsFeature -Name DHCP -IncludeManagementTools")]),
        ("Setup DHCP", lambda: app.navigate("DHCP")),
        ("Remove DHCP Scope", lambda: app.navigate("RemoveDHCP")),
        ("Install DNS Feature", "Installing DNS feature...", [CommandStep("Install DNS", "Install-WindowsFeature -Name DNS -IncludeManagementTools")]),
        ("Uninstall DNS Feature", "Removing DNS feature...", [CommandStep("Uninstall DNS", "Uninstall-WindowsFeature -Name DNS -IncludeManagementTools")]),
        ("Setup DNS", lambda: app.navigate("DNS")),
        ("Install iSCSI target", "Installing iSCSI target...", [CommandStep("Install iSCSI target", "Install-WindowsFeature -Name FS-iSCSITarget-Server")]),
        ("Uninstall iSCSI target", "Removing iSCSI target...", [CommandStep("Uninstall iSCSI target", "Uninstall-WindowsFeature -Name FS-iSCSITarget-Server")]),
        ("Setup iSCSI Disk Share", lambda: app.navigate("iSCSI")),
    ]

    for row, (label, action, *maybe_steps) in enumerate(feature_buttons, start=1):
        if callable(action):
            command = app.guard(action)
        else:
            steps = maybe_steps[0]
            command = app.guard(lambda msg=action, cmd_steps=steps: app.run_steps(msg, cmd_steps))

        ttk.Button(
            app.content,
            text=label,
            command=command,
            style="Custom.TButton",
        ).grid(row=row, column=0, columnspan=3, sticky="ew", pady=4)

    ttk.Button(
        app.content,
        text="Restart This Computer",
        command=app.guard(
            lambda: app.run_steps(
                "Restarting computer...",
                [CommandStep("Restart computer", "shutdown -r -t 0")],
            )
        ),
        style="Red.TButton",
    ).grid(row=len(feature_buttons) + 1, column=0, columnspan=3, sticky="ew", pady=(10, 4))
