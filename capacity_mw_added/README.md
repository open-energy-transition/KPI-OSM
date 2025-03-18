# Steps
1. Run capacity_added.py
2. It will ask for the country of choice, and the usernames of the mappers. 
3. If you want the % capacity that you have mapped, find the total capacity of your country of choice at https://openinframap.org/stats, and type it in the python terminal (eg. 8700MW).

## Example Output

![image](https://github.com/user-attachments/assets/76190443-3249-4107-855e-70bc43e6d028)

## Issues/Caveats
1. When two power plants are part of one multipolygon (ex: Ezra power plants in South sudan), it only counts as one in the tag value.
2. In OSM, there is no query to distinguish modification and creation. So if all you did was add a name, then that power plant will be counted to you. The only distinguisher of a node/way/relation, is the "version" in the changeset of OSM.
3. If you do not find capacity of a plant, then it's not counted
