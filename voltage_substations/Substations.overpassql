[out:json][timeout:400];

relation["boundary"="administrative"]
  [~"^name(:en)?$"~"Mozambique", i] -> .admin_boundary;
.admin_boundary map_to_area -> .searchArea;

node["power"="substation"](area.searchArea) -> .substation_nodes;
way["power"="substation"](area.searchArea) -> .substation_ways;
relation["power"="substation"](area.searchArea) -> .substation_relations;

(
  node.substation_nodes(user_touched:"Andreas Hernandez");
  way.substation_ways(user_touched:"Andreas Hernandez");
  relation.substation_relations(user_touched:"Andreas Hernandez");
);

out body;
>;
out skel qt;
