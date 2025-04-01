import requests
import pandas as pd
import re

# ---------------------- Configuration ---------------------- #
DEFAULT_COUNTRY = "Bolivia"  # Change this to your desired country
DEFAULT_USERS = ["Andreas Hernandez", "Tobias Augspurger"]  # Add or remove users as needed

# ---------------------- Overpass API Query ---------------------- #
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def get_overpass_query(country, users):
    user_filter = "\",\"".join(users)  # Format for user_touched filter
    return f"""
    [out:json][timeout:400];
    
    relation["boundary"="administrative"][~"^name(:en)?$"~"{country}", i] -> .admin_boundary;
    .admin_boundary map_to_area -> .searchArea;
    
    node["power"="plant"](user_touched:"{user_filter}")(area.searchArea) -> .plant_nodes;
    way["power"="plant"](user_touched:"{user_filter}")(area.searchArea) -> .plant_ways;
    relation["power"="plant"](user_touched:"{user_filter}")(area.searchArea) -> .plant_relations;
    
    (
      .plant_nodes;
      .plant_ways;
      .plant_relations;
    );
    
    out body;
    >;
    out skel qt;
    """

def fetch_osm_data(country, users):
    query = get_overpass_query(country, users)
    response = requests.get(OVERPASS_URL, params={"data": query})
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data:", response.status_code)
        return None

def convert_to_mw(value):
    value = str(value).strip().lower()
    match = re.match(r"(\d+(?:\.\d+)?)([a-z]*)", value)
    if match:
        num, unit = match.groups()
        num = float(num)
        if "kw" in unit:
            return num / 1000
        elif "gw" in unit:
            return num * 1000
        else:
            return num  # Assume MW
    return 0

def process_osm_data(data):
    total_capacity = 0
    if "elements" in data:
        for element in data["elements"]:
            if "tags" in element and "plant:output:electricity" in element["tags"]:
                total_capacity += convert_to_mw(element["tags"]["plant:output:electricity"])
    return total_capacity

def main():
    country = input(f"Enter the country name (Example: {DEFAULT_COUNTRY}): ") or DEFAULT_COUNTRY
    users = input(f"Enter user names separated by commas (default: {', '.join(DEFAULT_USERS)}): ")
    users = [user.strip() for user in users.split(",")] if users else DEFAULT_USERS
    
    print("Fetching data from OSM...")
    osm_data = fetch_osm_data(country, users)
    if not osm_data:
        return
    
    total_user_capacity = process_osm_data(osm_data)
    print(f"Total capacity added by users: {total_user_capacity:.2f} MW")
    
    total_country_capacity = input("Enter the total MW capacity of the country from OpenInfraMap: ")
    total_country_capacity = convert_to_mw(total_country_capacity)
    
    if total_country_capacity > 0:
        percentage = (total_user_capacity / total_country_capacity) * 100
        print(f"\nUsers have mapped {percentage:.2f}% of the total country capacity.")
    else:
        print("\nInvalid total capacity input.")

if __name__ == "__main__":
    main()
