"""
models/program.py
-----------------
Represents training, internship, and technology programs offered by Veda Technology.

Fields:
    id (str): Unique program identifier (e.g., 'PRG-201').
    name (str): Program name (e.g., 'Full-Stack Web Development Bootcamp').
    type (str): Type of program ('Training', 'Internship', 'Technology').
    duration (str): Program duration (e.g., '12 Weeks', '6 Months').
    fee (float): Enrollment fee in USD ($). Can be 0.0 for sponsored internships.
    seats (int): Maximum seat capacity.
    start_date (str): Scheduled start date in YYYY-MM-DD format.
    status (str): Operational status ('Active', 'Upcoming', 'Ongoing', 'Closed').
"""

from typing import Dict, Any


class Program:
    """Domain model representing a training or internship program."""

    VALID_TYPES = ["Training", "Internship", "Technology"]
    VALID_STATUSES = ["Active", "Upcoming", "Ongoing", "Completed", "Closed"]

    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        duration: str,
        fee: float,
        seats: int,
        start_date: str,
        status: str = "Active",
    ) -> None:
        """Initialize a Program instance.

        Args:
            id: Unique program ID.
            name: Title or name of the program.
            type: Program category ('Training', 'Internship', 'Technology').
            duration: Duration string (e.g., '8 Weeks').
            fee: Enrollment fee in USD.
            seats: Total available seats.
            start_date: Start date string (YYYY-MM-DD).
            status: Status ('Active', 'Upcoming', etc.).
        """
        self.id = str(id).strip()
        self.name = str(name).strip()
        self.type = str(type).strip().capitalize()
        if self.type not in self.VALID_TYPES:
            self.type = "Training"
        self.duration = str(duration).strip()
        self.fee = float(fee)
        self.seats = int(seats)
        self.start_date = str(start_date).strip()
        self.status = str(status).strip().capitalize()
        if self.status not in self.VALID_STATUSES:
            self.status = "Active"

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Program instance into a dictionary for JSON serialization.

        Returns:
            dict: Dictionary representation of the program.
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "duration": self.duration,
            "fee": round(self.fee, 2),
            "seats": self.seats,
            "start_date": self.start_date,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Program":
        """Create a Program instance from a dictionary.

        Args:
            data: Dictionary with program attributes.

        Returns:
            Program: Deserialized Program instance.
        """
        return cls(
            id=data.get("id", ""),
            name=data.get("name", data.get("title", "")),
            type=data.get("type", "Training"),
            duration=data.get("duration", "4 Weeks"),
            fee=float(data.get("fee", 0.0)),
            seats=int(data.get("seats", 20)),
            start_date=data.get("start_date", "2026-12-01"),
            status=data.get("status", "Active"),
        )

    def __str__(self) -> str:
        """User-friendly string representation of the program."""
        fee_display = f"${self.fee:,.2f}" if self.fee > 0 else "Free/Sponsored"
        return f"[{self.id}] {self.name} | {self.type} ({self.duration}) - {fee_display} - Seats: {self.seats} - Starts: {self.start_date} [{self.status}]"
