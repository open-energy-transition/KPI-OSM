[out:json][timeout:400];

// Select all power towers and poles mapped by the specified users
(
  node["power"="tower"](user:"Andreas Hernandez");
  node["power"="tower"](user:"Tobias Augspurger");
  node["power"="pole"](user:"Andreas Hernandez");
  node["power"="pole"](user:"Tobias Augspurger");
);

out body;
>;
out skel qt;
