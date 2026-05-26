TYPES = [
    "Developer",
    "Contractor",
    "Consultant",
    "General Planner",
    "Freelancer",
    "Housing Association",
    "Prefab Manufacturer",
    "Steel Manufacturer",
    "Software Company",
]

SERVICES = [
    "Architectural",
    "Structural",
    "MEP",
    "Civil",
    "Geotechnical",
    "Energy Consulting",
    "Scan to BIM",
    "Timber Construction",
    "Steel Construction",
    "Facade",
    "Infra",
    "Building",
    "Industrial",
    "Data Center",
]

COLUMNS = [
    "Company Name",
    "Street",
    "City",
    "Zip",
    "Website",
    "Phone",
    "E-Mail",
    "Contact Person",
    "Position",
    "Contact Email",
    "Contact Phone",
    "Note / Category",
]

HIGHLIGHT_COLUMNS = {"Website", "E-Mail"}

NA_VALUE = "n.a"


def is_valid_note(value: str) -> bool:
    """Return True if value is a valid 'type, service' or 'n.a, n.a'."""
    if value == f"{NA_VALUE}, {NA_VALUE}":
        return True
    parts = [p.strip() for p in value.split(",", 1)]
    if len(parts) != 2:
        return False
    return parts[0] in TYPES and parts[1] in SERVICES
