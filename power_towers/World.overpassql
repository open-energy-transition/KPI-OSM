[out:json][timeout:400];

// Select all power towers and poles mapped by the specified users
(
  node["power"="tower"](user:"Andreas Hernandez");
  node["power"="tower"](user:"Tobias Augspurger");
  node["power"="tower"](user:"Mwiche");
  node["power"="tower"](user:"davidtt92");
  node["power"="pole"](user:"Andreas Hernandez");
  node["power"="pole"](user:"Tobias Augspurger");
  node["power"="pole"](user:"Mwiche");
  node["power"="pole"](user:"davidtt92");
);

out body;
>;
out skel qt;
