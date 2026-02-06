import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def create_app_level_kpis():
    """
    Create application-level KPIs from reviews data.
    """
    reviews = pd.read_csv(PROCESSED_DIR / "reviews_clean.csv", parse_dates=["at"])

    app_kpis = reviews.groupby("app_id").agg(
        number_of_reviews=("reviewId", "count"),
        average_rating=("score", "mean"),
        pct_low_rating=("score", lambda x: (x <= 2).mean()),
        first_review_date=("at", "min"),
        last_review_date=("at", "max")
    ).reset_index()

    app_kpis.to_csv(PROCESSED_DIR / "app_kpis.csv", index=False)


def create_daily_metrics():
    """
    Create daily aggregated metrics from reviews data.
    """
    reviews = pd.read_csv(PROCESSED_DIR / "reviews_clean.csv", parse_dates=["at"])
    reviews["date"] = reviews["at"].dt.date

    daily_metrics = reviews.groupby("date").agg(
        daily_number_of_reviews=("reviewId", "count"),
        daily_average_rating=("score", "mean")
    ).reset_index()

    daily_metrics.to_csv(PROCESSED_DIR / "daily_metrics.csv", index=False)


if __name__ == "__main__":
    create_app_level_kpis()
    create_daily_metrics()
