"""
modules/validators.py
---------------------
Reusable validation and interactive prompting utilities for CLI input.

Functions include:
- Validating non-empty strings, positive floats/ints, dates, and choices.
- Preventing duplicate IDs.
- Robust user input loops with retry mechanisms and default value support.
"""

from typing import List, Optional, Any
from datetime import datetime


def validate_non_empty(value: str, field_name: str = "Field") -> str:
    """Validate that a string is not empty or composed solely of whitespace.

    Args:
        value: Input string to validate.
        field_name: Label used in error message.

    Returns:
        str: Trimmed string if valid.

    Raises:
        ValueError: If value is blank.
    """
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty.")
    return cleaned


def validate_positive_number(
    value: Any,
    field_name: str = "Number",
    is_float: bool = True,
    allow_zero: bool = True,
) -> float:
    """Validate that a value is a valid non-negative or strictly positive number.

    Args:
        value: Raw input (str or numeric).
        field_name: Label used in error message.
        is_float: True for float, False for int.
        allow_zero: Whether zero is an acceptable value.

    Returns:
        float or int: Validated numeric value.

    Raises:
        ValueError: If parsing fails or number is negative.
    """
    try:
        num = float(value) if is_float else int(value)
    except (ValueError, TypeError):
        expected = "decimal number" if is_float else "integer"
        raise ValueError(f"{field_name} must be a valid {expected}.")

    if allow_zero and num < 0:
        raise ValueError(f"{field_name} cannot be negative.")
    if not allow_zero and num <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")

    return num


def validate_date(date_str: str, field_name: str = "Date") -> str:
    """Validate that a date string follows YYYY-MM-DD format.

    Args:
        date_str: Input date string.
        field_name: Label used in error message.

    Returns:
        str: Cleaned date string.

    Raises:
        ValueError: If date format or calendar date is invalid.
    """
    cleaned = date_str.strip()
    try:
        parsed = datetime.strptime(cleaned, "%Y-%m-%d")
        return parsed.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"{field_name} must follow YYYY-MM-DD format (e.g., 2026-12-01).")


def validate_choice(value: str, allowed_choices: List[str], field_name: str = "Choice") -> str:
    """Validate that a string matches one of the allowed choices (case-insensitive).

    Args:
        value: Raw user input.
        allowed_choices: List of valid options.
        field_name: Label used in error message.

    Returns:
        str: Correctly cased choice from allowed_choices.

    Raises:
        ValueError: If value does not match any choice.
    """
    cleaned = value.strip().lower()
    for choice in allowed_choices:
        if cleaned == choice.lower():
            return choice
    allowed_str = ", ".join(allowed_choices)
    raise ValueError(f"Invalid {field_name}. Allowed options: {allowed_str}")


def validate_unique_id(new_id: str, existing_ids: List[str], entity_name: str = "Record") -> str:
    """Ensure the ID does not already exist in the collection.

    Args:
        new_id: Proposed new ID.
        existing_ids: List of currently assigned IDs.
        entity_name: Name of the entity type.

    Returns:
        str: Validated uppercase ID.

    Raises:
        ValueError: If ID is already taken.
    """
    cleaned = new_id.strip().upper()
    existing_upper = [str(x).strip().upper() for x in existing_ids]
    if cleaned in existing_upper:
        raise ValueError(f"{entity_name} with ID '{cleaned}' already exists. Please use a unique ID.")
    return cleaned


# ==============================================================================
# INTERACTIVE CLI PROMPT HELPERS
# ==============================================================================

def prompt_string(
    prompt_text: str,
    allow_empty: bool = False,
    default: str = "",
) -> str:
    """Interactively prompt user for a string with validation loop."""
    while True:
        display_prompt = f"{prompt_text} [{default}]: " if default else f"{prompt_text}: "
        try:
            val = input(display_prompt).strip()
            if not val:
                if default:
                    return default
                if allow_empty:
                    return ""
                print("  [!] Input cannot be blank. Please try again.")
                continue
            return val
        except (KeyboardInterrupt, EOFError):
            print("\n  [!] Operation cancelled.")
            return default


def prompt_number(
    prompt_text: str,
    is_float: bool = True,
    allow_zero: bool = True,
    default: Optional[Any] = None,
) -> Any:
    """Interactively prompt user for a positive number with validation loop."""
    while True:
        display_prompt = f"{prompt_text} [{default}]: " if default is not None else f"{prompt_text}: "
        try:
            val = input(display_prompt).strip()
            if not val and default is not None:
                return default
            num = validate_positive_number(val, prompt_text, is_float=is_float, allow_zero=allow_zero)
            return num
        except ValueError as err:
            print(f"  [!] {err}")
        except (KeyboardInterrupt, EOFError):
            print("\n  [!] Operation cancelled.")
            return default or 0


def prompt_date(
    prompt_text: str,
    default: Optional[str] = None,
) -> str:
    """Interactively prompt user for a date (YYYY-MM-DD) with validation loop."""
    while True:
        display_prompt = f"{prompt_text} [{default}]: " if default else f"{prompt_text}: "
        try:
            val = input(display_prompt).strip()
            if not val and default:
                return default
            return validate_date(val, prompt_text)
        except ValueError as err:
            print(f"  [!] {err}")
        except (KeyboardInterrupt, EOFError):
            print("\n  [!] Operation cancelled.")
            return default or ""


def prompt_choice(
    prompt_text: str,
    choices: List[str],
    default: Optional[str] = None,
) -> str:
    """Interactively prompt user to pick from a list of valid choices."""
    choices_str = "/".join(choices)
    while True:
        display_prompt = f"{prompt_text} ({choices_str}) [{default}]: " if default else f"{prompt_text} ({choices_str}): "
        try:
            val = input(display_prompt).strip()
            if not val and default:
                return default
            return validate_choice(val, choices, prompt_text)
        except ValueError as err:
            print(f"  [!] {err}")
        except (KeyboardInterrupt, EOFError):
            print("\n  [!] Operation cancelled.")
            return default or choices[0]


def prompt_confirm(prompt_text: str, default_yes: bool = True) -> bool:
    """Interactively ask user for a Yes/No confirmation."""
    options = "Y/n" if default_yes else "y/N"
    try:
        val = input(f"{prompt_text} ({options}): ").strip().lower()
        if not val:
            return default_yes
        return val in ["y", "yes"]
    except (KeyboardInterrupt, EOFError):
        return False
