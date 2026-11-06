"""
modules/storage.py
------------------
JSON persistence and file I/O operations for Veda Technology Business & Service Management System.

Handles:
- Loading and saving domain entities (Services, Programs, Customers, Inquiries).
- Graceful recovery from missing, empty, or corrupted JSON files.
- Seed data initialization with realistic, synthetic enterprise records.
"""

import os
import json
import logging
from typing import List, Dict, Any

from models.service import Service
from models.program import Program
from models.customer import Customer
from models.inquiry import Inquiry

# Configure module-level paths relative to the project root
MODULES_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(MODULES_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

SERVICES_FILE = os.path.join(DATA_DIR, "services.json")
PROGRAMS_FILE = os.path.join(DATA_DIR, "programs.json")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.json")
INQUIRIES_FILE = os.path.join(DATA_DIR, "inquiries.json")


def ensure_data_dir() -> None:
    """Ensure the data/ storage directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def load_json(file_path: str, default: Any = None) -> Any:
    """Safely read and deserialize a JSON file with error handling.

    Args:
        file_path: Path to the target JSON file.
        default: Default value returned if the file is missing or corrupted.

    Returns:
        Deserialized JSON object or the default value.
    """
    if default is None:
        default = []

    if not os.path.exists(file_path):
        return default

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                # File is empty
                return default
            return json.loads(content)
    except json.JSONDecodeError as err:
        print(f"\n[Warning] Corrupted JSON detected in '{os.path.basename(file_path)}': {err}")
        print("          Proceeding with clean default state to prevent crash.")
        return default
    except OSError as err:
        print(f"\n[Error] Unable to read file '{file_path}': {err}")
        return default


def save_json(file_path: str, data: Any) -> bool:
    """Serialize and write data to a JSON file safely.

    Args:
        file_path: Target file destination.
        data: JSON-serializable Python data structure.

    Returns:
        bool: True on success, False on failure.
    """
    ensure_data_dir()
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except (OSError, TypeError) as err:
        print(f"\n[Error] Failed to persist data to '{file_path}': {err}")
        return False


# ==============================================================================
# SYNTHETIC SAMPLE SEED DATA
# ==============================================================================

SEED_SERVICES = [
    {
        "id": "SRV-101",
        "name": "Enterprise Web Development",
        "category": "Web Development",
        "description": "Full-cycle responsive web applications with microservices backend.",
        "price": 4500.0,
        "status": "Active",
    },
    {
        "id": "SRV-102",
        "name": "Cloud Infrastructure & DevOps",
        "category": "Cloud Consulting",
        "description": "AWS/Azure cloud architecture, CI/CD automation, and Docker orchestration.",
        "price": 6000.0,
        "status": "Active",
    },
    {
        "id": "SRV-103",
        "name": "Mobile Application Development",
        "category": "App Development",
        "description": "Native and cross-platform (Flutter/React Native) mobile apps.",
        "price": 5200.0,
        "status": "Active",
    },
    {
        "id": "SRV-104",
        "name": "Business Intelligence & Data Analytics",
        "category": "Data Analytics",
        "description": "Interactive PowerBI/Tableau dashboards and automated reporting pipelines.",
        "price": 3800.0,
        "status": "Active",
    },
    {
        "id": "SRV-105",
        "name": "AI & Machine Learning Integration",
        "category": "AI Solutions",
        "description": "Custom LLM agents, predictive models, and intelligent process automation.",
        "price": 7500.0,
        "status": "Active",
    },
    {
        "id": "SRV-106",
        "name": "Legacy System Modernization",
        "category": "Enterprise IT",
        "description": "Re-engineering monolithic mainframe systems into cloud-native microservices.",
        "price": 8000.0,
        "status": "Inactive",
    },
]

SEED_PROGRAMS = [
    {
        "id": "PRG-201",
        "name": "Full-Stack Python & React Engineering",
        "type": "Training",
        "duration": "12 Weeks",
        "fee": 1200.0,
        "seats": 30,
        "start_date": "2026-12-01",
        "status": "Active",
    },
    {
        "id": "PRG-202",
        "name": "Cloud & DevOps Professional Internship",
        "type": "Internship",
        "duration": "16 Weeks",
        "fee": 0.0,
        "seats": 15,
        "start_date": "2026-12-15",
        "status": "Active",
    },
    {
        "id": "PRG-203",
        "name": "Data Science & Machine Learning Bootcamp",
        "type": "Training",
        "duration": "10 Weeks",
        "fee": 1500.0,
        "seats": 25,
        "start_date": "2027-01-10",
        "status": "Upcoming",
    },
    {
        "id": "PRG-204",
        "name": "Enterprise Cybersecurity Fundamentals",
        "type": "Technology",
        "duration": "6 Weeks",
        "fee": 950.0,
        "seats": 20,
        "start_date": "2026-11-20",
        "status": "Active",
    },
    {
        "id": "PRG-205",
        "name": "Mobile App Development with Flutter Internship",
        "type": "Internship",
        "duration": "12 Weeks",
        "fee": 350.0,
        "seats": 18,
        "start_date": "2027-02-01",
        "status": "Upcoming",
    },
    {
        "id": "PRG-206",
        "name": "Cobol to Microservices Transition Workshop",
        "type": "Technology",
        "duration": "4 Weeks",
        "fee": 1800.0,
        "seats": 10,
        "start_date": "2026-08-01",
        "status": "Closed",
    },
]

SEED_CUSTOMERS = [
    {
        "id": "CUST-001",
        "name": "Sarah Jenkins",
        "email": "s.jenkins@apexglobal.io",
        "phone": "+1-415-555-0143",
        "company": "Apex Global Logistics",
        "registered_date": "2026-09-12",
    },
    {
        "id": "CUST-002",
        "name": "David Chen",
        "email": "david.c@finedgetech.com",
        "phone": "+1-206-555-0188",
        "company": "FinEdge Technologies",
        "registered_date": "2026-09-25",
    },
    {
        "id": "CUST-003",
        "name": "Priya Sharma",
        "email": "priya.sharma@horizonedu.org",
        "phone": "+91-98765-43210",
        "company": "Horizon University",
        "registered_date": "2026-10-02",
    },
    {
        "id": "CUST-004",
        "name": "Marcus Vance",
        "email": "marcus.vance@greenleaf.com",
        "phone": "+1-312-555-0177",
        "company": "GreenLeaf Organics",
        "registered_date": "2026-10-18",
    },
    {
        "id": "CUST-005",
        "name": "Aisha Al-Mansoor",
        "email": "aisha@novabiotech.ae",
        "phone": "+971-50-555-1234",
        "company": "Nova Biotech",
        "registered_date": "2026-10-28",
    },
    {
        "id": "CUST-006",
        "name": "Ethan Walker",
        "email": "ethan.w@student.mit.edu",
        "phone": "+1-617-555-0199",
        "company": "Individual Scholar",
        "registered_date": "2026-11-01",
    },
]

SEED_INQUIRIES = [
    {
        "id": "INQ-301",
        "customer_id": "CUST-001",
        "customer_name": "Sarah Jenkins",
        "target_type": "Service",
        "target_id": "SRV-102",
        "target_name": "Cloud Infrastructure & DevOps",
        "subject": "AWS Cloud Migration Assessment",
        "message": "Looking to migrate our on-premise logistics systems to AWS with high availability.",
        "status": "In Progress",
        "priority": "High",
        "created_date": "2026-10-15",
    },
    {
        "id": "INQ-302",
        "customer_id": "CUST-002",
        "customer_name": "David Chen",
        "target_type": "Service",
        "target_id": "SRV-101",
        "target_name": "Enterprise Web Development",
        "subject": "B2B FinTech Client Portal",
        "message": "Requesting scope and quotation for a secure customer financial dashboard.",
        "status": "Open",
        "priority": "Urgent",
        "created_date": "2026-10-22",
    },
    {
        "id": "INQ-303",
        "customer_id": "CUST-003",
        "customer_name": "Priya Sharma",
        "target_type": "Program",
        "target_id": "PRG-203",
        "target_name": "Data Science & Machine Learning Bootcamp",
        "subject": "Institutional Student Cohort Enrollment",
        "message": "Inquiry regarding group discount for enrolling 12 university seniors in the cohort.",
        "status": "Open",
        "priority": "Medium",
        "created_date": "2026-10-29",
    },
    {
        "id": "INQ-304",
        "customer_id": "CUST-004",
        "customer_name": "Marcus Vance",
        "target_type": "Service",
        "target_id": "SRV-103",
        "target_name": "Mobile Application Development",
        "subject": "iOS & Android Storefront App",
        "message": "Need a cross-platform retail app with barcode scanner and loyalty integration.",
        "status": "Resolved",
        "priority": "Medium",
        "created_date": "2026-10-20",
    },
    {
        "id": "INQ-305",
        "customer_id": "CUST-005",
        "customer_name": "Aisha Al-Mansoor",
        "target_type": "Service",
        "target_id": "SRV-105",
        "target_name": "AI & Machine Learning Integration",
        "subject": "Laboratory Predictive Analytics Model",
        "message": "Seeking AI consulting for biomedical research pipeline automation.",
        "status": "In Progress",
        "priority": "High",
        "created_date": "2026-11-02",
    },
    {
        "id": "INQ-306",
        "customer_id": "CUST-006",
        "customer_name": "Ethan Walker",
        "target_type": "Program",
        "target_id": "PRG-202",
        "target_name": "Cloud & DevOps Professional Internship",
        "subject": "DevOps Internship Screening Inquiry",
        "message": "Applied for the sponsored DevOps internship; inquiry on interview timeline.",
        "status": "Closed",
        "priority": "Low",
        "created_date": "2026-11-03",
    },
]


def initialize_storage() -> None:
    """Check and seed storage files with default records if not present or empty."""
    ensure_data_dir()

    # Initialize Services
    if not os.path.exists(SERVICES_FILE) or os.path.getsize(SERVICES_FILE) == 0:
        save_json(SERVICES_FILE, SEED_SERVICES)

    # Initialize Programs
    if not os.path.exists(PROGRAMS_FILE) or os.path.getsize(PROGRAMS_FILE) == 0:
        save_json(PROGRAMS_FILE, SEED_PROGRAMS)

    # Initialize Customers
    if not os.path.exists(CUSTOMERS_FILE) or os.path.getsize(CUSTOMERS_FILE) == 0:
        save_json(CUSTOMERS_FILE, SEED_CUSTOMERS)

    # Initialize Inquiries
    if not os.path.exists(INQUIRIES_FILE) or os.path.getsize(INQUIRIES_FILE) == 0:
        save_json(INQUIRIES_FILE, SEED_INQUIRIES)


# ==============================================================================
# ENTITY-SPECIFIC LOADERS & SAVERS
# ==============================================================================

def load_services() -> List[Service]:
    """Load all services from services.json into Service objects."""
    raw_list = load_json(SERVICES_FILE, default=None)
    if not raw_list:
        # Fallback to seed data if empty
        save_json(SERVICES_FILE, SEED_SERVICES)
        raw_list = SEED_SERVICES
    return [Service.from_dict(item) for item in raw_list]


def save_services(services: List[Service]) -> bool:
    """Persist a list of Service objects to services.json."""
    data = [srv.to_dict() for srv in services]
    return save_json(SERVICES_FILE, data)


def load_programs() -> List[Program]:
    """Load all programs from programs.json into Program objects."""
    raw_list = load_json(PROGRAMS_FILE, default=None)
    if not raw_list:
        save_json(PROGRAMS_FILE, SEED_PROGRAMS)
        raw_list = SEED_PROGRAMS
    return [Program.from_dict(item) for item in raw_list]


def save_programs(programs: List[Program]) -> bool:
    """Persist a list of Program objects to programs.json."""
    data = [prg.to_dict() for prg in programs]
    return save_json(PROGRAMS_FILE, data)


def load_customers() -> List[Customer]:
    """Load all customers from customers.json into Customer objects."""
    raw_list = load_json(CUSTOMERS_FILE, default=None)
    if not raw_list:
        save_json(CUSTOMERS_FILE, SEED_CUSTOMERS)
        raw_list = SEED_CUSTOMERS
    return [Customer.from_dict(item) for item in raw_list]


def save_customers(customers: List[Customer]) -> bool:
    """Persist a list of Customer objects to customers.json."""
    data = [cust.to_dict() for cust in customers]
    return save_json(CUSTOMERS_FILE, data)


def load_inquiries() -> List[Inquiry]:
    """Load all inquiries from inquiries.json into Inquiry objects."""
    raw_list = load_json(INQUIRIES_FILE, default=None)
    if not raw_list:
        save_json(INQUIRIES_FILE, SEED_INQUIRIES)
        raw_list = SEED_INQUIRIES
    return [Inquiry.from_dict(item) for item in raw_list]


def save_inquiries(inquiries: List[Inquiry]) -> bool:
    """Persist a list of Inquiry objects to inquiries.json."""
    data = [inq.to_dict() for inq in inquiries]
    return save_json(INQUIRIES_FILE, data)
