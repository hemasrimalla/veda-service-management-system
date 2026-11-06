"""
models/inquiry.py
-----------------
Represents customer/service inquiries and requests linked to a customer and
a service or program offered by Veda Technology.

Fields:
    id (str): Unique inquiry identifier (e.g., 'INQ-301').
    customer_id (str): ID of the registered customer (e.g., 'CUST-001').
    customer_name (str): Cached display name of the customer.
    target_type (str): Type of offering requested ('Service' or 'Program').
    target_id (str): ID of the service or program.
    target_name (str): Title/Name of the service or program.
    subject (str): Brief subject line of the inquiry.
    message (str): Detailed request or message notes.
    status (str): Current status ('Open', 'In Progress', 'Resolved', 'Closed').
    priority (str): Priority tier ('Low', 'Medium', 'High', 'Urgent').
    created_date (str): Date the inquiry was logged (YYYY-MM-DD).
"""

from typing import Dict, Any
from datetime import date


class Inquiry:
    """Domain model representing an inquiry or service request."""

    VALID_TARGET_TYPES = ["Service", "Program"]
    VALID_STATUSES = ["Open", "In Progress", "Resolved", "Closed"]
    VALID_PRIORITIES = ["Low", "Medium", "High", "Urgent"]

    def __init__(
        self,
        id: str,
        customer_id: str,
        customer_name: str,
        target_type: str,
        target_id: str,
        target_name: str,
        subject: str,
        message: str,
        status: str = "Open",
        priority: str = "Medium",
        created_date: str = "",
    ) -> None:
        """Initialize an Inquiry instance.

        Args:
            id: Unique inquiry ID.
            customer_id: Linked customer ID.
            customer_name: Customer name.
            target_type: Target category ('Service' or 'Program').
            target_id: Target ID.
            target_name: Target title/name.
            subject: Short description of the inquiry.
            message: Full inquiry details.
            status: Status ('Open', 'In Progress', 'Resolved', 'Closed').
            priority: Priority ('Low', 'Medium', 'High', 'Urgent').
            created_date: Date logged (YYYY-MM-DD). Defaults to today.
        """
        self.id = str(id).strip()
        self.customer_id = str(customer_id).strip()
        self.customer_name = str(customer_name).strip()
        self.target_type = str(target_type).strip().capitalize()
        if self.target_type not in self.VALID_TARGET_TYPES:
            self.target_type = "Service"
        self.target_id = str(target_id).strip()
        self.target_name = str(target_name).strip()
        self.subject = str(subject).strip()
        self.message = str(message).strip()

        # Normalize status
        status_norm = str(status).strip().title()
        self.status = status_norm if status_norm in self.VALID_STATUSES else "Open"

        # Normalize priority
        prio_norm = str(priority).strip().capitalize()
        self.priority = prio_norm if prio_norm in self.VALID_PRIORITIES else "Medium"

        self.created_date = (
            str(created_date).strip() if created_date else date.today().isoformat()
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Inquiry instance to a dictionary for JSON serialization.

        Returns:
            dict: Dictionary representation of the inquiry.
        """
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "target_name": self.target_name,
            "subject": self.subject,
            "message": self.message,
            "status": self.status,
            "priority": self.priority,
            "created_date": self.created_date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Inquiry":
        """Create an Inquiry instance from a dictionary.

        Args:
            data: Dictionary with inquiry attributes.

        Returns:
            Inquiry: Deserialized Inquiry instance.
        """
        return cls(
            id=data.get("id", ""),
            customer_id=data.get("customer_id", data.get("customer", "")),
            customer_name=data.get("customer_name", data.get("customer", "Unknown")),
            target_type=data.get("target_type", "Service"),
            target_id=data.get("target_id", data.get("item_id", "")),
            target_name=data.get("target_name", data.get("interest", "")),
            subject=data.get("subject", "General Inquiry"),
            message=data.get("message", ""),
            status=data.get("status", "Open"),
            priority=data.get("priority", "Medium"),
            created_date=data.get("created_date", data.get("date", date.today().isoformat())),
        )

    def __str__(self) -> str:
        """User-friendly string representation of the inquiry."""
        return (
            f"[{self.id}] {self.subject} | Customer: {self.customer_name} ({self.customer_id}) "
            f"| For: {self.target_type} '{self.target_name}' [{self.target_id}] "
            f"| Priority: {self.priority} | Status: {self.status}"
        )
