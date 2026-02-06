import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Paths
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

# Load data
app_kpis = pd.read_csv(PROCESSED_DIR / "app_kpis.csv")

# Sort apps by average rating
app_kpis = app_kpis.sort_values("average_rating", ascending=False)

# Plot
plt.figure(figsize=(10, 6))
plt.barh(app_kpis["app_id"], app_kpis["average_rating"])
plt.xlabel("Average Rating")
plt.title("Average User Rating by AI Note-Taking Application")
plt.gca().invert_yaxis()
plt.tight_layout()

# Save figure
output_path = OUTPUTS_DIR / "average_rating_by_app.png"
plt.savefig(output_path)

# Show plot
plt.show()
