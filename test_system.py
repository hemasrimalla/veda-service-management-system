"""
test_system.py
--------------
Automated test suite verifying all models, modules, CRUD operations,
data persistence, validators, search filters, and business reports
for the Veda Technology Business & Service Management System.

Run:
    python test_system.py
"""

import sys
import os
import unittest
from datetime import date

# Ensure project root is in the path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models.service import Service
from models.program import Program
from models.customer import Customer
from models.inquiry import Inquiry
from modules import storage
from modules import validators
from modules import service_manager
from modules import program_manager
from modules import inquiry_manager
from modules import search_filter
from modules import reports


class TestVedaSystem(unittest.TestCase):
    """Comprehensive test cases for Veda Management System."""

    def setUp(self):
        """Prepare fresh mock data before each test."""
        self.sample_service = Service(
            id="TEST-SRV",
            name="Cloud Security Architecture",
            category="Cloud Consulting",
            description="Enterprise cloud security review and penetration audit.",
            price=3500.0,
            status="Active",
        )
        self.sample_program = Program(
            id="TEST-PRG",
            name="Applied AI Engineering",
            type="Training",
            duration="8 Weeks",
            fee=1250.0,
            seats=20,
            start_date="2026-12-01",
            status="Active",
        )
        self.sample_customer = Customer(
            id="TEST-CUST",
            name="Alice Smith",
            email="alice@innovate.co",
            phone="+1-555-0199",
            company="Innovate Labs",
            registered_date="2026-11-01",
        )
        self.sample_inquiry = Inquiry(
            id="TEST-INQ",
            customer_id="TEST-CUST",
            customer_name="Alice Smith",
            target_type="Service",
            target_id="TEST-SRV",
            target_name="Cloud Security Architecture",
            subject="Cloud Security Project Quote",
            message="Need security hardening for AWS workloads.",
            status="Open",
            priority="High",
            created_date="2026-11-05",
        )

    # --------------------------------------------------------------------------
    # 1. MODELS TESTS
    # --------------------------------------------------------------------------

    def test_service_model(self):
        """Test Service serialization and deserialization."""
        d = self.sample_service.to_dict()
        self.assertEqual(d["id"], "TEST-SRV")
        self.assertEqual(d["price"], 3500.0)

        restored = Service.from_dict(d)
        self.assertEqual(restored.id, "TEST-SRV")
        self.assertEqual(restored.name, "Cloud Security Architecture")
        self.assertIn("Cloud Security Architecture", str(restored))

    def test_program_model(self):
        """Test Program serialization and deserialization."""
        d = self.sample_program.to_dict()
        self.assertEqual(d["id"], "TEST-PRG")
        self.assertEqual(d["seats"], 20)
        self.assertEqual(d["start_date"], "2026-12-01")

        restored = Program.from_dict(d)
        self.assertEqual(restored.id, "TEST-PRG")
        self.assertEqual(restored.fee, 1250.0)
        self.assertIn("Applied AI Engineering", str(restored))

    def test_customer_model(self):
        """Test Customer serialization and deserialization."""
        d = self.sample_customer.to_dict()
        self.assertEqual(d["id"], "TEST-CUST")
        self.assertEqual(d["company"], "Innovate Labs")

        restored = Customer.from_dict(d)
        self.assertEqual(restored.id, "TEST-CUST")
        self.assertEqual(restored.email, "alice@innovate.co")
        self.assertIn("Alice Smith", str(restored))

    def test_inquiry_model(self):
        """Test Inquiry serialization and deserialization."""
        d = self.sample_inquiry.to_dict()
        self.assertEqual(d["id"], "TEST-INQ")
        self.assertEqual(d["priority"], "High")
        self.assertEqual(d["status"], "Open")

        restored = Inquiry.from_dict(d)
        self.assertEqual(restored.id, "TEST-INQ")
        self.assertEqual(restored.target_name, "Cloud Security Architecture")
        self.assertIn("TEST-INQ", str(restored))

    # --------------------------------------------------------------------------
    # 2. VALIDATORS TESTS
    # --------------------------------------------------------------------------

    def test_validators(self):
        """Test all input validation functions."""
        # Non-empty
        self.assertEqual(validators.validate_non_empty("  Valid Text  "), "Valid Text")
        with self.assertRaises(ValueError):
            validators.validate_non_empty("   ")

        # Positive numbers
        self.assertEqual(validators.validate_positive_number("120.50", is_float=True), 120.50)
        self.assertEqual(validators.validate_positive_number("25", is_float=False), 25)
        with self.assertRaises(ValueError):
            validators.validate_positive_number("-10", allow_zero=False)
        with self.assertRaises(ValueError):
            validators.validate_positive_number("abc")

        # Dates
        self.assertEqual(validators.validate_date("2026-12-31"), "2026-12-31")
        with self.assertRaises(ValueError):
            validators.validate_date("invalid-date")
        with self.assertRaises(ValueError):
            validators.validate_date("31-12-2026")

        # Choices
        self.assertEqual(validators.validate_choice("open", ["Open", "Closed"]), "Open")
        with self.assertRaises(ValueError):
            validators.validate_choice("Pending", ["Open", "Closed"])

        # Unique IDs
        existing = ["SRV-101", "SRV-102"]
        self.assertEqual(validators.validate_unique_id("SRV-103", existing), "SRV-103")
        with self.assertRaises(ValueError):
            validators.validate_unique_id("srv-101", existing)

    # --------------------------------------------------------------------------
    # 3. STORAGE & SEED DATA TESTS
    # --------------------------------------------------------------------------

    def test_storage_loaders(self):
        """Verify data files load properly and seed at least 5 records."""
        storage.initialize_storage()

        services = storage.load_services()
        self.assertGreaterEqual(len(services), 5)
        self.assertIsInstance(services[0], Service)

        programs = storage.load_programs()
        self.assertGreaterEqual(len(programs), 5)
        self.assertIsInstance(programs[0], Program)

        customers = storage.load_customers()
        self.assertGreaterEqual(len(customers), 5)
        self.assertIsInstance(customers[0], Customer)

        inquiries = storage.load_inquiries()
        self.assertGreaterEqual(len(inquiries), 5)
        self.assertIsInstance(inquiries[0], Inquiry)

    def test_storage_error_resilience(self):
        """Ensure corrupted or missing files do not crash the application."""
        corrupted_path = os.path.join(storage.DATA_DIR, "_corrupted_test.json")
        try:
            with open(corrupted_path, "w", encoding="utf-8") as f:
                f.write("{ INVALID JSON CONTENT :::")

            loaded = storage.load_json(corrupted_path, default=[])
            self.assertEqual(loaded, [])
        finally:
            if os.path.exists(corrupted_path):
                os.remove(corrupted_path)

    # --------------------------------------------------------------------------
    # 4. LOOKUP & CRUD TESTS
    # --------------------------------------------------------------------------

    def test_service_lookup_and_crud(self):
        """Test service find by ID and list manipulation."""
        services = [self.sample_service]
        found = service_manager.find_service_by_id(services, "test-srv")
        self.assertIsNotNone(found)
        self.assertEqual(found.id, "TEST-SRV")

        not_found = service_manager.find_service_by_id(services, "UNKNOWN")
        self.assertIsNone(not_found)

    def test_program_lookup_and_crud(self):
        """Test program lookup by ID."""
        programs = [self.sample_program]
        found = program_manager.find_program_by_id(programs, "test-prg")
        self.assertIsNotNone(found)
        self.assertEqual(found.id, "TEST-PRG")

    def test_customer_and_inquiry_lookup(self):
        """Test customer and inquiry lookup functions."""
        customers = [self.sample_customer]
        inquiries = [self.sample_inquiry]

        c_found = inquiry_manager.find_customer_by_id(customers, "test-cust")
        self.assertIsNotNone(c_found)
        self.assertEqual(c_found.email, "alice@innovate.co")

        i_found = inquiry_manager.find_inquiry_by_id(inquiries, "test-inq")
        self.assertIsNotNone(i_found)
        self.assertEqual(i_found.status, "Open")

    # --------------------------------------------------------------------------
    # 5. REPORTS TESTS
    # --------------------------------------------------------------------------

    def test_reports_generation(self):
        """Verify that all report generator functions produce rich formatted text."""
        services = [self.sample_service]
        programs = [self.sample_program]
        customers = [self.sample_customer]
        inquiries = [self.sample_inquiry]

        summary = reports.generate_executive_summary(services, programs, customers, inquiries)
        self.assertIn("EXECUTIVE BUSINESS SUMMARY", summary)
        self.assertIn("Total Digital Services Catalog :    1", summary)

        status_rep = reports.generate_inquiry_status_report(inquiries)
        self.assertIn("INQUIRY DISTRIBUTION BY STATUS", status_rep)
        self.assertIn("Open", status_rep)

        demand_rep = reports.generate_demand_ranking_report(inquiries)
        self.assertIn("DEMAND ANALYSIS", demand_rep)
        self.assertIn("Cloud Security Architecture", demand_rep)

        revenue_rep = reports.generate_program_revenue_report(programs)
        self.assertIn("PROGRAM CAPACITY & PROJECTED REVENUE", revenue_rep)
        # 20 seats * 1250 fee = 25,000
        self.assertIn("25,000.00", revenue_rep)


if __name__ == "__main__":
    print("\nRunning automated tests for Veda Technology System...\n")
    unittest.main(verbosity=2)
