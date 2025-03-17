import pandas as pd

# Function to convert to MW
def convert_to_mw(value):
    value = str(value).strip()
    if value.lower().endswith("kwp"):
        return float(value[:-3]) / 1000  # Remove "kwp" and convert to MW
    elif value.lower().endswith("kw"):
        return float(value[:-2]) / 1000  # Remove "kW" and convert to MW
    elif value.lower().endswith("mw"):
        return float(value[:-2])         # Remove "MW" and use as is
    elif value.lower().endswith("mwp"):
        return float(value[:-3])         # Remove "MWp" and use as is
    else:
        return float(value)  # Assume it's already in MW

# Function to convert total country capacity to MW
def convert_country_capacity(input_value):
    input_value = str(input_value).strip().lower()
    if "gw" in input_value:
        return float(input_value.replace("gw", "")) * 1000  # Convert GW to MW
    elif "mw" in input_value:
        return float(input_value.replace("mw", ""))         # Use as is
    else:
        return float(input_value)  # Assume it's already in MW

# Get multi-line input from the user
print("Paste power values (one per line) and press Enter twice to finish:")
lines = []
while True:
    line = input()
    if line == "":  # Stop reading input when an empty line is entered
        break
    lines.append(line)

# Convert the list into a pandas DataFrame
df = pd.DataFrame(lines, columns=["plant:output:electricity"])

# Apply the conversion function to each value
df["Output_MW"] = df["plant:output:electricity"].apply(convert_to_mw)

# Sum the converted values
total_found_capacity = df["Output_MW"].sum()

# Print the processed data and total found capacity
print("\nProcessed Data:")
print(df)
print(f"\nTotal Found Capacity: {total_found_capacity} MW")

# Ask for the total MW capacity of the country
total_country_input = input("\nWhat is the total MW capacity of the country? (e.g., 2500, 2500 MW): ")

# Convert the input to MW
total_country_capacity = convert_country_capacity(total_country_input)

# Calculate the percentage
percentage = (total_found_capacity / total_country_capacity) * 100

# Print the percentage
print(f"\nYou have mapped {percentage:.2f}% of the total country capacity.")
