"""
modules/service_manager.py
--------------------------
Service management module for Veda Technology.

Supports:
- Listing and viewing digital services in clean tabular layout.
- Viewing complete service details.
- Adding a new service with full validation.
- Updating existing service attributes.
- Deleting an obsolete service safely.
"""

from typing import List, Optional
from models.service import Service
from models.inquiry import Inquiry
from modules import storage
from modules.validators import (
    validate_unique_id,
    prompt_string,
    prompt_number,
    prompt_choice,
    prompt_confirm,
)


def display_services_table(services: List[Service]) -> None:
    """Print a formatted ASCII table of services."""
    if not services:
        print("\n  [i] No services found.")
        return

    print("\n" + "=" * 90)
    print(f"{'ID':<10} | {'SERVICE NAME':<32} | {'CATEGORY':<20} | {'PRICE ($)':>10} | {'STATUS':<8}")
    print("-" * 90)
    for s in services:
        name_disp = s.name if len(s.name) <= 30 else s.name[:27] + "..."
        cat_disp = s.category if len(s.category) <= 18 else s.category[:15] + "..."
        print(f"{s.id:<10} | {name_disp:<32} | {cat_disp:<20} | {s.price:>10,.2f} | {s.status:<8}")
    print("=" * 90)
    print(f" Total Services: {len(services)}")


def find_service_by_id(services: List[Service], service_id: str) -> Optional[Service]:
    """Look up a Service by its ID (case-insensitive)."""
    service_id_clean = service_id.strip().upper()
    for s in services:
        if s.id.upper() == service_id_clean:
            return s
    return None


def view_all_services(services: List[Service]) -> None:
    """Submenu action: List all services."""
    print("\n--- ALL VEDA TECHNOLOGY DIGITAL SERVICES ---")
    display_services_table(services)


def view_service_detail(services: List[Service]) -> None:
    """Submenu action: View detailed information for a specific service."""
    if not services:
        print("\n  [!] No services available to view.")
        return

    srv_id = prompt_string("\nEnter Service ID to view (e.g., SRV-101)")
    service = find_service_by_id(services, srv_id)
    if not service:
        print(f"  [!] Service with ID '{srv_id}' not found.")
        return

    print("\n" + "=" * 60)
    print(" SERVICE DETAILS".center(60))
    print("=" * 60)
    print(f"  Service ID   : {service.id}")
    print(f"  Name         : {service.name}")
    print(f"  Category     : {service.category}")
    print(f"  Base Price   : ${service.price:,.2f} USD")
    print(f"  Status       : {service.status}")
    print(f"  Description  : {service.description}")
    print("=" * 60)


def add_service(services: List[Service]) -> None:
    """Submenu action: Prompt user and add a new service."""
    print("\n--- ADD NEW DIGITAL SERVICE ---")
    existing_ids = [s.id for s in services]

    # Validate Unique ID
    while True:
        srv_id = prompt_string("Enter Service ID (e.g., SRV-107)")
        try:
            srv_id = validate_unique_id(srv_id, existing_ids, "Service")
            break
        except ValueError as err:
            print(f"  [!] {err}")

    name = prompt_string("Enter Service Name (e.g., Cloud Architecture Review)")
    category = prompt_string("Enter Category (e.g., Cloud Consulting, Web Dev, AI)")
    description = prompt_string("Enter Description / Scope of Work")
    price = prompt_number("Enter Base Price in USD ($)", is_float=True, allow_zero=True)
    status = prompt_choice("Select Status", Service.VALID_STATUSES, default="Active")

    new_srv = Service(
        id=srv_id,
        name=name,
        category=category,
        description=description,
        price=price,
        status=status,
    )

    services.append(new_srv)
    if storage.save_services(services):
        print(f"\n  [OK] Service '{new_srv.name}' [{new_srv.id}] created and saved successfully!")
    else:
        print("\n  [Warning] Service added in memory, but disk persistence encountered an issue.")


def update_service(services: List[Service]) -> None:
    """Submenu action: Update an existing service."""
    if not services:
        print("\n  [!] No services available to update.")
        return

    display_services_table(services)
    srv_id = prompt_string("\nEnter Service ID to update")
    service = find_service_by_id(services, srv_id)
    if not service:
        print(f"  [!] Service with ID '{srv_id}' not found.")
        return

    print(f"\nUpdating Service [{service.id}]. Press Enter to keep current value.")

    new_name = prompt_string(f"Name", default=service.name)
    new_cat = prompt_string(f"Category", default=service.category)
    new_desc = prompt_string(f"Description", default=service.description)
    new_price = prompt_number(f"Price ($)", is_float=True, allow_zero=True, default=service.price)
    new_status = prompt_choice(f"Status", Service.VALID_STATUSES, default=service.status)

    service.name = new_name
    service.category = new_cat
    service.description = new_desc
    service.price = new_price
    service.status = new_status

    if storage.save_services(services):
        print(f"\n  [OK] Service [{service.id}] successfully updated!")
    else:
        print("\n  [Warning] Service updated in memory, but disk persistence encountered an issue.")


def delete_service(services: List[Service], inquiries: Optional[List[Inquiry]] = None) -> None:
    """Submenu action: Delete a service with confirmation and reference checks."""
    if not services:
        print("\n  [!] No services available to delete.")
        return

    display_services_table(services)
    srv_id = prompt_string("\nEnter Service ID to delete")
    service = find_service_by_id(services, srv_id)
    if not service:
        print(f"  [!] Service with ID '{srv_id}' not found.")
        return

    # Check inquiry references
    if inquiries:
        linked_inquiries = [inq for inq in inquiries if inq.target_id.upper() == service.id.upper()]
        if linked_inquiries:
            print(f"\n  [Note] There are {len(linked_inquiries)} customer inquiry/inquiries linked to this service.")

    if prompt_confirm(f"Are you sure you want to delete '{service.name}' [{service.id}]?", default_yes=False):
        services.remove(service)
        if storage.save_services(services):
            print(f"  [OK] Service [{service.id}] deleted successfully.")
        else:
            print("  [Warning] Service deleted from memory, but failed to save file.")
    else:
        print("  [i] Deletion cancelled.")


def service_menu(services: List[Service], inquiries: Optional[List[Inquiry]] = None) -> None:
    """Interactive submenu loop for Digital Service Management."""
    while True:
        print("\n" + "=" * 50)
        print(" DIGITAL SERVICE MANAGEMENT".center(50))
        print("=" * 50)
        print("  1. View All Services")
        print("  2. View Service Details by ID")
        print("  3. Add New Service")
        print("  4. Update Service")
        print("  5. Delete Service")
        print("  6. Return to Main Menu")
        print("=" * 50)

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            view_all_services(services)
        elif choice == "2":
            view_service_detail(services)
        elif choice == "3":
            add_service(services)
        elif choice == "4":
            update_service(services)
        elif choice == "5":
            delete_service(services, inquiries)
        elif choice == "6":
            break
        else:
            print("  [!] Invalid choice. Please enter a number between 1 and 6.")
