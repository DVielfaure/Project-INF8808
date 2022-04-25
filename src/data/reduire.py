import pandas as pd

list_csv = ['Id', 'Departure Date', 
        'Departure Hardour', 'Departure Region', 
        'Departure Latitude', 'Departure Longitude', 
        'Arrival Date', 'Arrival Hardour', 
        'Arrival Region', 'Arrival Latitude', 
        'Arrival Longitude', 'Vessel Type', 
        'Lenght', 'Width', 
        'DeadWeight Tonnage', 'Maximum Draugth']

# df = pd.read_csv("Arrival Date.csv")
# df = df["Arrival Date"].str.replace(":00.000","")
# df.to_csv("Arrival Date.csv", index=False)

# df = pd.read_csv("Departure Date.csv")
# df = df["Departure Date"].str.replace(":00.000","")
# df.to_csv("Departure Date.csv", index=False)

# df = pd.read_csv("Lenght.csv")
# df = df["Lenght"].round(decimals=0)
# df.to_csv("Lenght.csv", index=False)

# df = pd.read_csv("Maximum Draugth.csv")
# df = df["Maximum Draugth"].round(decimals=0)
# df.to_csv("Maximum Draugth.csv", index=False)

# df = pd.read_csv("Width.csv")
# df = df["Width"].round(decimals=0)
# df.to_csv("Width.csv", index=False)

df = pd.read_csv("DeadWeight Tonnage.csv")
df = df["DeadWeight Tonnage"].astype(int)
df.to_csv("DeadWeight Tonnage.csv", index=False)

df = pd.read_csv("Lenght.csv")
df = df["Lenght"].astype(int)
df.to_csv("Lenght.csv", index=False)

df = pd.read_csv("Maximum Draugth.csv")
df = df["Maximum Draugth"].astype(int)
df.to_csv("Maximum Draugth.csv", index=False)

df = pd.read_csv("Width.csv")
df = df["Width"].astype(int)
df.to_csv("Width.csv", index=False)

# for name in list_csv:
#     df = pd.read_csv(name+".csv")
#     df.drop(index=df.index[:165000], axis=0, inplace=True)
#     df.to_csv(name+".csv", index=False)
#     print(name)