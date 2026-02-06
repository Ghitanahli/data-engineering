# Lab 1 – Python-only Data Pipeline  
January 2026 – Written Answers

---

## A. Environment Setup

A dedicated Python virtual environment (Python 3.7+) was created to isolate project dependencies and ensure reproducibility.
All libraries required for the pipeline were installed inside this environment as the project evolved.
VS Code was used as the main development environment instead of Jupyter notebooks, in order to reflect a more realistic
data engineering workflow based on scripts and re-runnable pipelines.

The active virtual environment was explicitly selected in both the terminal and the IDE to ensure that the correct
dependencies were used when running the code.

---

## B. End-to-End Data Pipeline

The goal of this lab was to build a Python-only data pipeline that converts raw data into analytics-ready datasets.
The pipeline follows the main stages of the data engineering lifecycle:
data generation, ingestion, transformation, serving, and consumption.

The use case focuses on competitive market research for AI note-taking mobile applications.
Two datasets were used:
- Applications Catalog: metadata about each app (dimension dataset).
- Applications Reviews: user-generated reviews (fact dataset).

Raw data is stored in `data/raw`, while cleaned and aggregated outputs are written to `data/processed`.
All pipeline logic is implemented in Python scripts located in the `src` directory.

---

## 1. Data Acquisition and Ingestion

Google Play Store was used as the data source.
To extract data programmatically, the `google-play-scraper` Python library was used instead of manual web scraping.
This approach provides more structured and reliable data access.

The following data was extracted:
- Application metadata (title, developer, ratings, installs, category, price, etc.).
- User reviews, including rating, review text, timestamps, and engagement metrics.

Raw data was stored **as-is** in JSON files:
- `apps_metadata.json`
- `apps_reviews.json`

No transformations were applied at this stage in order to preserve the original source data and allow the pipeline
to be re-run from scratch.

---

## 2. Diagnosing and Transforming Raw Data

Before implementing transformations, the raw JSON files were inspected to understand their structure and limitations.
Several issues were identified that prevent direct analytical use:

1. The data is semi-structured and contains nested fields.
2. Some fields contain missing or null values.
3. Numeric values (ratings, scores) are not always guaranteed to behave numerically.
4. Timestamps are not directly usable for aggregation.
5. Duplicate reviews can appear.
6. Some raw fields are not suitable for analytics in their original form.

---

### Transformation Strategy

The transformation logic was implemented using Python and Pandas.
The objective was to convert semi-structured JSON data into clean, tabular datasets suitable for analytics.

Two processed datasets were produced:

#### Applications Catalog
Fields:
- appId  
- title  
- developer  
- score  
- ratings  
- installs  
- genre  
- price  

#### Applications Reviews
Fields:
- app_id  
- app_name  
- reviewId  
- userName  
- score  
- content  
- thumbsUpCount  
- at  

Key transformations included:
- Flattening JSON structures.
- Removing duplicate reviews.
- Converting numeric fields to proper numeric types.
- Parsing timestamps into datetime objects.
- Ensuring consistency and joinability across datasets.

Processed datasets were written to the `data/processed` directory as CSV files.
Raw data files were never modified directly.
The pipeline can be re-run from scratch at any time.

---

## 3. Serving Layer

The serving layer prepares data for downstream consumers such as dashboards and analytics tools.
Only transformed datasets from `data/processed` were used.

Two serving-layer outputs were created:

### Output 1 – App-Level KPIs
For each application:
- Number of reviews
- Average rating
- Percentage of low-rating reviews (rating ≤ 2)
- First review date
- Most recent review date

### Output 2 – Daily Metrics
For each day:
- Daily number of reviews
- Daily average rating

Both outputs are reproducible and regenerated entirely when the pipeline is re-run.

---

## 4. Lightweight Dashboarding (Consumer View)

A lightweight dashboard was built using Matplotlib.
The dashboard consumes only serving-layer outputs and does not modify the pipeline.

The visualization compares average user ratings across applications.
This allows identification of applications that perform best or worst according to user reviews
and highlights differences in perceived quality across competitors.

The resulting chart is saved as a static image to make results easily reviewable without re-running the code.

---

## C. Pipeline Changes and Stress Testing

This section highlights how fragile early-stage data pipelines can be when upstream data changes.

---

### 1. New Reviews Batch

When running the pipeline on a new batch of reviews, only minor code changes were required.
The pipeline performs a full rebuild implicitly, as all outputs are regenerated from raw inputs.
Duplicate reviews are handled during transformation through deduplication logic.
Reviews referencing unknown applications remain in the dataset but may not join with application metadata.

This step revealed that full-refresh behavior exists but is not explicitly documented in the pipeline design.

---

### 2. Schema Drift in Reviews

When column names and structures changed, parts of the pipeline relying on hard-coded field names failed.
Some failures were explicit, while others could silently produce incorrect results.

Adapting the pipeline required modifying transformation logic, showing how schema drift can introduce
maintenance overhead and fragility in Python-only pipelines.

---

### 3. Dirty and Inconsistent Data Records

When the reviews dataset contained invalid ratings or malformed timestamps, the pipeline relied on default
type coercion behavior.
Invalid values were often converted to null values and propagated into downstream aggregations without
explicit errors.

This demonstrated how data quality issues can silently affect analytical results if not explicitly handled.

---

### 4. Updated Applications Metadata

When applications metadata included duplicate identifiers or missing values, joins between reviews and
applications were affected.
Duplicate application identifiers could lead to ambiguous joins and distorted aggregates.

This step highlighted the lack of explicit enforcement of uniqueness and referential integrity assumptions
in the pipeline.

---# Lab 1 – Python-only Data Pipeline  
January 2026 – Written Answers

---

## A. Environment Setup

A dedicated Python virtual environment (Python 3.7+) was created to isolate project dependencies and ensure reproducibility.
All libraries required for the pipeline were installed inside this environment as the project evolved.
VS Code was used as the main development environment instead of Jupyter notebooks, in order to reflect a more realistic
data engineering workflow based on scripts and re-runnable pipelines.

The active virtual environment was explicitly selected in both the terminal and the IDE to ensure that the correct
dependencies were used when running the code.

---

## B. End-to-End Data Pipeline

The goal of this lab was to build a Python-only data pipeline that converts raw data into analytics-ready datasets.
The pipeline follows the main stages of the data engineering lifecycle:
data generation, ingestion, transformation, serving, and consumption.

The use case focuses on competitive market research for AI note-taking mobile applications.
Two datasets were used:
- Applications Catalog: metadata about each app (dimension dataset).
- Applications Reviews: user-generated reviews (fact dataset).

Raw data is stored in `data/raw`, while cleaned and aggregated outputs are written to `data/processed`.
All pipeline logic is implemented in Python scripts located in the `src` directory.

---

## 1. Data Acquisition and Ingestion

Google Play Store was used as the data source.
To extract data programmatically, the `google-play-scraper` Python library was used instead of manual web scraping.
This approach provides more structured and reliable data access.

The following data was extracted:
- Application metadata (title, developer, ratings, installs, category, price, etc.).
- User reviews, including rating, review text, timestamps, and engagement metrics.

Raw data was stored **as-is** in JSON files:
- `apps_metadata.json`
- `apps_reviews.json`

No transformations were applied at this stage in order to preserve the original source data and allow the pipeline
to be re-run from scratch.

---

## 2. Diagnosing and Transforming Raw Data

Before implementing transformations, the raw JSON files were inspected to understand their structure and limitations.
Several issues were identified that prevent direct analytical use:

1. The data is semi-structured and contains nested fields.
2. Some fields contain missing or null values.
3. Numeric values (ratings, scores) are not always guaranteed to behave numerically.
4. Timestamps are not directly usable for aggregation.
5. Duplicate reviews can appear.
6. Some raw fields are not suitable for analytics in their original form.

---

### Transformation Strategy

The transformation logic was implemented using Python and Pandas.
The objective was to convert semi-structured JSON data into clean, tabular datasets suitable for analytics.

Two processed datasets were produced:

#### Applications Catalog
Fields:
- appId  
- title  
- developer  
- score  
- ratings  
- installs  
- genre  
- price  

#### Applications Reviews
Fields:
- app_id  
- app_name  
- reviewId  
- userName  
- score  
- content  
- thumbsUpCount  
- at  

Key transformations included:
- Flattening JSON structures.
- Removing duplicate reviews.
- Converting numeric fields to proper numeric types.
- Parsing timestamps into datetime objects.
- Ensuring consistency and joinability across datasets.

Processed datasets were written to the `data/processed` directory as CSV files.
Raw data files were never modified directly.
The pipeline can be re-run from scratch at any time.

---

## 3. Serving Layer

The serving layer prepares data for downstream consumers such as dashboards and analytics tools.
Only transformed datasets from `data/processed` were used.

Two serving-layer outputs were created:

### Output 1 – App-Level KPIs
For each application:
- Number of reviews
- Average rating
- Percentage of low-rating reviews (rating ≤ 2)
- First review date
- Most recent review date

### Output 2 – Daily Metrics
For each day:
- Daily number of reviews
- Daily average rating

Both outputs are reproducible and regenerated entirely when the pipeline is re-run.

---

## 4. Lightweight Dashboarding (Consumer View)

A lightweight dashboard was built using Matplotlib.
The dashboard consumes only serving-layer outputs and does not modify the pipeline.

The visualization compares average user ratings across applications.
This allows identification of applications that perform best or worst according to user reviews
and highlights differences in perceived quality across competitors.

The resulting chart is saved as a static image to make results easily reviewable without re-running the code.

---

## C. Pipeline Changes and Stress Testing

This section highlights how fragile early-stage data pipelines can be when upstream data changes.

---

### 1. New Reviews Batch

When running the pipeline on a new batch of reviews, only minor code changes were required.
The pipeline performs a full rebuild implicitly, as all outputs are regenerated from raw inputs.
Duplicate reviews are handled during transformation through deduplication logic.
Reviews referencing unknown applications remain in the dataset but may not join with application metadata.

This step revealed that full-refresh behavior exists but is not explicitly documented in the pipeline design.

---

### 2. Schema Drift in Reviews

When column names and structures changed, parts of the pipeline relying on hard-coded field names failed.
Some failures were explicit, while others could silently produce incorrect results.

Adapting the pipeline required modifying transformation logic, showing how schema drift can introduce
maintenance overhead and fragility in Python-only pipelines.

---

### 3. Dirty and Inconsistent Data Records

When the reviews dataset contained invalid ratings or malformed timestamps, the pipeline relied on default
type coercion behavior.
Invalid values were often converted to null values and propagated into downstream aggregations without
explicit errors.

This demonstrated how data quality issues can silently affect analytical results if not explicitly handled.

---

### 4. Updated Applications Metadata

When applications metadata included duplicate identifiers or missing values, joins between reviews and
applications were affected.
Duplicate application identifiers could lead to ambiguous joins and distorted aggregates.

This step highlighted the lack of explicit enforcement of uniqueness and referential integrity assumptions
in the pipeline.

---

### 5. New Business Logic Stress Test

The requested analysis of sentiment-rating mismatches cannot be answered using existing serving outputs.
Additional fields and transformations would be required, such as sentiment indicators derived from review text.

This logic would naturally belong in the transformation layer.
Supporting this request would require changes across multiple pipeline components, demonstrating that
business-driven changes can significantly impact pipeline design.

The current pipeline partially separates data preparation from analytical logic, but reuse and extensibility
would become increasingly difficult as new requirements accumulate.

---

## Conclusion

This lab demonstrates the complete data engineering lifecycle using a Python-only pipeline.
It exposes common challenges such as schema drift, data quality issues, implicit assumptions, and
maintenance complexity.
These limitations highlight why more structured tools and frameworks are typically introduced in
production-grade data systems.
red, such as sentiment indicators derived from review text.

This logic would naturally belong in the transformation layer.
Supporting this request would require changes across multiple pipeline components, demonstrating that
business-driven changes can significantly impact pipeline design.

The current pipeline partially separates data preparation from analytical logic, but reuse and extensibility
would become increasingly difficult as new requirements accumulate.

---

## Conclusion

This lab demonstrates the complete data engineering lifecycle using a Python-only pipeline.
It exposes common challenges such as schema drift, data quality issues, implicit assumptions, and
maintenance complexity.
These limitations highlight why more structured tools and frameworks are typically introduced in
production-grade data systems.
