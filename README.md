# MP2 REST API

This project is a FastAPI application that wraps the MP1 data pipeline in a REST API. `POST /upload` accepts a CSV file, stores it in memory, and returns its ID along with row and column counts. `GET /datasets/{dataset_id}` returns up to `limit` rows of a stored dataset and the total row count. `POST /datasets/{dataset_id}/process` takes a JSON configuration, validates the dataset with the MP1 validator, applies the enabled cleaning steps (duplicate removal, missing-value handling, and outlier removal), replaces the stored data with the cleaned version, and returns a cleaning report. `GET /health` reports the API status and version. The reusable MP1 modules live in `data_pipeline/`, while `src/` holds the API models, in-memory storage, logging setup, and a middleware that logs each request with a unique request ID, status code, and duration. Tests in `tests/` use pytest and FastAPI's TestClient to cover the upload, process, and retrieve workflow.

## Usage

```bash
python -m uvicorn main:app --reload
python -m pytest tests -v
```
