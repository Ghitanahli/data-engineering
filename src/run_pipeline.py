from extract import extract_apps, extract_reviews
from transform import transform_apps, transform_reviews
from serve import create_app_level_kpis, create_daily_metrics


def run_pipeline():
    apps = extract_apps()
    extract_reviews(apps)

    transform_apps()
    transform_reviews()

    create_app_level_kpis()
    create_daily_metrics()


if __name__ == "__main__":
    run_pipeline()
