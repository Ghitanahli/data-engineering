from google_play_scraper import search, app, reviews
import json
from pathlib import Path

# Root directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def extract_apps():
    """
    Extract metadata for AI note-taking applications from Google Play Store
    and store raw results as JSON.
    """
    search_results = search(
        "AI note taking",
        lang="en",
        country="us",
        n_hits=20
    )

    apps_metadata = []

    for result in search_results:
        app_details = app(result["appId"])
        apps_metadata.append(app_details)

    with open(RAW_DIR / "apps_metadata.json", "w", encoding="utf-8") as f:
        json.dump(apps_metadata, f, indent=2, ensure_ascii=False)

    return apps_metadata


def extract_reviews(apps_metadata):
    """
    Extract user reviews for each application and store raw reviews as JSON.
    """
    all_reviews = []

    for app_meta in apps_metadata:
        app_id = app_meta["appId"]
        app_name = app_meta["title"]

        reviews_data, _ = reviews(
            app_id,
            lang="en",
            country="us",
            count=200
        )

        for review in reviews_data:
    # Convert datetime to string for JSON compatibility
            if "at" in review and review["at"] is not None:
                review["at"] = review["at"].isoformat()

            review["appId"] = app_id
            review["appName"] = app_name
            all_reviews.append(review)

    with open(RAW_DIR / "apps_reviews.json", "w", encoding="utf-8") as f:
        json.dump(all_reviews, f, indent=2, ensure_ascii=False, default=str)



if __name__ == "__main__":
    apps = extract_apps()
    extract_reviews(apps)
