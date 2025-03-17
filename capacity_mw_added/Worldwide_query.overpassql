[out:json][timeout:400];

// Include power plants within the administrative boundary
node["power"="plant"](user:"Andreas Hernandez") -> .plant_nodes;
way["power"="plant"](user:"Andreas Hernandez") -> .plant_ways;
relation["power"="plant"](user:"Andreas Hernandez")-> .plant_relations;


// Combine all relevant results
(
  .plant_nodes;
  .plant_ways;
  .plant_relations;
);

out body;
>;
out skel qt;
