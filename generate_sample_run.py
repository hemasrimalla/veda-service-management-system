"""
generate_sample_run.py
----------------------
Script to run main.py interactively via piped standard input, exercising each
menu option and writing a comprehensive transcript to sample_output/sample_run.txt.
"""

import subprocess
import sys
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_PY = os.path.join(PROJECT_DIR, "main.py")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "sample_output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "sample_run.txt")

simulated_inputs = [
    # -------------------------------------------------------------
    # 1. Digital Service Management
    # -------------------------------------------------------------
    "1",             # Main menu: 1. Digital Service Management
    "1",             # 1. View All Services
    "2",             # 2. View Service Details by ID
    "SRV-101",       # Service ID
    "3",             # 3. Add New Service
    "SRV-107",       # Service ID
    "Cybersecurity Vulnerability Assessment", # Service Name
    "Cybersecurity", # Category
    "Comprehensive vulnerability assessment and penetration testing.", # Description
    "4200.0",        # Price
    "Active",        # Status
    "4",             # 4. Update Service
    "SRV-107",       # Target Service ID
    "",              # Keep Name
    "",              # Keep Category
    "",              # Keep Description
    "4500.0",        # Updated Price
    "",              # Keep Status
    "6",             # 6. Return to Main Menu

    # -------------------------------------------------------------
    # 2. Program & Internship Management
    # -------------------------------------------------------------
    "2",             # Main menu: 2. Program Management
    "1",             # 1. View All Programs
    "2",             # 2. View Program Details by ID
    "PRG-201",       # Program ID
    "3",             # 3. Add New Program
    "PRG-207",       # Program ID
    "AI Agents & LLM Engineering Masterclass", # Name
    "Training",      # Type
    "8 Weeks",       # Duration
    "1400.0",        # Fee
    "25",            # Seats
    "2027-03-01",    # Start Date
    "Active",        # Status
    "6",             # 6. Return to Main Menu

    # -------------------------------------------------------------
    # 3. Customer & Inquiry Management
    # -------------------------------------------------------------
    "3",             # Main menu: 3. Customer & Inquiry Management
    "7",             # 7. View All Registered Customers
    "6",             # 6. Register New Customer
    "CUST-007",      # Customer ID
    "Elena Rostova", # Full Name
    "elena@quantumscale.io", # Email
    "+1-555-0144",   # Phone
    "QuantumScale AI Labs", # Company
    "1",             # 1. View All Inquiries
    "2",             # 2. View Inquiry Details
    "INQ-301",       # Inquiry ID
    "3",             # 3. Log New Inquiry
    "CUST-007",      # Existing Customer ID
    "Service",       # Offering Type
    "SRV-101",       # Target Service ID
    "INQ-307",       # Inquiry ID
    "Microservices Migration Consultation", # Subject
    "Need technical evaluation for converting Django monolith to FastAPI.", # Message
    "High",          # Priority
    "Open",          # Status
    "4",             # 4. Update Inquiry Status & Priority
    "INQ-307",       # Inquiry ID
    "In Progress",   # New Status
    "Urgent",        # New Priority
    "9",             # 9. Return to Main Menu

    # -------------------------------------------------------------
    # 4. Search & Multi-Criteria Filtering
    # -------------------------------------------------------------
    "4",             # Main menu: 4. Search & Filtering
    "1",             # 1. Keyword Search
    "cloud",         # Keyword
    "2",             # 2. Filter Services
    "1",             # Filter by Category
    "Web",           # Category keyword
    "3",             # 3. Filter Programs
    "1",             # Filter by Type
    "Internship",    # Type
    "4",             # 4. Filter Inquiries
    "1",             # Filter by Status
    "Open",          # Status
    "5",             # 5. Return to Main Menu

    # -------------------------------------------------------------
    # 5. Business Analytics & Reports
    # -------------------------------------------------------------
    "5",             # Main menu: 5. Business Analytics & Reports
    "1",             # 1. Executive Summary
    "2",             # 2. Inquiry Distribution by Status & Priority
    "3",             # 3. Most Requested Services & Programs
    "4",             # 4. Program Capacity & Revenue Estimation
    "5",             # 5. Full Business Health Report
    "6",             # 6. Export Report to File
    "TXT",           # TXT format
    "veda_executive_report.txt", # Filename
    "6",             # 6. Export Report to File
    "CSV",           # CSV format
    "veda_business_metrics.csv", # Filename
    "7",             # 7. Return to Main Menu

    # -------------------------------------------------------------
    # 6. System Data Status & Reload
    # -------------------------------------------------------------
    "6",             # Main menu: 6. System Data Status
    "n",             # Don't reload

    # -------------------------------------------------------------
    # 7. Exit Application
    # -------------------------------------------------------------
    "7",             # Main menu: 7. Exit Application
]


def run_simulation() -> None:
    """Execute main.py piping simulated inputs and capture output."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Reset seed data so the run transcript is completely clean and reproducible
    from modules import storage
    storage.save_json(storage.SERVICES_FILE, storage.SEED_SERVICES)
    storage.save_json(storage.PROGRAMS_FILE, storage.SEED_PROGRAMS)
    storage.save_json(storage.CUSTOMERS_FILE, storage.SEED_CUSTOMERS)
    storage.save_json(storage.INQUIRIES_FILE, storage.SEED_INQUIRIES)

    input_stream = "\n".join(simulated_inputs) + "\n"

    print("Executing full interactive menu walkthrough simulation...")
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.Popen(
        [sys.executable, MAIN_PY],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        cwd=PROJECT_DIR,
    )

    stdout_data, _ = proc.communicate(input=input_stream)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(stdout_data)

    print(f"Simulation completed with exit code: {proc.returncode}")
    print(f"Output recorded to: {OUTPUT_FILE}")


if __name__ == "__main__":
    run_simulation()
