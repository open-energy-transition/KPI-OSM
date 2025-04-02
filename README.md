# KPI-OSM
This repository includes individual scripts but also a web interface to see your progress here: 
https://open-energy-transition.github.io/KPI-OSM/ <br>
The web interface includes 4 kpi tools for now.

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
This script gives you the total line length in km of power lines (ways) edited by you. It also gives a table with the distribution based on voltage.



