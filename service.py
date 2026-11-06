"""
models/service.py
-----------------
Represents digital and IT services offered by Veda Technology.

Fields:
    id (str): Unique service identifier (e.g., 'SRV-101').
    name (str): Service name (e.g., 'Full-Stack Web Development').
    category (str): Service category (e.g., 'Web Development', 'Cloud Consulting').
    description (str): Detailed scope of the service.
    price (float): Base or starting price in USD ($).
    status (str): Operational status ('Active' or 'Inactive').
"""

from typing import Dict, Any


class Service:
    """Domain model representing a digital/IT service."""

    VALID_STATUSES = ["Active", "Inactive"]

    def __init__(
        self,
        id: str,
        name: str,
        category: str,
        description: str,
        price: float,
        status: str = "Active",
    ) -> None:
        """Initialize a Service instance.

        Args:
            id: Unique service ID.
            name: Title or name of the service.
            category: Service category.
            description: Description of the service.
            price: Service pricing in USD.
            status: Status ('Active' or 'Inactive').
        """
        self.id = str(id).strip()
        self.name = str(name).strip()
        self.category = str(category).strip()
        self.description = str(description).strip()
        self.price = float(price)
        self.status = str(status).strip().capitalize()
        if self.status not in self.VALID_STATUSES:
            self.status = "Active"

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Service instance into a dictionary for JSON serialization.

        Returns:
            dict: Dictionary representation of the service.
        """
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "price": round(self.price, 2),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Service":
        """Create a Service instance from a dictionary.

        Args:
            data: Dictionary with service attributes.

        Returns:
            Service: Deserialized Service instance.
        """
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            category=data.get("category", "General"),
            description=data.get("description", ""),
            price=float(data.get("price", 0.0)),
            status=data.get("status", "Active"),
        )

    def __str__(self) -> str:
        """User-friendly string representation of the service."""
        return f"[{self.id}] {self.name} ({self.category}) - ${self.price:,.2f} [{self.status}]"
