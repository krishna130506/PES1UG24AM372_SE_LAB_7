"""Elevator request parsing and input validation utilities."""
import re


def _require_string(value, field_name):
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    return value


def _parse_integer(value, field_name):
    if not re.fullmatch(r"[+-]?\d+", value.strip()):
        raise ValueError(f"{field_name} must be a valid integer")
    return int(value.strip())


def parse_request(text):
    """Parse FROM->TO and return a pair of non-negative floor numbers."""
    text = _require_string(text, "Request")
    if text.count("->") != 1:
        raise ValueError("Request must contain exactly one '->' separator")
    start_text, end_text = (part.strip() for part in text.split("->"))
    start = _parse_integer(start_text, "Start floor")
    end = _parse_integer(end_text, "Destination floor")
    if start < 0 or end < 0:
        raise ValueError("Floor numbers must be non-negative")
    return start, end


def total_travel(floors_csv):
    """Calculate total absolute travel distance from a comma-separated floor list."""
    floors_csv = _require_string(floors_csv, "Floor list")
    parts = [part.strip() for part in floors_csv.split(",")]
    if any(not part for part in parts):
        raise ValueError("Floor list must not contain empty entries")
    floors = [_parse_integer(part, "Floor") for part in parts]
    if any(floor < 0 for floor in floors):
        raise ValueError("Floor numbers must be non-negative")
    return sum(abs(floors[i + 1] - floors[i]) for i in range(len(floors) - 1))


def load_percent(text):
    """Calculate the integer load percentage from 'X of Y'."""
    text = _require_string(text, "Load")
    if text.count(" of ") != 1:
        raise ValueError("Load must use the format 'X of Y'")
    load_text, capacity_text = (part.strip() for part in text.split(" of "))
    load = _parse_integer(load_text, "Load")
    capacity = _parse_integer(capacity_text, "Capacity")
    if load < 0:
        raise ValueError("Load must be non-negative")
    if capacity <= 0:
        raise ValueError("Capacity must be greater than zero")
    if load > capacity:
        raise ValueError("Load cannot exceed capacity")
    return load * 100 // capacity


def main():
    print("==== Running parse_request ====")
    try:
        request = input("Enter a request as FROM->TO (e.g. 5->9): ")
        print("From and To:", parse_request(request))
        print("\n==== Running total_travel ====")
        floors = input("Enter floors visited as CSV (e.g. 1,5,3,9): ")
        print("Floors Travelled:", total_travel(floors))
        print("\n==== Running load_percent ====")
        load = input("Enter load as 'X of Y' (e.g. 450 of 630): ")
        print("Load Percent:", load_percent(load))
    except ValueError as error:
        print(f"Invalid input: {error}")


if __name__ == "__main__":
    main()
