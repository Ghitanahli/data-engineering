import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def transform_apps():
    """
    Transform raw applications metadata into a clean tabular dataset.
    """
    with open(RAW_DIR / "apps_metadata.json", encoding="utf-8") as f:
        apps = json.load(f)

    rows = []

    for app_meta in apps:
        rows.append({
            "appId": app_meta.get("appId"),
            "title": app_meta.get("title"),
            "developer": app_meta.get("developer"),
            "score": app_meta.get("score"),
            "ratings": app_meta.get("ratings"),
            "installs": app_meta.get("installs"),
            "genre": app_meta.get("genre"),
            "price": app_meta.get("price", 0.0)
        })

    df_apps = pd.DataFrame(rows)
    df_apps.to_csv(PROCESSED_DIR / "apps_catalog.csv", index=False)


def transform_reviews():
    """
    Transform raw reviews into a clean analytics-ready dataset.
    """
    with open(RAW_DIR / "apps_reviews.json", encoding="utf-8") as f:
        reviews = json.load(f)

    rows = []

    for review in reviews:
        rows.append({
            "app_id": review.get("appId"),
            "app_name": review.get("appName"),
            "reviewId": review.get("reviewId"),
            "userName": review.get("userName"),
            "score": review.get("score"),
            "content": review.get("content"),
            "thumbsUpCount": review.get("thumbsUpCount"),
            "at": pd.to_datetime(review.get("at"), errors="coerce")
        })

    df_reviews = pd.DataFrame(rows)

    # Basic cleaning
    df_reviews = df_reviews.drop_duplicates(subset="reviewId")
    df_reviews["score"] = pd.to_numeric(df_reviews["score"], errors="coerce")

    df_reviews.to_csv(PROCESSED_DIR / "reviews_clean.csv", index=False)


if __name__ == "__main__":
    transform_apps()
    transform_reviews()
