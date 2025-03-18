import requests
import pandas as pd
from collections import defaultdict

# ---------------------- Overpass API Query ---------------------- #
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
COUNTRY = "Bolivia"  # Replace with actual country name

OVERPASS_QUERY = f"""
[out:json][timeout:400];

// Define the area of interest
relation["boundary"="administrative"]["name"~"{COUNTRY}"] -> .admin_boundary;
.admin_boundary map_to_area -> .searchArea;

// Find all power towers within the administrative boundary
node["power"="tower"](area.searchArea) -> .towers;

// Find all power poles within the administrative boundary
node["power"="pole"](area.searchArea) -> .poles;

// Find all power lines that are connected to towers within the administrative boundary
way["power"="line"](area.searchArea)(bn.towers) -> .lines_connected;

// Find all high-voltage power lines (>= 90 kV) within the administrative boundary
way["power"="line"]["voltage"](if:t["voltage"] >= 90000)(area.searchArea) -> .high_voltage_lines;

// Find only poles that are part of high-voltage lines within the administrative boundary
node.poles(w.high_voltage_lines) -> .hv_poles;

// Combine all towers and poles created by Andreas or Tobias
(
  node.towers(user_touched:"Andreas Hernandez");
  node.towers(user_touched:"Tobias Augspurger");
  node.hv_poles(user_touched:"Andreas Hernandez");
  node.hv_poles(user_touched:"Tobias Augspurger");
) -> .my_nodes;

// Fetch all ways connected to your nodes, regardless of who last edited them
way["power"="line"](bn.my_nodes) -> .connected_ways;

// Combine all relevant results
(
  .my_nodes;
  .connected_ways;
);

out body;
>;
out skel qt;
"""
# ---------------------- Fetch Data from Overpass API ---------------------- #
def fetch_data():
    response = requests.get(OVERPASS_URL, params={"data": OVERPASS_QUERY})
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data:", response.status_code)
        return None

# ---------------------- Process Data ---------------------- #
def process_data(data):
    towers = {}
    tower_voltages = defaultdict(int)
    
    # Extract towers and high-voltage poles (nodes)
    for element in data['elements']:
        if element['type'] == 'node' and 'power' in element.get('tags', {}):
            if element['tags']['power'] in ['tower', 'pole']:
                towers[element['id']] = element  # Store towers and HV poles by node ID
    
    total_towers_poles = len(towers)  # Count total towers and poles
    print(f"Total towers and poles: {total_towers_poles}")  # Display total count
    
    # Track which towers/poles have been counted
    counted_towers = set()
    
    # Extract power lines and assign voltages
    for element in data['elements']:
        if element['type'] == 'way' and 'power' in element.get('tags', {}):
            voltage = element['tags'].get('voltage', None)
            if voltage:
                voltage_levels = process_voltage(voltage)
                for node_id in element.get('nodes', []):  # Assign voltage to towers and poles in the way
                    if node_id in towers and node_id not in counted_towers:
                        tower_voltages[voltage_levels] += 1
                        counted_towers.add(node_id)  # Mark this tower/pole as counted
    
    return tower_voltages

# ---------------------- Process Voltage ---------------------- #
def process_voltage(voltage):
    """Converts voltage string to max kV value."""
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

if __name__ == "__main__":
    data = fetch_data()
    if data:
        tower_voltages = process_data(data)
        display_results(tower_voltages)
