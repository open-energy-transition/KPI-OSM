import requests
import pandas as pd
from collections import defaultdict
from haversine import haversine

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
    
    way["power"="line"](area.searchArea)(user_touched:"{user_filter}") -> .user_lines;
    
    (
      .user_lines;
      node(w.user_lines);
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
    nodes = {}
    power_lines = []
    voltage_lengths = defaultdict(float)
    total_length = 0.0
    
    # First pass: collect all nodes
    for element in data.get("elements", []):
        if element["type"] == "node":
            nodes[element["id"]] = (element["lat"], element["lon"])
    
    # Second pass: process power lines
    for element in data.get("elements", []):
        if element["type"] == "way" and element.get("tags", {}).get("power") == "line":
            voltage = element["tags"].get("voltage", "unknown")
            way_nodes = element.get("nodes", [])
            
            # Calculate length of this power line segment
            length_km = 0.0
            for i in range(len(way_nodes) - 1):
                node1 = way_nodes[i]
                node2 = way_nodes[i + 1]
                
                if node1 in nodes and node2 in nodes:
                    coord1 = nodes[node1]
                    coord2 = nodes[node2]
                    length_km += haversine(coord1, coord2)
            
            # Add to totals
            voltage_lengths[voltage] += length_km
            total_length += length_km
            
            power_lines.append({
                "id": element["id"],
                "voltage": voltage,
                "length_km": length_km
            })
    
    return total_length, voltage_lengths, power_lines

# ---------------------- Process Voltage ---------------------- #
def process_voltage(voltage_str):
    """Convert voltage string to a consistent format for grouping"""
    if isinstance(voltage_str, (int, float)):
        return str(voltage_str)
    
    voltage_str = str(voltage_str).strip()
    if voltage_str.lower() in ["unknown", "none", ""]:
        return "unknown"
    
    # Handle combined voltages (take the highest)
    if "/" in voltage_str:
        parts = voltage_str.split("/")
        try:
            max_voltage = max(float(part.strip()) for part in parts)
            return str(int(max_voltage))
        except ValueError:
            return voltage_str
    
    # Try to clean up the voltage string
    try:
        # Remove non-numeric characters except digits and decimal point
        cleaned = ''.join(c for c in voltage_str if c.isdigit() or c in ['.', ','])
        cleaned = cleaned.replace(',', '.')
        return str(int(float(cleaned)))
    except ValueError:
        return voltage_str

# ---------------------- Display Results ---------------------- #
def display_results(total_length, voltage_lengths):
    print(f"\nYou have placed {total_length:.2f} km of power lines")
    
    # Process voltage strings for consistent grouping
    processed_voltages = defaultdict(float)
    for voltage, length in voltage_lengths.items():
        key = process_voltage(voltage)
        processed_voltages[key] += length
    
    # Create and display dataframe
    df = pd.DataFrame(
        [(voltage, f"{length:.2f} km") for voltage, length in processed_voltages.items()],
        columns=["Voltage", "Length"]
    )
    df = df.sort_values(by="Voltage")
    
    print("\nLength by Voltage:")
    print(df.to_string(index=False))

# ---------------------- Main Execution ---------------------- #
if __name__ == "__main__":
    country = input(f"Enter the country name (example: {DEFAULT_COUNTRY}): ") or DEFAULT_COUNTRY
    users = input("Enter OSM usernames separated by commas: ").strip()
    users = [user.strip() for user in users.split(",")] if users else []
    
    print("Fetching data from OSM...")
    osm_data = fetch_osm_data(country, users)
    if osm_data:
        total_length, voltage_lengths, power_lines = process_osm_data(osm_data)
        display_results(total_length, voltage_lengths)
