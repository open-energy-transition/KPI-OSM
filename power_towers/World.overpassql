[out:json][timeout:400];
node["power"= "tower"](user:"Andreas Hernandez")->.towers;
node["power"="pole"](user:"Andreas Hernandez") -> .poles;

(
.towers;
.poles;
);

out body;
>;
out skel qt;
