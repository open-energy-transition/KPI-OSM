import requests
import pandas as pd
from haversine import haversine

# ---------------------- Configuration ---------------------- #
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# ---------------------- Overpass Query ---------------------- #
def get_overpass_query(country, username):
    return f"""
    [out:json][timeout:400];

    relation["boundary"="administrative"][~"^name(:en)?$"~"{country}", i] -> .admin_boundary;
    .admin_boundary map_to_area -> .searchArea;

    way["power"="line"](area.searchArea) -> .lines;
    way["power"="cable"](area.searchArea) -> .cables;

    (
      way.lines(user_touched:"{username}");
      way.cables(user_touched:"{username}");
    );

    out body;
    >;
    out skel qt;
    """

# ---------------------- Fetch Data ---------------------- #
def fetch_osm_data(country, username):
    query = get_overpass_query(country, username)
    response = requests.get(OVERPASS_URL, params={"data": query})
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data:", response.status_code)
        return None

# ---------------------- Calculate Distance ---------------------- #
def calculate_total_length(data):
    nodes = {}
    total_length = 0.0
    
    # Collect all node coordinates
    for element in data.get("elements", []):
        if element["type"] == "node":
            nodes[element["id"]] = (element["lat"], element["lon"])

    # Calculate total length
    for element in data.get("elements", []):
        if element["type"] == "way":
            way_nodes = element.get("nodes", [])
            
            way_length = 0.0
            for i in range(len(way_nodes) - 1):
                node1, node2 = way_nodes[i], way_nodes[i + 1]
                if node1 in nodes and node2 in nodes:
                    coord1, coord2 = nodes[node1], nodes[node2]
                    way_length += haversine(coord1, coord2)

            total_length += way_length

    return total_length

# ---------------------- Main Execution ---------------------- #
if __name__ == "__main__":
    country = input("Enter the country name (e.g., Nepal): ").strip()
    username = input("Enter the OSM username: ").strip()
    
    print("\nFetching data from Overpass API...")
    osm_data = fetch_osm_data(country, username)
    
    if osm_data:
        total_km = calculate_total_length(osm_data)
        print(f"\nTotal mapped power lines and cables by {username} in {country}: {total_km:.2f} km")
