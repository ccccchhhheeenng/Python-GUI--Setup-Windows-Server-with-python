from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..powershell import CommandStep, ps_quote
from ..validators import compute_scope_id, require_text, validate_ipv4


def build_setup(app) -> None:
    app.set_window_size(460, 350)
    app.render_header()

    start_range = app.add_labeled_entry("Start Range", row=1)
    end_range = app.add_labeled_entry("End Range", row=2)
    subnet_mask = app.add_labeled_entry("Subnet Mask", row=3)
    scope_name = app.add_labeled_entry("Scope Name", row=4)
    dns_address = app.add_labeled_entry("DNS Address", row=5)
    router = app.add_labeled_entry("Router IP", row=6)

    def submit() -> None:
        start = validate_ipv4(start_range.get(), "Start range")
        end = validate_ipv4(end_range.get(), "End range")
        mask = validate_ipv4(subnet_mask.get(), "Subnet mask")
        name = require_text(scope_name.get(), "Scope name")
        dns = validate_ipv4(dns_address.get(), "DNS address")
        router_ip = validate_ipv4(router.get(), "Router IP")
        scope_id = compute_scope_id(start)
        app.run_steps(
            "Creating DHCP scope...",
            [
                CommandStep(
                    "Add DHCP scope",
                    f"Add-DhcpServerV4Scope -Name {ps_quote(name)} -StartRange {ps_quote(start)} -EndRange {ps_quote(end)} -SubnetMask {ps_quote(mask)}",
                ),
                CommandStep(
                    "Set DHCP DNS",
                    f"Set-DhcpServerv4OptionValue -ScopeId {ps_quote(scope_id)} -OptionId 6 -Value {ps_quote(dns)}",
                ),
                CommandStep(
                    "Set DHCP router",
                    f"Set-DhcpServerv4OptionValue -ScopeId {ps_quote(scope_id)} -Router {ps_quote(router_ip)}",
                ),
            ],
        )

    app.add_form_actions(row=7, submit_text="Finish", submit=submit)


def build_remove_scope(app) -> None:
    app.set_window_size(460, 220)
    app.render_header()

    scope_id = app.add_labeled_entry("Scope ID", row=1)

    def submit() -> None:
        value = validate_ipv4(scope_id.get(), "Scope ID")
        app.run_steps(
            "Removing DHCP scope...",
            [CommandStep("Remove DHCP scope", f"Remove-DhcpServerv4Scope -ScopeId {ps_quote(value)} -Force")],
        )

    app.add_form_actions(row=2, submit_text="Finish", submit=submit)
