# Steps
1. Run query in JOSM to find power plants modified or created by you
2. Select all -> in the Tags Window (on the right), right click on the "plant=output=electricity" **value**, and copy value
3. Run python script, paste values and press enter. This will show you the capacity you have added in MW
4. To see the % extra you added to a country , you can go to https://openinframap.org/stats and see total capacity of a country.


## Issues
1. When two power plants are part of one multipolygon (ex: Ezra power plants in South sudan), it only counts as one in the tag value.
2. In OSM, there is no query to distinguish modification and creation. So if all you did was add a name, then that power plant will be counted to you. The only distinguisher of a node/way/relation, is the "version" in the changeset of OSM.
