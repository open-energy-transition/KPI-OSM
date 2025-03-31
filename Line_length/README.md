# 🚀 Steps
1. Run line_length.py
2. Enter in the terminal, the country name and the usernames of the mappers

## ⭐ Output
This will show you the total line length users have modified in km, as well as a table with the distribution in km per voltage levels.

![image](https://github.com/user-attachments/assets/0e14c720-135d-4c19-b7eb-88d173d86eee)


## ❗Issues/Caveats
1. This looks at modification of a "way", therefore adding voltage to a way will count as the entire way being modified, even though you did not place X km of line.
2. Issues may arise since not all voltage values have been cleaned for (ex: 220kv;110kv/60kv).
