"""
modules/program_manager.py
--------------------------
Program and internship management module for Veda Technology.

Supports:
- Listing and viewing training, internship, and technology programs.
- Viewing complete program details.
- Adding a new program with rigorous input validation.
- Updating existing program records.
- Deleting programs safely.
"""

from typing import List, Optional
from models.program import Program
from models.inquiry import Inquiry
from modules import storage
from modules.validators import (
    validate_unique_id,
    prompt_string,
    prompt_number,
    prompt_choice,
    prompt_date,
    prompt_confirm,
)


def display_programs_table(programs: List[Program]) -> None:
    """Print an aligned ASCII table of all programs."""
    if not programs:
        print("\n  [i] No programs found.")
        return

    print("\n" + "=" * 105)
    print(f"{'ID':<10} | {'PROGRAM NAME':<34} | {'TYPE':<12} | {'DURATION':<10} | {'FEE ($)':>9} | {'SEATS':>5} | {'START DATE':<10} | {'STATUS':<9}")
    print("-" * 105)
    for p in programs:
        name_disp = p.name if len(p.name) <= 32 else p.name[:29] + "..."
        fee_disp = f"{p.fee:>9,.2f}" if p.fee > 0 else f"{'FREE':>9}"
        print(
            f"{p.id:<10} | {name_disp:<34} | {p.type:<12} | {p.duration:<10} | "
            f"{fee_disp} | {p.seats:>5} | {p.start_date:<10} | {p.status:<9}"
        )
    print("=" * 105)
    print(f" Total Programs: {len(programs)}")


def find_program_by_id(programs: List[Program], program_id: str) -> Optional[Program]:
    """Look up a Program by its ID (case-insensitive)."""
    clean_id = program_id.strip().upper()
    for p in programs:
        if p.id.upper() == clean_id:
            return p
    return None


def view_all_programs(programs: List[Program]) -> None:
    """Submenu action: Display all programs."""
    print("\n--- ALL VEDA TECHNOLOGY TRAINING & INTERNSHIP PROGRAMS ---")
    display_programs_table(programs)


def view_program_detail(programs: List[Program]) -> None:
    """Submenu action: View detailed information for a single program."""
    if not programs:
        print("\n  [!] No programs available to view.")
        return

    prg_id = prompt_string("\nEnter Program ID to view (e.g., PRG-201)")
    program = find_program_by_id(programs, prg_id)
    if not program:
        print(f"  [!] Program with ID '{prg_id}' not found.")
        return

    fee_str = f"${program.fee:,.2f} USD" if program.fee > 0 else "Free / Sponsored"
    print("\n" + "=" * 60)
    print(" PROGRAM DETAILS".center(60))
    print("=" * 60)
    print(f"  Program ID   : {program.id}")
    print(f"  Name         : {program.name}")
    print(f"  Track Type   : {program.type}")
    print(f"  Duration     : {program.duration}")
    print(f"  Tuition Fee  : {fee_str}")
    print(f"  Total Seats  : {program.seats}")
    print(f"  Start Date   : {program.start_date}")
    print(f"  Status       : {program.status}")
    print("=" * 60)


def add_program(programs: List[Program]) -> None:
    """Submenu action: Add a new program with complete validation."""
    print("\n--- ADD NEW TECHNOLOGY / TRAINING PROGRAM ---")
    existing_ids = [p.id for p in programs]

    while True:
        prg_id = prompt_string("Enter Program ID (e.g., PRG-207)")
        try:
            prg_id = validate_unique_id(prg_id, existing_ids, "Program")
            break
        except ValueError as err:
            print(f"  [!] {err}")

    name = prompt_string("Enter Program Name (e.g., Cloud Security Specialist)")
    prg_type = prompt_choice("Select Program Type", Program.VALID_TYPES, default="Training")
    duration = prompt_string("Enter Duration (e.g., 8 Weeks, 3 Months)")
    fee = prompt_number("Enter Enrollment Fee in USD ($) [0 for Free/Sponsored]", is_float=True, allow_zero=True)
    seats = prompt_number("Enter Total Seat Capacity", is_float=False, allow_zero=False)
    start_date = prompt_date("Enter Scheduled Start Date (YYYY-MM-DD)")
    status = prompt_choice("Select Initial Status", Program.VALID_STATUSES, default="Active")

    new_prg = Program(
        id=prg_id,
        name=name,
        type=prg_type,
        duration=duration,
        fee=fee,
        seats=seats,
        start_date=start_date,
        status=status,
    )

    programs.append(new_prg)
    if storage.save_programs(programs):
        print(f"\n  [OK] Program '{new_prg.name}' [{new_prg.id}] successfully added and saved!")
    else:
        print("\n  [Warning] Program added in memory, but disk persistence encountered an issue.")


def update_program(programs: List[Program]) -> None:
    """Submenu action: Update an existing program record."""
    if not programs:
        print("\n  [!] No programs available to update.")
        return

    display_programs_table(programs)
    prg_id = prompt_string("\nEnter Program ID to update")
    program = find_program_by_id(programs, prg_id)
    if not program:
        print(f"  [!] Program with ID '{prg_id}' not found.")
        return

    print(f"\nUpdating Program [{program.id}]. Press Enter to keep current value.")

    new_name = prompt_string("Name", default=program.name)
    new_type = prompt_choice("Type", Program.VALID_TYPES, default=program.type)
    new_duration = prompt_string("Duration", default=program.duration)
    new_fee = prompt_number("Fee ($)", is_float=True, allow_zero=True, default=program.fee)
    new_seats = prompt_number("Seats", is_float=False, allow_zero=False, default=program.seats)
    new_start = prompt_date("Start Date (YYYY-MM-DD)", default=program.start_date)
    new_status = prompt_choice("Status", Program.VALID_STATUSES, default=program.status)

    program.name = new_name
    program.type = new_type
    program.duration = new_duration
    program.fee = new_fee
    program.seats = new_seats
    program.start_date = new_start
    program.status = new_status

    if storage.save_programs(programs):
        print(f"\n  [OK] Program [{program.id}] updated successfully!")
    else:
        print("\n  [Warning] Program updated in memory, but failed to save file.")


def delete_program(programs: List[Program], inquiries: Optional[List[Inquiry]] = None) -> None:
    """Submenu action: Delete a program with confirmation and reference checks."""
    if not programs:
        print("\n  [!] No programs available to delete.")
        return

    display_programs_table(programs)
    prg_id = prompt_string("\nEnter Program ID to delete")
    program = find_program_by_id(programs, prg_id)
    if not program:
        print(f"  [!] Program with ID '{prg_id}' not found.")
        return

    if inquiries:
        linked_inquiries = [inq for inq in inquiries if inq.target_id.upper() == program.id.upper()]
        if linked_inquiries:
            print(f"\n  [Note] There are {len(linked_inquiries)} customer inquiry/inquiries linked to this program.")

    if prompt_confirm(f"Are you sure you want to delete '{program.name}' [{program.id}]?", default_yes=False):
        programs.remove(program)
        if storage.save_programs(programs):
            print(f"  [OK] Program [{program.id}] deleted successfully.")
        else:
            print("  [Warning] Program deleted from memory, but failed to save file.")
    else:
        print("  [i] Deletion cancelled.")


def program_menu(programs: List[Program], inquiries: Optional[List[Inquiry]] = None) -> None:
    """Interactive submenu loop for Program & Internship Management."""
    while True:
        print("\n" + "=" * 50)
        print(" PROGRAM & INTERNSHIP MANAGEMENT".center(50))
        print("=" * 50)
        print("  1. View All Programs")
        print("  2. View Program Details by ID")
        print("  3. Add New Program")
        print("  4. Update Program")
        print("  5. Delete Program")
        print("  6. Return to Main Menu")
        print("=" * 50)

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            view_all_programs(programs)
        elif choice == "2":
            view_program_detail(programs)
        elif choice == "3":
            add_program(programs)
        elif choice == "4":
            update_program(programs)
        elif choice == "5":
            delete_program(programs, inquiries)
        elif choice == "6":
            break
        else:
            print("  [!] Invalid choice. Please enter a number between 1 and 6.")
