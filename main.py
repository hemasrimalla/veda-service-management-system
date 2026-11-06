"""
main.py
-------
Entry point for the Veda Technology Business & Service Management System.

A modular, menu-driven CLI application simulating the business operations,
service offerings, training and internship programs, customer registry,
and customer inquiry lifecycle of Veda Technology.

Run:
    python main.py
"""

import sys
import os

# Ensure project root is in the Python search path for clean modular imports
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules import storage
from modules.service_manager import service_menu
from modules.program_manager import program_menu
from modules.inquiry_manager import inquiry_menu
from modules.search_filter import search_filter_menu
from modules.reports import reports_menu
from modules.validators import prompt_confirm


def print_banner() -> None:
    """Print the startup branding banner."""
    print("\n" + "=" * 72)
    print("      VEDA TECHNOLOGY BUSINESS & SERVICE MANAGEMENT SYSTEM")
    print("          Enterprise Digital Services & Academy Platform")
    print("=" * 72)
    print("  Welcome! Manage digital services, training programs, client")
    print("  registrations, customer inquiries, search, and executive analytics.")
    print("=" * 72)


def display_system_status(services, programs, customers, inquiries) -> None:
    """Display real-time record counts and data persistence paths."""
    print("\n" + "=" * 60)
    print(" SYSTEM STORAGE & DATA STATUS".center(60))
    print("=" * 60)
    print(f"  Storage Directory : {storage.DATA_DIR}")
    print(f"  Services Loaded   : {len(services)} records (File: services.json)")
    print(f"  Programs Loaded   : {len(programs)} records (File: programs.json)")
    print(f"  Customers Loaded  : {len(customers)} records (File: customers.json)")
    print(f"  Inquiries Loaded  : {len(inquiries)} records (File: inquiries.json)")
    print("-" * 60)

    if prompt_confirm("Do you want to re-load datasets from disk?", default_yes=False):
        services.clear()
        services.extend(storage.load_services())
        programs.clear()
        programs.extend(storage.load_programs())
        customers.clear()
        customers.extend(storage.load_customers())
        inquiries.clear()
        inquiries.extend(storage.load_inquiries())
        print("  [OK] Datasets successfully reloaded from disk.")


def main() -> None:
    """Main application lifecycle loop."""
    print_banner()

    # Step 1: Initialize JSON persistence files and seed defaults if empty
    storage.initialize_storage()

    # Step 2: Load current datasets into in-memory object collections
    services = storage.load_services()
    programs = storage.load_programs()
    customers = storage.load_customers()
    inquiries = storage.load_inquiries()

    print(
        f"[i] Storage ready: {len(services)} services, {len(programs)} programs, "
        f"{len(customers)} customers, {len(inquiries)} inquiries loaded.\n"
    )

    # Step 3: Main interactive menu loop
    while True:
        try:
            print("\n" + "=" * 52)
            print(" MAIN NAVIGATION MENU".center(52))
            print("=" * 52)
            print("  1. Digital Service Management")
            print("  2. Program & Internship Management")
            print("  3. Customer & Inquiry Management")
            print("  4. Search & Multi-Criteria Filtering")
            print("  5. Business Analytics & Reports")
            print("  6. System Data Status & Reload")
            print("  7. Exit Application")
            print("=" * 52)

            choice = input("Select an option (1-7): ").strip()

            if choice == "1":
                service_menu(services, inquiries)
            elif choice == "2":
                program_menu(programs, inquiries)
            elif choice == "3":
                inquiry_menu(inquiries, customers, services, programs)
            elif choice == "4":
                search_filter_menu(services, programs, inquiries)
            elif choice == "5":
                reports_menu(services, programs, customers, inquiries)
            elif choice == "6":
                display_system_status(services, programs, customers, inquiries)
            elif choice == "7":
                print("\nThank you for using Veda Technology Business & Service Management System!")
                print("Exiting application. Goodbye.\n")
                break
            else:
                print("  [!] Invalid selection. Please enter a number between 1 and 7.")

        except (KeyboardInterrupt, EOFError):
            print("\n\nOperation interrupted by user. Exiting safely...")
            break


if __name__ == "__main__":
    main()
