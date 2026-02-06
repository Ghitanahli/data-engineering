import pandas as pd
import matplotlib.pyplot as plt

# Load serving-layer data
app_kpis = pd.read_csv("data/processed/app_kpis.csv")

# Sort apps by average rating
app_kpis = app_kpis.sort_values("average_rating", ascending=False)

# Plot
plt.figure(figsize=(10, 6))
plt.barh(app_kpis["app_id"], app_kpis["average_rating"])
plt.xlabel("Average Rating")
plt.title("Average User Rating by AI Note-Taking Application")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
