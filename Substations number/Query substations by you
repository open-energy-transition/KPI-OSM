[out:json][timeout:400];

node["power"="substation"](user:"Andreas Hernandez")-> .substation_nodes;
way["power"="substation"](user:"Andreas Hernandez") -> .substation_ways;
relation["power"="substation"](user:"Andreas Hernandez")-> .substation_relations;

// Combine all relevant results
(
  .substation_nodes;
  .substation_ways;
  .substation_relations;

);

out body;
>;
out skel qt;
