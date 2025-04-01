import requests
import pandas as pd
from collections import defaultdict

# ---------------------- Configuration ---------------------- #
DEFAULT_COUNTRY = "Bolivia"  # Change this to your desired country
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# ---------------------- Overpass Query ---------------------- #
def get_overpass_query(country, users):
    user_filter = "\",\"".join(users)  # Format for user_touched filter
    return f"""
    [out:json][timeout:400];
    
    relation["boundary"="administrative"][~"^name(:en)?$"~"^{country}.*", i] -> .admin_boundary;
    .admin_boundary map_to_area -> .searchArea;
    
    node["power"="substation"](area.searchArea) -> .substation_nodes;
    way["power"="substation"](area.searchArea) -> .substation_ways;
    relation["power"="substation"](area.searchArea) -> .substation_relations;
    
    (
      node.substation_nodes(user_touched:"{user_filter}");
      way.substation_ways(user_touched:"{user_filter}");
      relation.substation_relations(user_touched:"{user_filter}");
    );
    
    out body;
    >;
    out skel qt;
    """

# ---------------------- Fetch Data ---------------------- #
def fetch_osm_data(country, users):
    query = get_overpass_query(country, users)
    response = requests.get(OVERPASS_URL, params={"data": query})
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data:", response.status_code)
        return None

# ---------------------- Process Data ---------------------- #
def process_osm_data(data):
    substations = {}
    substation_voltages = defaultdict(int)
    
    # Extract substations (nodes, ways, and relations)
    for element in data.get("elements", []):
        if "power" in element.get("tags", {}) and element["tags"]["power"] == "substation":
            substations[element["id"]] = element  # Store substations by ID
    
    total_substations = len(substations)  # Count total substations
    print(f"Total substations: {total_substations}")  # Display total count
    
    # Process voltages
    for substation in substations.values():
        voltage = substation.get("tags", {}).get("voltage", None)
        if voltage:
            voltage_levels = process_voltage(voltage)
            substation_voltages[voltage_levels] += 1
    
    return substation_voltages

# ---------------------- Process Voltage ---------------------- #
def process_voltage(voltage):
    voltage = str(voltage).strip()
    if "/" in voltage:  # Handle combined voltages (e.g., 230000/115000)
        parts = voltage.split("/")
        return max(float(part) for part in parts) / 1000  # Take the largest and convert to kV
    elif ";" in voltage:  # Handle voltages separated by semicolons
        parts = voltage.split(";")
        return max(float(part) for part in parts) / 1000  # Take the largest and convert to kV
    else:
        return float(voltage) / 1000  # Convert to kV


# ---------------------- Display Results ---------------------- #
def display_results(substation_voltages):
    df = pd.DataFrame(list(substation_voltages.items()), columns=["Voltage (kV)", "Number of Substations"])
    df = df.sort_values(by="Voltage (kV)")
    print("\nVoltage Distribution of Substations:")
    print(df.to_string(index=False))

# ---------------------- Main Execution ---------------------- #
if __name__ == "__main__":
    country = input(f"Enter the country name (default: {DEFAULT_COUNTRY}): ") or DEFAULT_COUNTRY
    users = input("Enter OSM usernames separated by commas: ").strip()
    users = [user.strip() for user in users.split(",")] if users else []
    
    print("Fetching data from OSM...")
    osm_data = fetch_osm_data(country, users)
    if osm_data:
        substation_voltages = process_osm_data(osm_data)
        display_results(substation_voltages)
