from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..powershell import CommandStep, ps_quote
from ..validators import require_text, validate_ipv4, validate_ipv6, validate_network_id, validate_zone_name

RECORD_TYPES = ("A", "AAAA", "CNAME")


def build(app) -> None:
    route = app.state.route
    if "ForwardLookupZone" in route:
        build_forward(app)
        return
    if "ReverseLookupZone" in route:
        build_reverse(app)
        return
    if "SetForwarder" in route:
        build_forwarder(app)
        return

    app.set_window_size(440, 260)
    app.render_header()
    for row, (label, destination) in enumerate((
        ("Forward Lookup Zone Settings", "ForwardLookupZone"),
        ("Reverse Lookup Zone Settings", "ReverseLookupZone"),
        ("Set Forwarder", "SetForwarder"),
    ), start=1):
        ttk.Button(app.content, text=label, command=app.guard(lambda dest=destination: app.navigate(dest)), style="Custom.TButton").grid(row=row, column=0, columnspan=3, sticky="ew", pady=4)
    app.add_back_button().grid(row=4, column=0, columnspan=3, sticky="ew", pady=(8, 0))


def build_forward(app) -> None:
    route = app.state.route
    if "AddDnsPrimaryZone" in route:
        build_add_primary_zone(app)
        return
    if "AddDnsPrimaryRecord" in route:
        build_add_primary_record(app)
        return
    if "RemoveDnsPrimaryZone" in route:
        build_remove_primary_zone(app)
        return
    if "RemoveDnsPrimaryRecord" in route:
        build_remove_primary_record(app)
        return

    app.set_window_size(460, 280)
    app.render_header()
    for row, (label, destination) in enumerate((
        ("Add Primary Zone", "AddDnsPrimaryZone"),
        ("Add DNS Record", "AddDnsPrimaryRecord"),
        ("Remove DNS Zone", "RemoveDnsPrimaryZone"),
        ("Remove DNS Record", "RemoveDnsPrimaryRecord"),
    ), start=1):
        ttk.Button(app.content, text=label, command=app.guard(lambda dest=destination: app.navigate(dest)), style="Custom.TButton").grid(row=row, column=0, columnspan=3, sticky="ew", pady=4)
    app.add_back_button().grid(row=5, column=0, columnspan=3, sticky="ew", pady=(8, 0))


def build_add_primary_zone(app) -> None:
    app.set_window_size(460, 220)
    app.render_header()
    zone_name = app.add_labeled_entry("Zone Name", row=1)

    def submit() -> None:
        name = validate_zone_name(zone_name.get())
        zone_file = f"{name}.dns"
        app.run_steps(
            "Adding primary DNS zone...",
            [CommandStep("Add primary zone", f"Add-DnsServerPrimaryZone -Name {ps_quote(name)} -ZoneFile {ps_quote(zone_file)}")],
        )

    app.add_form_actions(row=2, submit_text="Finish", submit=submit)


def build_add_primary_record(app) -> None:
    app.set_window_size(500, 320)
    app.render_header()
    zone_name = app.add_labeled_entry("Zone Name", row=1)
    record_type = app.add_combobox("Record Type", RECORD_TYPES, row=2)
    record_type.set("A")
    record_name = app.add_labeled_entry("Record Name", row=3)
    value_entry = app.add_labeled_entry("Value", row=4)
    value_label = app.dynamic_labels[-1]

    def sync_value_label(_event=None) -> None:
        mapping = {
            "A": "IPv4 Address",
            "AAAA": "IPv6 Address",
            "CNAME": "Host Name Alias",
        }
        value_label.config(text=mapping[record_type.get()])

    record_type.bind("<<ComboboxSelected>>", sync_value_label)
    sync_value_label()

    def submit() -> None:
        zone = validate_zone_name(zone_name.get())
        name = require_text(record_name.get(), "Record name")
        selected = record_type.get()
        value = value_entry.get()
        if selected == "A":
            command = f"Add-DnsServerResourceRecordA -Name {ps_quote(name)} -ZoneName {ps_quote(zone)} -IPv4Address {ps_quote(validate_ipv4(value, 'IPv4 address'))}"
        elif selected == "AAAA":
            command = f"Add-DnsServerResourceRecordAAAA -Name {ps_quote(name)} -ZoneName {ps_quote(zone)} -IPv6Address {ps_quote(validate_ipv6(value, 'IPv6 address'))}"
        else:
            alias = require_text(value, "Host name alias")
            command = f"Add-DnsServerResourceRecordCName -Name {ps_quote(name)} -ZoneName {ps_quote(zone)} -HostNameAlias {ps_quote(alias)}"
        app.run_steps("Adding DNS record...", [CommandStep(f"Add {selected} record", command)])

    app.add_form_actions(row=5, submit_text="Finish", submit=submit)


def build_remove_primary_zone(app) -> None:
    app.set_window_size(460, 220)
    app.render_header()
    zone_name = app.add_labeled_entry("Zone Name", row=1)

    def submit() -> None:
        zone = validate_zone_name(zone_name.get())
        app.run_steps(
            "Removing DNS zone...",
            [CommandStep("Remove DNS zone", f"Remove-DnsServerZone -Name {ps_quote(zone)} -Force")],
        )

    app.add_form_actions(row=2, submit_text="Finish", submit=submit)


def build_remove_primary_record(app) -> None:
    app.set_window_size(500, 280)
    app.render_header()
    zone_name = app.add_labeled_entry("Zone Name", row=1)
    record_name = app.add_labeled_entry("Record Name", row=2)
    record_type = app.add_combobox("Record Type", RECORD_TYPES, row=3)
    record_type.set("A")

    def submit() -> None:
        zone = validate_zone_name(zone_name.get())
        name = require_text(record_name.get(), "Record name")
        rr_type = require_text(record_type.get(), "Record type")
        app.run_steps(
            "Removing DNS record...",
            [CommandStep("Remove DNS record", f"Remove-DnsServerResourceRecord -ZoneName {ps_quote(zone)} -Name {ps_quote(name)} -RRType {ps_quote(rr_type)} -Force")],
        )

    app.add_form_actions(row=4, submit_text="Finish", submit=submit)


def build_reverse(app) -> None:
    route = app.state.route
    if "AddDnsReverseZone" in route:
        build_add_reverse_zone(app)
        return
    if "RemoveDnsReverseZone" in route:
        build_remove_reverse_zone(app)
        return
    if "AddDnsPtrRecord" in route:
        build_add_ptr_record(app)
        return
    if "RemoveDnsPtrRecord" in route:
        build_remove_ptr_record(app)
        return

    app.set_window_size(460, 280)
    app.render_header()
    for row, (label, destination) in enumerate((
        ("Add Zone", "AddDnsReverseZone"),
        ("Remove Zone", "RemoveDnsReverseZone"),
        ("Add PTR Record", "AddDnsPtrRecord"),
        ("Remove PTR Record", "RemoveDnsPtrRecord"),
    ), start=1):
        ttk.Button(app.content, text=label, command=app.guard(lambda dest=destination: app.navigate(dest)), style="Custom.TButton").grid(row=row, column=0, columnspan=3, sticky="ew", pady=4)
    app.add_back_button().grid(row=5, column=0, columnspan=3, sticky="ew", pady=(8, 0))


def reverse_zone_name(network_id: str) -> str:
    octets = network_id.split(".")
    return f"{octets[2]}.{octets[1]}.{octets[0]}.in-addr.arpa"


def build_add_reverse_zone(app) -> None:
    app.set_window_size(460, 220)
    app.render_header()
    network_id = app.add_labeled_entry("Network ID", row=1)

    def submit() -> None:
        network = validate_network_id(network_id.get())
        zone_name = reverse_zone_name(network)
        zone_file = f"{zone_name}.dns"
        app.run_steps(
            "Adding reverse DNS zone...",
            [CommandStep("Add reverse zone", f"Add-DnsServerPrimaryZone -NetworkID {ps_quote(network + '/24')} -ZoneFile {ps_quote(zone_file)}")],
        )

    app.add_form_actions(row=2, submit_text="Finish", submit=submit)


def build_remove_reverse_zone(app) -> None:
    app.set_window_size(460, 220)
    app.render_header()
    network_id = app.add_labeled_entry("Network ID", row=1)

    def submit() -> None:
        network = validate_network_id(network_id.get())
        zone_name = reverse_zone_name(network)
        app.run_steps(
            "Removing reverse DNS zone...",
            [CommandStep("Remove reverse zone", f"Remove-DnsServerZone -Name {ps_quote(zone_name)} -Force")],
        )

    app.add_form_actions(row=2, submit_text="Finish", submit=submit)


def build_add_ptr_record(app) -> None:
    app.set_window_size(520, 280)
    app.render_header()
    record_name = app.add_labeled_entry("Record Name", row=1)
    zone_network = app.add_labeled_entry("Zone Network ID", row=2)
    ptr_domain = app.add_labeled_entry("PTR Domain Name", row=3)

    def submit() -> None:
        name = require_text(record_name.get(), "Record name")
        zone_name = reverse_zone_name(validate_network_id(zone_network.get()))
        ptr = require_text(ptr_domain.get(), "PTR domain name")
        app.run_steps(
            "Adding PTR record...",
            [CommandStep("Add PTR record", f"Add-DnsServerResourceRecordPtr -Name {ps_quote(name)} -ZoneName {ps_quote(zone_name)} -PtrDomainName {ps_quote(ptr)}")],
        )

    app.add_form_actions(row=4, submit_text="Finish", submit=submit)


def build_remove_ptr_record(app) -> None:
    app.set_window_size(520, 250)
    app.render_header()
    record_name = app.add_labeled_entry("Record Name", row=1)
    zone_network = app.add_labeled_entry("Zone Network ID", row=2)

    def submit() -> None:
        name = require_text(record_name.get(), "Record name")
        zone_name = reverse_zone_name(validate_network_id(zone_network.get()))
        app.run_steps(
            "Removing PTR record...",
            [CommandStep("Remove PTR record", f"Remove-DnsServerResourceRecord -ZoneName {ps_quote(zone_name)} -RRType PTR -Name {ps_quote(name)} -Force")],
        )

    app.add_form_actions(row=3, submit_text="Finish", submit=submit)


def build_forwarder(app) -> None:
    app.set_window_size(460, 220)
    app.render_header()
    address = app.add_labeled_entry("IP Address", row=1)

    def submit() -> None:
        value = validate_ipv4(address.get(), "IP address")
        app.run_steps(
            "Setting DNS forwarder...",
            [CommandStep("Set DNS forwarder", f"Set-DnsServerForwarder -IPAddress {ps_quote(value)}")],
        )

    app.add_form_actions(row=2, submit_text="Finish", submit=submit)
