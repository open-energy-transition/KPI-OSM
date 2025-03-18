[out:json][timeout:400];

node["place"~"country|state|province"]({{bbox}}) -> .places;

relation["boundary"="administrative"]["admin_level"="2"](bn.places) -> .admin_boundary;

.admin_boundary map_to_area -> .searchArea;

// Map the relation to an area
.admin_boundary map_to_area -> .searchArea;


// Find all power towers within the administrative boundary
node["power"="tower"](area.searchArea) -> .towers;


// Find all power poles within the administrative boundary
node["power"="pole"](area.searchArea) -> .poles;

// Find all power lines that are connected to towers within the administrative boundary
way["power"="line"](area.searchArea)
  (bn.towers) -> .lines_connected;

// Find all high-voltage power lines (>= 90 kV) within the administrative boundary
way["power"="line"]["voltage"](if:t["voltage"] >= 90000)(area.searchArea) -> .high_voltage_lines;

// Find only poles that are part of high-voltage lines within the administrative boundary
node.poles(w.high_voltage_lines) -> .hv_poles;

(
.towers;
.hv_poles;
)-> .all_towers;

(
  nwr.all_towers(user_touched:"Andreas Hernandez");
  nwr.all_towers(user_touched:"Tobias Augspurger");
);

out body;
>;
out skel qt;
