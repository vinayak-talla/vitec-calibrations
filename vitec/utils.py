import json
from pathlib import Path

DATA_FILE_PATH = Path(__file__).resolve().parent.parent / "data" / "types.json"

def get_dropdown_options(key):
    """Retrieve options for a specific dropdown."""
    with open(DATA_FILE_PATH, "r") as file:
        data = json.load(file)
    return data.get(key, [])

def add_dropdown_option(key, new_option):
    """Add a new option to a specific dropdown."""
    with open(DATA_FILE_PATH, "r+") as file:
        data = json.load(file)

        # Ensure the key exists in the JSON file
        if key not in data:
            data[key] = []

        # Add the new option if it doesn't already exist
        if new_option not in data[key]:
            data[key].append(new_option)
            file.seek(0)  # Go back to the start of the file
            json.dump(data, file, indent=4)
            file.truncate()
            return True  # Indicate success
        return False  # Indicate duplicate

def load_instrument_types():
    """Load instrument types from the JSON file."""
    try:
        with open(DATA_FILE_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"pipette_types": [], "rpm_types": [], "temperature_types": []}  # Default empty structure