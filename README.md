# KPI-OSM
This repository includes individual scripts but also a web interface to see your progress here:<br>
https://open-energy-transition.github.io/KPI-OSM/ <br>

The web interface includes 4 kpi tools for now.

❗The accuracy of how contributions by mappers is calculated is in progress. This is because it can be difficult to attribute creations and modifications correctly to people, especially "ways".
Any KPI where "ways" are measured such as power lines, is at the moment overinflated, since your small modification of a way will show as if you had created the entire way. There is an argument however that without your contribution, the way would not be correctly finalised, or important metadata would be missing. However, we are working to find a way (no pun intended) to precisely attribute changes to users (looking at changeset versions for example etc).

## 🔄 Before and after script
This script gives you a good visualisation of the mapping activities users have made. 
It includes two queries: the first query fetches all mapping activity since a specific date, and the second fetches all activity by usernames.

❗If you use the query based on a date, someone else might have mapped in-between and thus that activity will also be fetched.

## 🔋Power plant capacity added
This script gives you the total amount of capacity a user(s) have mapped in a country. If the total [capacity](https://openinframap.org/stats)  from that country is added in the terminal, it will also give you the % of the country power plants capacity you have mapped.

## 🗼Power towers
This folder contains a python script which gives you the total towers and high-voltage poles users have mapped in a country, and also gives you a table with the distribution of these towers based on voltages. The other scripts are overpass queries that can show you 1) The % towers you have mapped in a country, and 2) The total amount of towers worldwide you have mapped.

## 🔌 Voltage Substations
This script gives you the total amount of substations you have mapped/edited in a country, as well as a table with the distribution of these substations based on voltage.

## :straight_ruler: Power line length
This script gives you the total line length in km of power lines (ways) edited by you. It also gives a table with the distribution based on voltage. The line length is calculated using OSM coordinates of the nodes the lines are connected to. The projection used by OSM is WGS84 EPSG:4326. Progress could be made by integrating a more precise local UTM projection. <br>
⚠️One big caveat with line length attribution to a user, is that it depends on how you have mapped the way (power lines). If you "continue" the way from someone else, then that entire way will be attributed to you and thus the line length your user has touched is overinflated. So power line length for users as a kpi is not the best.



