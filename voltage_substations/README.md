# 🚀 Steps
1. Run python_voltagescript
2. Enter in the terminal, the country name and the usernames of the mappers

## ⭐ Output
This will show you the number of substations you have edited. It will also show you a small table with the different voltage substations and the count.

![image](https://github.com/user-attachments/assets/6c23d432-b63a-47c1-bd6d-1ef535142ec1)



## ❗Issues/Caveats
1. In OSM, there is no query to distinguish modification and creation. So if all you did was add a name, then that power plant will be counted to you. The only distinguisher of a node/way/relation, is the "version" in the changeset of OSM.
3. If you do not find capacity of a plant, then it's not counted
