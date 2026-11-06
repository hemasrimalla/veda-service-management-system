"""
modules/inquiry_manager.py
--------------------------
Customer registration and service inquiry lifecycle management for Veda Technology.

Handles:
- Customer registration and directory management.
- Logging client requests linked to a registered customer and a specific service or program.
- Updating inquiry statuses ('Open', 'In Progress', 'Resolved', 'Closed') and priorities.
- Deleting inquiries.
"""

from typing import List, Optional
from models.customer import Customer
from models.inquiry import Inquiry
from models.service import Service
from models.program import Program
from modules import storage
from modules.validators import (
    validate_unique_id,
    prompt_string,
    prompt_choice,
    prompt_confirm,
)


# ==============================================================================
# CUSTOMER MANAGEMENT FUNCTIONS
# ==============================================================================

def display_customers_table(customers: List[Customer]) -> None:
    """Print an aligned ASCII table of registered customers."""
    if not customers:
        print("\n  [i] No customers registered yet.")
        return

    print("\n" + "=" * 95)
    print(f"{'ID':<10} | {'NAME':<22} | {'COMPANY / ORG':<22} | {'EMAIL':<24} | {'REGISTERED':<10}")
    print("-" * 95)
    for c in customers:
        name_disp = c.name if len(c.name) <= 20 else c.name[:17] + "..."
        comp_disp = c.company if len(c.company) <= 20 else c.company[:17] + "..."
        email_disp = c.email if len(c.email) <= 22 else c.email[:19] + "..."
        print(f"{c.id:<10} | {name_disp:<22} | {comp_disp:<22} | {email_disp:<24} | {c.registered_date:<10}")
    print("=" * 95)
    print(f" Total Customers: {len(customers)}")


def find_customer_by_id(customers: List[Customer], customer_id: str) -> Optional[Customer]:
    """Look up a Customer by ID (case-insensitive)."""
    clean_id = customer_id.strip().upper()
    for c in customers:
        if c.id.upper() == clean_id:
            return c
    return None


def register_customer(customers: List[Customer]) -> Optional[Customer]:
    """Prompt user and register a new customer."""
    print("\n--- REGISTER NEW CUSTOMER ---")
    existing_ids = [c.id for c in customers]

    while True:
        cust_id = prompt_string("Enter Customer ID (e.g., CUST-007)")
        try:
            cust_id = validate_unique_id(cust_id, existing_ids, "Customer")
            break
        except ValueError as err:
            print(f"  [!] {err}")

    name = prompt_string("Enter Full Name")
    email = prompt_string("Enter Contact Email")
    phone = prompt_string("Enter Contact Phone")
    company = prompt_string("Enter Company / Institution (or press Enter for Individual)", allow_empty=True, default="Individual")

    new_cust = Customer(
        id=cust_id,
        name=name,
        email=email,
        phone=phone,
        company=company,
    )

    customers.append(new_cust)
    if storage.save_customers(customers):
        print(f"\n  [OK] Customer '{new_cust.name}' [{new_cust.id}] registered and saved successfully!")
    else:
        print("\n  [Warning] Customer registered in memory, but disk save encountered an issue.")

    return new_cust


def view_all_customers(customers: List[Customer]) -> None:
    """Submenu action: View all registered customers."""
    print("\n--- REGISTERED CLIENTS & PROSPECTS ---")
    display_customers_table(customers)


def update_customer(customers: List[Customer]) -> None:
    """Submenu action: Update customer contact details."""
    if not customers:
        print("\n  [!] No customers registered.")
        return

    display_customers_table(customers)
    cust_id = prompt_string("\nEnter Customer ID to update")
    customer = find_customer_by_id(customers, cust_id)
    if not customer:
        print(f"  [!] Customer with ID '{cust_id}' not found.")
        return

    print(f"\nUpdating Customer [{customer.id}]. Press Enter to keep current value.")
    new_name = prompt_string("Name", default=customer.name)
    new_email = prompt_string("Email", default=customer.email)
    new_phone = prompt_string("Phone", default=customer.phone)
    new_company = prompt_string("Company", default=customer.company)

    customer.name = new_name
    customer.email = new_email
    customer.phone = new_phone
    customer.company = new_company

    if storage.save_customers(customers):
        print(f"\n  [OK] Customer [{customer.id}] updated successfully!")
    else:
        print("\n  [Warning] Customer updated in memory, but failed to save file.")


# ==============================================================================
# INQUIRY MANAGEMENT FUNCTIONS
# ==============================================================================

def display_inquiries_table(inquiries: List[Inquiry]) -> None:
    """Print an aligned ASCII table of all inquiries."""
    if not inquiries:
        print("\n  [i] No inquiries found.")
        return

    print("\n" + "=" * 115)
    print(f"{'ID':<10} | {'CUSTOMER':<20} | {'TARGET OFFERING':<30} | {'PRIORITY':<9} | {'STATUS':<12} | {'DATE':<10}")
    print("-" * 115)
    for inq in inquiries:
        cust_disp = inq.customer_name if len(inq.customer_name) <= 18 else inq.customer_name[:15] + "..."
        target_disp = f"[{inq.target_type[:1]}] {inq.target_name}"
        if len(target_disp) > 28:
            target_disp = target_disp[:25] + "..."
        print(
            f"{inq.id:<10} | {cust_disp:<20} | {target_disp:<30} | "
            f"{inq.priority:<9} | {inq.status:<12} | {inq.created_date:<10}"
        )
    print("=" * 115)
    print(f" Total Inquiries: {len(inquiries)}")


def find_inquiry_by_id(inquiries: List[Inquiry], inquiry_id: str) -> Optional[Inquiry]:
    """Look up an Inquiry by its ID (case-insensitive)."""
    clean_id = inquiry_id.strip().upper()
    for inq in inquiries:
        if inq.id.upper() == clean_id:
            return inq
    return None


def view_all_inquiries(inquiries: List[Inquiry]) -> None:
    """Submenu action: List all inquiries."""
    print("\n--- ALL CUSTOMER INQUIRIES & SERVICE REQUESTS ---")
    display_inquiries_table(inquiries)


def view_inquiry_detail(inquiries: List[Inquiry]) -> None:
    """Submenu action: View detailed information for a single inquiry."""
    if not inquiries:
        print("\n  [!] No inquiries available to view.")
        return

    inq_id = prompt_string("\nEnter Inquiry ID to view (e.g., INQ-301)")
    inquiry = find_inquiry_by_id(inquiries, inq_id)
    if not inquiry:
        print(f"  [!] Inquiry with ID '{inq_id}' not found.")
        return

    print("\n" + "=" * 65)
    print(" INQUIRY / SERVICE REQUEST DETAILS".center(65))
    print("=" * 65)
    print(f"  Inquiry ID       : {inquiry.id}")
    print(f"  Date Logged      : {inquiry.created_date}")
    print(f"  Status           : {inquiry.status}")
    print(f"  Priority         : {inquiry.priority}")
    print("-" * 65)
    print(f"  Customer         : {inquiry.customer_name} (ID: {inquiry.customer_id})")
    print(f"  Offering Type    : {inquiry.target_type}")
    print(f"  Target Item      : {inquiry.target_name} (ID: {inquiry.target_id})")
    print(f"  Subject          : {inquiry.subject}")
    print(f"  Message / Scope  : {inquiry.message}")
    print("=" * 65)


def log_inquiry(
    inquiries: List[Inquiry],
    customers: List[Customer],
    services: List[Service],
    programs: List[Program],
) -> None:
    """Submenu action: Register an inquiry linked to a customer and service/program."""
    print("\n--- LOG NEW CUSTOMER INQUIRY / SERVICE REQUEST ---")

    # Step 1: Select or register customer
    customer: Optional[Customer] = None
    if customers:
        display_customers_table(customers)
        cust_id = prompt_string("\nEnter Customer ID (or type 'NEW' to register a new customer)")
        if cust_id.upper() == "NEW":
            customer = register_customer(customers)
        else:
            customer = find_customer_by_id(customers, cust_id)
            if not customer:
                print(f"  [!] Customer '{cust_id}' not found. Please register first.")
                if prompt_confirm("Would you like to register this customer now?"):
                    customer = register_customer(customers)
                else:
                    return
    else:
        print("  [i] No customers registered yet. Let's register the first customer.")
        customer = register_customer(customers)

    if not customer:
        print("  [!] Customer selection aborted.")
        return

    # Step 2: Select Offering Type (Service or Program)
    offering_type = prompt_choice("Inquiry Type", ["Service", "Program"], default="Service")
    target_id = ""
    target_name = ""

    if offering_type == "Service":
        if not services:
            print("  [!] No services available in the system.")
            return
        print("\nAvailable Services:")
        for s in services:
            print(f"  - [{s.id}] {s.name} (${s.price:,.2f}) [{s.status}]")
        while True:
            srv_choice = prompt_string("Enter Target Service ID").upper()
            found = next((s for s in services if s.id.upper() == srv_choice), None)
            if found:
                target_id = found.id
                target_name = found.name
                break
            print("  [!] Invalid Service ID. Try again.")
    else:
        if not programs:
            print("  [!] No programs available in the system.")
            return
        print("\nAvailable Programs:")
        for p in programs:
            print(f"  - [{p.id}] {p.name} ({p.type}) [{p.status}]")
        while True:
            prg_choice = prompt_string("Enter Target Program ID").upper()
            found = next((p for p in programs if p.id.upper() == prg_choice), None)
            if found:
                target_id = found.id
                target_name = found.name
                break
            print("  [!] Invalid Program ID. Try again.")

    # Step 3: Inquiry Metadata
    existing_ids = [inq.id for inq in inquiries]
    while True:
        inq_id = prompt_string("Enter Inquiry ID (e.g., INQ-307)")
        try:
            inq_id = validate_unique_id(inq_id, existing_ids, "Inquiry")
            break
        except ValueError as err:
            print(f"  [!] {err}")

    subject = prompt_string("Enter Subject / Short Summary")
    message = prompt_string("Enter Inquiry Details / Customer Requirements")
    priority = prompt_choice("Set Priority", Inquiry.VALID_PRIORITIES, default="Medium")
    status = prompt_choice("Set Initial Status", Inquiry.VALID_STATUSES, default="Open")

    new_inq = Inquiry(
        id=inq_id,
        customer_id=customer.id,
        customer_name=customer.name,
        target_type=offering_type,
        target_id=target_id,
        target_name=target_name,
        subject=subject,
        message=message,
        status=status,
        priority=priority,
    )

    inquiries.append(new_inq)
    if storage.save_inquiries(inquiries):
        print(f"\n  [OK] Inquiry [{new_inq.id}] logged successfully for {customer.name}!")
    else:
        print("\n  [Warning] Inquiry created in memory, but disk save encountered an issue.")


def update_inquiry_status_priority(inquiries: List[Inquiry]) -> None:
    """Submenu action: Update lifecycle status and priority tier."""
    if not inquiries:
        print("\n  [!] No inquiries available.")
        return

    display_inquiries_table(inquiries)
    inq_id = prompt_string("\nEnter Inquiry ID to update")
    inquiry = find_inquiry_by_id(inquiries, inq_id)
    if not inquiry:
        print(f"  [!] Inquiry with ID '{inq_id}' not found.")
        return

    print(f"\nUpdating Inquiry [{inquiry.id}] - Current Status: {inquiry.status}, Priority: {inquiry.priority}")
    new_status = prompt_choice("Select New Status", Inquiry.VALID_STATUSES, default=inquiry.status)
    new_priority = prompt_choice("Select New Priority", Inquiry.VALID_PRIORITIES, default=inquiry.priority)

    inquiry.status = new_status
    inquiry.priority = new_priority

    if storage.save_inquiries(inquiries):
        print(f"\n  [OK] Inquiry [{inquiry.id}] updated: Status -> {inquiry.status}, Priority -> {inquiry.priority}")
    else:
        print("\n  [Warning] Inquiry updated in memory, but failed to save file.")


def delete_inquiry(inquiries: List[Inquiry]) -> None:
    """Submenu action: Delete an inquiry with confirmation."""
    if not inquiries:
        print("\n  [!] No inquiries available to delete.")
        return

    display_inquiries_table(inquiries)
    inq_id = prompt_string("\nEnter Inquiry ID to delete")
    inquiry = find_inquiry_by_id(inquiries, inq_id)
    if not inquiry:
        print(f"  [!] Inquiry with ID '{inq_id}' not found.")
        return

    if prompt_confirm(f"Are you sure you want to delete Inquiry [{inquiry.id}] '{inquiry.subject}'?", default_yes=False):
        inquiries.remove(inquiry)
        if storage.save_inquiries(inquiries):
            print(f"  [OK] Inquiry [{inquiry.id}] deleted successfully.")
        else:
            print("  [Warning] Inquiry deleted from memory, but failed to save file.")
    else:
        print("  [i] Deletion cancelled.")


def inquiry_menu(
    inquiries: List[Inquiry],
    customers: List[Customer],
    services: List[Service],
    programs: List[Program],
) -> None:
    """Interactive submenu loop for Customer & Inquiry Management."""
    while True:
        print("\n" + "=" * 50)
        print(" CUSTOMER & INQUIRY MANAGEMENT".center(50))
        print("=" * 50)
        print("  1. View All Inquiries")
        print("  2. View Inquiry Details by ID")
        print("  3. Log New Inquiry / Service Request")
        print("  4. Update Inquiry Status & Priority")
        print("  5. Delete Inquiry")
        print("  6. Register New Customer")
        print("  7. View All Registered Customers")
        print("  8. Update Customer Details")
        print("  9. Return to Main Menu")
        print("=" * 50)

        choice = input("Select an option (1-9): ").strip()

        if choice == "1":
            view_all_inquiries(inquiries)
        elif choice == "2":
            view_inquiry_detail(inquiries)
        elif choice == "3":
            log_inquiry(inquiries, customers, services, programs)
        elif choice == "4":
            update_inquiry_status_priority(inquiries)
        elif choice == "5":
            delete_inquiry(inquiries)
        elif choice == "6":
            register_customer(customers)
        elif choice == "7":
            view_all_customers(customers)
        elif choice == "8":
            update_customer(customers)
        elif choice == "9":
            break
        else:
            print("  [!] Invalid choice. Please enter a number between 1 and 9.")
