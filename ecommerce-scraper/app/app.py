from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

def load_df():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "books_data.xlsx")
    return pd.read_excel(data_path)

df = load_df()

@app.route("/", methods=["GET", "POST"])
def home():
    query = request.form.get("query")
    if query:
        results = df[df["Title"].str.contains(query, case=False, na=False)]
    else:
        results = df
    return render_template("index.html", tables=results.to_html(classes='data', index=False))

# Optional: button-free refresh URL to reload Excel after scraping new data
@app.route("/refresh")
def refresh():
    global df
    df = load_df()
    return "Data refreshed. <a href='/'>Go back</a>"

if __name__ == "__main__":
    app.run(debug=True)
