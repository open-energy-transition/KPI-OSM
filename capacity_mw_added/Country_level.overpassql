[out:json][timeout:400];

node["place"~"country|state|province"]({{bbox}}) -> .places;

relation["boundary"="administrative"]["admin_level"="2"](bn.places) -> .admin_boundary;

// Map the relation to an area
.admin_boundary map_to_area -> .searchArea;

node["power"="plant"](user:"Andreas Hernandez")(area.searchArea)-> .plant_nodes;
way["power"="plant"](user:"Andreas Hernandez")(area.searchArea)-> .plant_ways;
relation["power"="plant"](user:"Andreas Hernandez")(area.searchArea)-> .plant_relations;

// Combine all relevant results
(
  .plant_nodes;
  .plant_ways;
  .plant_relations;
);

out body;
>;
out skel qt;

