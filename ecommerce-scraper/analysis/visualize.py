import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data_path = os.path.join(os.path.dirname(__file__), "..", "data", "books_data.xlsx")
df = pd.read_excel(data_path)

# Ensure charts dir exists
charts_dir = os.path.join(os.path.dirname(__file__), "charts")
os.makedirs(charts_dir, exist_ok=True)

# Price distribution
plt.figure()
sns.histplot(df["Price"], bins=10, kde=True)
plt.title("Book Price Distribution")
plt.savefig(os.path.join(charts_dir, "price_distribution.png"))
plt.show()

# Rating count
plt.figure()
sns.countplot(x="Rating", data=df)
plt.title("Book Ratings Count")
plt.savefig(os.path.join(charts_dir, "rating_count.png"))
plt.show()

print(f"Charts saved in: {os.path.abspath(charts_dir)}")
