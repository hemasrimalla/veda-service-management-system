"""
models/customer.py
------------------
Represents clients, businesses, and student applicants registered with Veda Technology.

Fields:
    id (str): Unique customer identifier (e.g., 'CUST-001').
    name (str): Full name or business contact name.
    email (str): Primary contact email address.
    phone (str): Contact phone number.
    company (str): Company, college, or organization name.
    registered_date (str): Registration date in YYYY-MM-DD format.
"""

from typing import Dict, Any
from datetime import date


class Customer:
    """Domain model representing a customer or student applicant."""

    def __init__(
        self,
        id: str,
        name: str,
        email: str,
        phone: str,
        company: str = "Individual",
        registered_date: str = "",
    ) -> None:
        """Initialize a Customer instance.

        Args:
            id: Unique customer ID.
            name: Full name of customer.
            email: Contact email address.
            phone: Contact phone number.
            company: Company or institution affiliation.
            registered_date: Registration date (YYYY-MM-DD). Defaults to today.
        """
        self.id = str(id).strip()
        self.name = str(name).strip()
        self.email = str(email).strip()
        self.phone = str(phone).strip()
        self.company = str(company).strip() or "Individual"
        self.registered_date = (
            str(registered_date).strip() if registered_date else date.today().isoformat()
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Customer instance to a dictionary for JSON serialization.

        Returns:
            dict: Dictionary representation of the customer.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "registered_date": self.registered_date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Customer":
        """Create a Customer instance from a dictionary.

        Args:
            data: Dictionary with customer attributes.

        Returns:
            Customer: Deserialized Customer instance.
        """
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            company=data.get("company", "Individual"),
            registered_date=data.get("registered_date", date.today().isoformat()),
        )

    def __str__(self) -> str:
        """User-friendly string representation of the customer."""
        return f"[{self.id}] {self.name} ({self.company}) | Email: {self.email} | Phone: {self.phone}"
