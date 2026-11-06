"""
modules/reports.py
------------------
Business analytics, metric calculations, and report export utilities for
Veda Technology Business & Service Management System.

Features:
- Entity totals and active vs inactive status counts.
- Inquiry lifecycle distribution (by status and priority).
- Demand ranking (most requested services and programs).
- Capacity & estimated revenue analytics from training programs.
- Exporting reports to formatted Plain Text (.txt) or Comma-Separated Values (.csv).
"""

import os
import csv
from datetime import datetime
from typing import List, Dict, Tuple
from collections import Counter

from models.service import Service
from models.program import Program
from models.customer import Customer
from models.inquiry import Inquiry
from modules.validators import prompt_choice, prompt_string


def generate_executive_summary(
    services: List[Service],
    programs: List[Program],
    customers: List[Customer],
    inquiries: List[Inquiry],
) -> str:
    """Generate a clean executive summary string."""
    active_services = sum(1 for s in services if s.status.lower() == "active")
    inactive_services = len(services) - active_services

    active_programs = sum(1 for p in programs if p.status.lower() == "active")
    upcoming_programs = sum(1 for p in programs if p.status.lower() == "upcoming")
    closed_programs = len(programs) - (active_programs + upcoming_programs)

    open_inquiries = sum(1 for inq in inquiries if inq.status.lower() == "open")
    in_progress_inquiries = sum(1 for inq in inquiries if inq.status.lower() == "in progress")
    resolved_inquiries = sum(1 for inq in inquiries if inq.status.lower() == "resolved")
    closed_inquiries = sum(1 for inq in inquiries if inq.status.lower() == "closed")

    lines = [
        "=" * 65,
        " VEDA TECHNOLOGY - EXECUTIVE BUSINESS SUMMARY".center(65),
        f" Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(65),
        "=" * 65,
        f"  Total Digital Services Catalog : {len(services):>4}",
        f"    - Active Offerings           : {active_services:>4}",
        f"    - Inactive / Deprecated      : {inactive_services:>4}",
        "-" * 65,
        f"  Total Training & Tech Programs : {len(programs):>4}",
        f"    - Active Cohorts             : {active_programs:>4}",
        f"    - Upcoming Cohorts           : {upcoming_programs:>4}",
        f"    - Closed / Completed Cohorts : {closed_programs:>4}",
        "-" * 65,
        f"  Total Registered Customers     : {len(customers):>4}",
        "-" * 65,
        f"  Total Inquiries Logged         : {len(inquiries):>4}",
        f"    - Open (Pending Review)      : {open_inquiries:>4}",
        f"    - In Progress                : {in_progress_inquiries:>4}",
        f"    - Resolved                   : {resolved_inquiries:>4}",
        f"    - Closed                     : {closed_inquiries:>4}",
        "=" * 65,
    ]
    return "\n".join(lines)


def generate_inquiry_status_report(inquiries: List[Inquiry]) -> str:
    """Analyze inquiry distribution by status and priority tier."""
    status_counts = Counter(inq.status for inq in inquiries)
    priority_counts = Counter(inq.priority for inq in inquiries)
    total = len(inquiries) or 1

    lines = [
        "=" * 65,
        " INQUIRY DISTRIBUTION BY STATUS & PRIORITY".center(65),
        "=" * 65,
        " [Status Breakdown]",
    ]
    for status in ["Open", "In Progress", "Resolved", "Closed"]:
        cnt = status_counts.get(status, 0)
        pct = (cnt / total) * 100
        lines.append(f"  {status:<16} : {cnt:>3} ({pct:>5.1f}%)")

    lines.append("-" * 65)
    lines.append(" [Priority Breakdown]")
    for prio in ["Urgent", "High", "Medium", "Low"]:
        cnt = priority_counts.get(prio, 0)
        pct = (cnt / total) * 100
        lines.append(f"  {prio:<16} : {cnt:>3} ({pct:>5.1f}%)")
    lines.append("=" * 65)

    return "\n".join(lines)


def generate_demand_ranking_report(inquiries: List[Inquiry]) -> str:
    """Identify the most requested services and programs based on logged inquiries."""
    service_requests = Counter(
        inq.target_name for inq in inquiries if inq.target_type.lower() == "service"
    )
    program_requests = Counter(
        inq.target_name for inq in inquiries if inq.target_type.lower() == "program"
    )

    lines = [
        "=" * 65,
        " DEMAND ANALYSIS: MOST REQUESTED OFFERINGS".center(65),
        "=" * 65,
        " [Top Requested Digital Services]",
    ]
    if service_requests:
        for rank, (name, count) in enumerate(service_requests.most_common(), 1):
            lines.append(f"  {rank}. {name:<42} : {count} inquiries")
    else:
        lines.append("  No service inquiries recorded.")

    lines.append("-" * 65)
    lines.append(" [Top Requested Training & Internship Programs]")
    if program_requests:
        for rank, (name, count) in enumerate(program_requests.most_common(), 1):
            lines.append(f"  {rank}. {name:<42} : {count} inquiries")
    else:
        lines.append("  No program inquiries recorded.")
    lines.append("=" * 65)

    return "\n".join(lines)


def generate_program_revenue_report(programs: List[Program]) -> str:
    """Calculate capacity, tuition, and projected revenue for programs."""
    total_seats = sum(p.seats for p in programs)
    total_potential_revenue = sum(p.fee * p.seats for p in programs)
    sponsored_programs = [p for p in programs if p.fee == 0.0]
    paid_programs = [p for p in programs if p.fee > 0.0]
    avg_fee = (sum(p.fee for p in paid_programs) / len(paid_programs)) if paid_programs else 0.0

    lines = [
        "=" * 65,
        " PROGRAM CAPACITY & PROJECTED REVENUE REPORT".center(65),
        "=" * 65,
        f"  Total Educational Programs      : {len(programs)}",
        f"  Tuition-Paid Programs           : {len(paid_programs)}",
        f"  Free / Sponsored Internships    : {len(sponsored_programs)}",
        f"  Total Seat Capacity Across All  : {total_seats} seats",
        f"  Average Paid Program Tuition    : ${avg_fee:,.2f} USD",
        f"  Total Potential Program Revenue : ${total_potential_revenue:,.2f} USD",
        "-" * 65,
        " [Cohort Revenue Potential Breakdown]",
    ]
    for p in programs:
        pot = p.fee * p.seats
        fee_str = f"${p.fee:,.2f}" if p.fee > 0 else "Free"
        lines.append(
            f"  - {p.name[:30]:<30} | {p.seats:>2} seats @ {fee_str:>9} = ${pot:>10,.2f}"
        )
    lines.append("=" * 65)

    return "\n".join(lines)


def export_report_to_file(
    content: str,
    default_filename: str = "business_report.txt",
    is_csv: bool = False,
    csv_rows: List[List[str]] = None,
) -> None:
    """Export report content to a TXT or CSV file."""
    filename = prompt_string(
        "Enter export filename",
        default=default_filename,
    )

    # Place in scratch or project root
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_output")
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, filename)

    try:
        if is_csv and csv_rows:
            with open(full_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(csv_rows)
        else:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        print(f"\n  [OK] Report successfully exported to:")
        print(f"       {full_path}")
    except OSError as err:
        print(f"\n  [Error] Failed to write report file: {err}")


def export_full_csv_metrics(
    services: List[Service],
    programs: List[Program],
    customers: List[Customer],
    inquiries: List[Inquiry],
) -> None:
    """Export a multi-sheet structured CSV file containing business metric tables."""
    rows = [
        ["REPORT", "Veda Technology Enterprise Business Metrics"],
        ["GENERATED_AT", datetime.now().isoformat()],
        [],
        ["--- ENTITY TOTALS ---"],
        ["Metric", "Value"],
        ["Total Services", len(services)],
        ["Active Services", sum(1 for s in services if s.status.lower() == "active")],
        ["Total Programs", len(programs)],
        ["Active Programs", sum(1 for p in programs if p.status.lower() == "active")],
        ["Total Customers", len(customers)],
        ["Total Inquiries", len(inquiries)],
        [],
        ["--- PROGRAM REVENUE METRICS ---"],
        ["Program ID", "Program Name", "Type", "Fee ($)", "Seats", "Potential Revenue ($)", "Status"],
    ]
    for p in programs:
        rows.append([p.id, p.name, p.type, p.fee, p.seats, p.fee * p.seats, p.status])

    rows.extend([
        [],
        ["--- INQUIRY SUMMARY ---"],
        ["Inquiry ID", "Customer Name", "Target Type", "Target Name", "Priority", "Status", "Date"],
    ])
    for inq in inquiries:
        rows.append([
            inq.id,
            inq.customer_name,
            inq.target_type,
            inq.target_name,
            inq.priority,
            inq.status,
            inq.created_date,
        ])

    export_report_to_file("", default_filename="veda_business_metrics.csv", is_csv=True, csv_rows=rows)


def reports_menu(
    services: List[Service],
    programs: List[Program],
    customers: List[Customer],
    inquiries: List[Inquiry],
) -> None:
    """Interactive submenu loop for Business Analytics & Reports."""
    while True:
        print("\n" + "=" * 50)
        print(" BUSINESS ANALYTICS & REPORTS".center(50))
        print("=" * 50)
        print("  1. Executive Summary (Entity & Active Counts)")
        print("  2. Inquiry Distribution by Status & Priority")
        print("  3. Most Requested Services & Programs")
        print("  4. Program Capacity & Revenue Estimation")
        print("  5. Full Business Health Report (Combined)")
        print("  6. Export Report to File (Text .txt or CSV .csv)")
        print("  7. Return to Main Menu")
        print("=" * 50)

        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            print()
            print(generate_executive_summary(services, programs, customers, inquiries))

        elif choice == "2":
            print()
            print(generate_inquiry_status_report(inquiries))

        elif choice == "3":
            print()
            print(generate_demand_ranking_report(inquiries))

        elif choice == "4":
            print()
            print(generate_program_revenue_report(programs))

        elif choice == "5":
            full_report = "\n\n".join([
                generate_executive_summary(services, programs, customers, inquiries),
                generate_inquiry_status_report(inquiries),
                generate_demand_ranking_report(inquiries),
                generate_program_revenue_report(programs),
            ])
            print()
            print(full_report)

        elif choice == "6":
            export_fmt = prompt_choice("Select Export Format", ["TXT", "CSV"], default="TXT")
            if export_fmt == "TXT":
                full_report = "\n\n".join([
                    generate_executive_summary(services, programs, customers, inquiries),
                    generate_inquiry_status_report(inquiries),
                    generate_demand_ranking_report(inquiries),
                    generate_program_revenue_report(programs),
                ])
                export_report_to_file(full_report, default_filename="veda_executive_report.txt")
            else:
                export_full_csv_metrics(services, programs, customers, inquiries)

        elif choice == "7":
            break
        else:
            print("  [!] Invalid choice. Please enter a number between 1 and 7.")
