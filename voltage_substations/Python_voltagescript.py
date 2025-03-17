import pandas as pd

# Function to convert voltage to kV and handle combined voltages
def process_voltage(value):
    value = str(value).strip()
    if "/" in value:  # Handle combined voltages (e.g., 230000/115000)
        parts = value.split("/")
        return max(float(part) for part in parts) / 1000  # Take the largest and convert to kV
    else:
        return float(value) / 1000  # Convert to kV

# Get multi-line input from the user
print("Paste substation voltages (one per line). Press Enter twice to finish:")
lines = []
while True:
    try:
        line = input()
    except EOFError:  # Handle Ctrl+D (end of input)
        break
    if line == "":  # Stop reading input when an empty line is entered
        break
    lines.append(line)

# Process the voltages
voltages_kv = [process_voltage(value) for value in lines if value.strip()]  # Skip empty lines

# Count the number of substations
num_substations = len(voltages_kv)

# Create a table of voltages and their counts
voltage_counts = pd.Series(voltages_kv).value_counts().sort_index().reset_index()
voltage_counts.columns = ["Voltage (kV)", "Number of Substations"]

# Print the results
print(f"\nYou have edited {num_substations} substations.")
print("\nVoltage Distribution:")
print(voltage_counts.to_string(index=False))
