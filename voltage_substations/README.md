# Steps
1. Run query in JOSM to find substations modified or created by you
2. Select all substation -> in the Tags Window (on the right), right click on the "voltage" **value**, and copy **value**.
3. Run python script, paste values and press enter. This will show you the number of substations you have edited. It will also show you a small table with the different voltage substations and the count.


## Issues/Caveats
1. In OSM, there is no query to distinguish modification and creation. So if all you did was add a name, then that power plant will be counted to you. The only distinguisher of a node/way/relation, is the "version" in the changeset of OSM.
3. If you do not find capacity of a plant, then it's not counted
