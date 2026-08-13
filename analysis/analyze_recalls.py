import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

dbname = "postgres"
user = "postgres"
password = os.getenv("POSTGRES_PASSWORD")
host = "localhost"


def load_data() -> pd.DataFrame:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    df = pd.read_sql("SELECT * FROM rappel_conso_table", conn)
    conn.close()
    return df


def plot_top_categories(df: pd.DataFrame):
    counts = df["categorie_de_produit"].value_counts().head(10)
    plt.figure(figsize=(8, 5))
    counts.plot(kind="barh")
    plt.gca().invert_yaxis()
    plt.title("Top 10 Product Categories by Recall Count")
    plt.xlabel("Number of recalls")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_categories.png"))
    plt.close()


def plot_recalls_over_time(df: pd.DataFrame):
    dates = pd.to_datetime(df["date_de_publication"], errors="coerce")
    by_month = dates.dt.to_period("M").value_counts().sort_index()
    plt.figure(figsize=(10, 5))
    by_month.plot(kind="line", marker="o")
    plt.title("Recalls Over Time (by month)")
    plt.xlabel("Month")
    plt.ylabel("Number of recalls")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "recalls_over_time.png"))
    plt.close()


def plot_top_reasons(df: pd.DataFrame):
    counts = df["motif_du_rappel"].value_counts().head(10)
    plt.figure(figsize=(8, 5))
    counts.plot(kind="barh")
    plt.gca().invert_yaxis()
    plt.title("Top 10 Recall Reasons")
    plt.xlabel("Number of recalls")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_reasons.png"))
    plt.close()


def print_summary(df: pd.DataFrame):
    print(f"Total recalls: {len(df)}")
    print(f"Date range: {df['date_de_publication'].min()} to {df['date_de_publication'].max()}")
    print("\nTop 5 categories:")
    print(df["categorie_de_produit"].value_counts().head(5))
    print("\nTop 5 recall reasons:")
    print(df["motif_du_rappel"].value_counts().head(5))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_data()
    print_summary(df)
    plot_top_categories(df)
    plot_recalls_over_time(df)
    plot_top_reasons(df)
    print(f"\nCharts saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
