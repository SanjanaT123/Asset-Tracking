import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

file_path = r"C:\Users\Sanjana\OneDrive\Documents\RSSIProject\RSSI_FINAL - Copy.xlsx"

df = pd.read_excel(file_path)

# Get distance labels
distances = df.iloc[1, 1:6].tolist()
distances = [str(d).replace('m', '').replace('(', '').replace(')', '') for d in distances]
distances = [float(d) for d in distances if d.strip() != '']

# Get RSSI values for CORNER 1
corner1 = df.iloc[3:, 1].dropna().astype(float).to_frame(name='RSSI')

# Calculate needed repeat length
repeat_count = len(corner1) // len(distances)
remaining = len(corner1) % len(distances)

# Build final distance list
full_distances = distances * repeat_count + distances[:remaining]
corner1['Distance'] = full_distances
corner1['Corner'] = 'Corner 1'

# Drop rows with any missing values
corner1 = corner1.dropna()

data = corner1  # If you have other corners, concat here

# Split features
X = data[['RSSI']]
y_corner = data['Corner']
y_distance = data['Distance']

X_train, X_test, y_corner_train, y_corner_test, y_distance_train, y_distance_test = train_test_split(
    X, y_corner, y_distance, test_size=0.2, random_state=42
)

corner_model = RandomForestClassifier()
corner_model.fit(X_train, y_corner_train)

distance_model = RandomForestRegressor()
distance_model.fit(X_train, y_distance_train)

corner_distance_models = {}
for corner_name in y_corner.unique():
    mask = y_corner == corner_name
    model = RandomForestRegressor()
    model.fit(X[mask], y_distance[mask])
    corner_distance_models[corner_name] = model

# Example RSSI
example_rssi = pd.DataFrame([[75]], columns=['RSSI'])

closest_corner = corner_model.predict(example_rssi)[0]
print("Predicted closest corner:", closest_corner)

predicted_distance = distance_model.predict(example_rssi)[0]
print("Predicted distance to that corner: {:.2f} meters".format(predicted_distance))

for c, model in corner_distance_models.items():
    d = model.predict(example_rssi)[0]
    print(f"{c}: {d:.2f} meters")
