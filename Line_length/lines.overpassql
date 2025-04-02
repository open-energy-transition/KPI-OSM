[out:json][timeout:400];

relation["boundary"="administrative"][~"^name(:en)?$"~"Nepal", i] -> .admin_boundary;
.admin_boundary map_to_area -> .searchArea;

way["power"="line"](area.searchArea) -> .lines;
way["power"="cable"](area.searchArea) -> .cables;

(
  way.lines(user_touched:"Andreas Hernandez");
  way.cables(user_touched:"Andreas Hernandez");
);

out body;
>;
out skel qt;
