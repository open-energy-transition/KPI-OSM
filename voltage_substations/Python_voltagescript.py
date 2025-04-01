import requests
import pandas as pd
import re
from collections import defaultdict
 
# ---------------------- Configuration ---------------------- #
 
DEFAULT_COUNTRY = "Bolivia"  # Change this to your desired country
 
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
 
# ---------------------- Overpass Query ---------------------- #
 
def get_overpass_query(country, users):
 
    user_filter = "\",\"".join(users)  # Format for user_touched filter
 
    return f"""
    [out:json][timeout:400]; 
    relation["boundary"="administrative"][~"^name(:en)?$"~"{country}", i] -> .admin_boundary;
    .admin_boundary map_to_area -> .searchArea;
 
    node["power"="tower"](area.searchArea) -> .towers;
    node["power"="pole"](area.searchArea) -> .poles;
    way["power"="line"](area.searchArea)(bn.towers) -> .lines_connected;
    way["power"="line"]["voltage"](if:t["voltage"] >= 90000)(area.searchArea) -> .high_voltage_lines;
    node.poles(w.high_voltage_lines) -> .hv_poles;
 
    (
      node.towers(user_touched:"{user_filter}");
      node.hv_poles(user_touched:"{user_filter}");
    ) -> .my_nodes;
  
    way["power"="line"](bn.my_nodes) -> .connected_ways;
 
    (
      .my_nodes;
      .connected_ways;
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
 
    towers = {}
 
    tower_voltages = defaultdict(int)

    for element in data.get("elements", []):
 
        if element["type"] == "node" and "power" in element.get("tags", {}):
 
            if element["tags"]["power"] in ["tower", "pole"]:
 
                towers[element["id"]] = element  # Store towers and HV poles by node ID
 

 
    total_towers_poles = len(towers)  # Count total towers and poles
 
    print(f"Total towers and poles: {total_towers_poles}")  # Display total count
 

 
    counted_towers = set()
 

 
    for element in data.get("elements", []):
 
        if element["type"] == "way" and "power" in element.get("tags", {}):
 
            voltage = element["tags"].get("voltage", None)
 
            if voltage:
 
                voltage_levels = process_voltage(voltage)
 
                for node_id in element.get("nodes", []):  # Assign voltage to towers and poles in the way
 
                    if node_id in towers and node_id not in counted_towers:
 
                        tower_voltages[voltage_levels] += 1
 
                        counted_towers.add(node_id)  # Mark this tower/pole as counted
 
 
    return tower_voltages
 
 
# ---------------------- Process Voltage ---------------------- #
 
def process_voltage(voltage):
 
    voltage = str(voltage).strip()
 
    if "/" in voltage:  # Handle combined voltages (e.g., 230000/115000)
 
        parts = voltage.split("/")
 
        return max(float(part) for part in parts) / 1000  # Take the largest and convert to kV
 
    else:
 
        return float(voltage) / 1000  # Convert to kV
 

 
# ---------------------- Display Results ---------------------- #
 
def display_results(tower_voltages):
 
    df = pd.DataFrame(list(tower_voltages.items()), columns=["Voltage (kV)", "Number of Towers/Poles"])
 
    df = df.sort_values(by="Voltage (kV)")
 
    print("\nVoltage Distribution of Towers and HV Poles:")
 
    print(df.to_string(index=False))
 
 
# ---------------------- Main Execution ---------------------- #
 
if __name__ == "__main__":

    country = input(f"Enter the country name (Example: {DEFAULT_COUNTRY}): ") or DEFAULT_COUNTRY
 
    users = input("Enter OSM username(s) (Example: Andreas Hernandez, Mwiche): ").strip()
 
    users = [user.strip() for user in users.split(",")] if users else []
 
 
    print("Fetching data from OSM...")
 
    osm_data = fetch_osm_data(country, users)
 
    if osm_data:
 
        tower_voltages = process_osm_data(osm_data)
 
        display_results(tower_voltages)
