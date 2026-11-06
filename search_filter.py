"""
modules/search_filter.py
------------------------
Search and multi-criteria filtering engine for Veda Technology records.

Capabilities:
- Universal keyword search across Services and Programs.
- Filter Services by Category, Status, or Price Range.
- Filter Programs by Track Type, Status, or Fee Range.
- Filter Inquiries by Status, Priority Tier, or Customer.
"""

from typing import List
from models.service import Service
from models.program import Program
from models.inquiry import Inquiry
from modules.service_manager import display_services_table
from modules.program_manager import display_programs_table
from modules.inquiry_manager import display_inquiries_table
from modules.validators import (
    prompt_string,
    prompt_number,
    prompt_choice,
)


def search_offerings_by_keyword(
    services: List[Service],
    programs: List[Program],
) -> None:
    """Search services and programs matching a keyword in title, category, or description."""
    keyword = prompt_string("\nEnter keyword to search across services and programs").lower()

    matched_services = [
        s for s in services
        if keyword in s.name.lower() or keyword in s.category.lower() or keyword in s.description.lower()
    ]
    matched_programs = [
        p for p in programs
        if keyword in p.name.lower() or keyword in p.type.lower() or keyword in p.duration.lower()
    ]

    print(f"\nSearch Results for '{keyword}':")
    print(f"-> Services Found: {len(matched_services)}")
    if matched_services:
        display_services_table(matched_services)

    print(f"\n-> Programs Found: {len(matched_programs)}")
    if matched_programs:
        display_programs_table(matched_programs)


def filter_services(services: List[Service]) -> None:
    """Interactive filtering of services by category, status, or price range."""
    print("\n--- FILTER SERVICES ---")
    print("  1. Filter by Category")
    print("  2. Filter by Status (Active / Inactive)")
    print("  3. Filter by Price Range ($ Min - $ Max)")
    print("  4. Return to Search Menu")

    choice = prompt_string("Choose filter criteria (1-4)")

    if choice == "1":
        cat = prompt_string("Enter Category to filter (e.g., Web Development, Cloud Consulting)")
        results = [s for s in services if cat.lower() in s.category.lower()]
        print(f"\nFiltered Services (Category contains '{cat}'):")
        display_services_table(results)

    elif choice == "2":
        status = prompt_choice("Select Status", Service.VALID_STATUSES, default="Active")
        results = [s for s in services if s.status.lower() == status.lower()]
        print(f"\nFiltered Services (Status = '{status}'):")
        display_services_table(results)

    elif choice == "3":
        min_p = prompt_number("Minimum Price ($)", is_float=True, allow_zero=True, default=0.0)
        max_p = prompt_number("Maximum Price ($)", is_float=True, allow_zero=True, default=999999.0)
        results = [s for s in services if min_p <= s.price <= max_p]
        print(f"\nFiltered Services (${min_p:,.2f} to ${max_p:,.2f}):")
        display_services_table(results)


def filter_programs(programs: List[Program]) -> None:
    """Interactive filtering of programs by type, status, or fee range."""
    print("\n--- FILTER PROGRAMS ---")
    print("  1. Filter by Program Type (Training / Internship / Technology)")
    print("  2. Filter by Status (Active / Upcoming / Closed)")
    print("  3. Filter by Fee Range ($ Min - $ Max)")
    print("  4. Return to Search Menu")

    choice = prompt_string("Choose filter criteria (1-4)")

    if choice == "1":
        ptype = prompt_choice("Select Program Type", Program.VALID_TYPES, default="Training")
        results = [p for p in programs if p.type.lower() == ptype.lower()]
        print(f"\nFiltered Programs (Type = '{ptype}'):")
        display_programs_table(results)

    elif choice == "2":
        status = prompt_choice("Select Status", Program.VALID_STATUSES, default="Active")
        results = [p for p in programs if p.status.lower() == status.lower()]
        print(f"\nFiltered Programs (Status = '{status}'):")
        display_programs_table(results)

    elif choice == "3":
        min_f = prompt_number("Minimum Fee ($)", is_float=True, allow_zero=True, default=0.0)
        max_f = prompt_number("Maximum Fee ($)", is_float=True, allow_zero=True, default=999999.0)
        results = [p for p in programs if min_f <= p.fee <= max_f]
        print(f"\nFiltered Programs (Fee: ${min_f:,.2f} to ${max_f:,.2f}):")
        display_programs_table(results)


def filter_inquiries(inquiries: List[Inquiry]) -> None:
    """Interactive filtering of inquiries by status, priority tier, or customer."""
    print("\n--- FILTER INQUIRIES ---")
    print("  1. Filter by Status (Open / In Progress / Resolved / Closed)")
    print("  2. Filter by Priority (Low / Medium / High / Urgent)")
    print("  3. Filter by Customer Name or ID")
    print("  4. Return to Search Menu")

    choice = prompt_string("Choose filter criteria (1-4)")

    if choice == "1":
        status = prompt_choice("Select Status", Inquiry.VALID_STATUSES, default="Open")
        results = [inq for inq in inquiries if inq.status.lower() == status.lower()]
        print(f"\nFiltered Inquiries (Status = '{status}'):")
        display_inquiries_table(results)

    elif choice == "2":
        prio = prompt_choice("Select Priority", Inquiry.VALID_PRIORITIES, default="High")
        results = [inq for inq in inquiries if inq.priority.lower() == prio.lower()]
        print(f"\nFiltered Inquiries (Priority = '{prio}'):")
        display_inquiries_table(results)

    elif choice == "3":
        query = prompt_string("Enter Customer Name or Customer ID to match").lower()
        results = [
            inq for inq in inquiries
            if query in inq.customer_name.lower() or query in inq.customer_id.lower()
        ]
        print(f"\nFiltered Inquiries for Customer query '{query}':")
        display_inquiries_table(results)


def search_filter_menu(
    services: List[Service],
    programs: List[Program],
    inquiries: List[Inquiry],
) -> None:
    """Interactive submenu loop for Search & Filtering operations."""
    while True:
        print("\n" + "=" * 50)
        print(" SEARCH & FILTERING ENGINE".center(50))
        print("=" * 50)
        print("  1. Keyword Search (Services & Programs)")
        print("  2. Filter Services (Category, Status, Price)")
        print("  3. Filter Programs (Type, Status, Fee)")
        print("  4. Filter Inquiries (Status, Priority, Customer)")
        print("  5. Return to Main Menu")
        print("=" * 50)

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            search_offerings_by_keyword(services, programs)
        elif choice == "2":
            filter_services(services)
        elif choice == "3":
            filter_programs(programs)
        elif choice == "4":
            filter_inquiries(inquiries)
        elif choice == "5":
            break
        else:
            print("  [!] Invalid choice. Please enter a number between 1 and 5.")
