def test_upload_csv(client, sample_csv_bytes):
    response = client.post(
        "/upload",
        files={"file": ("sample_data.csv", sample_csv_bytes, "text/csv")}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["rows"] == 6
    assert body["columns"] == 2
    assert isinstance(body["id"], int)
    assert body["id"] > 0


def test_process_and_retrieve(client, uploaded_dataset_id, processing_body):
    response = client.post(
        f"/datasets/{uploaded_dataset_id}/process",
        json=processing_body
    )
    assert response.status_code == 200
    body = response.json()
    assert body["validation_rows_removed"] == 1
    assert body["cleaning_report"]["rows_before"] == 5
    assert body["cleaning_report"]["rows_after"] == 3

    response = client.get(f"/datasets/{uploaded_dataset_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["total_rows"] == 3
    student_ids = [row["student_id"] for row in body["data"]]
    scores = [row["score"] for row in body["data"]]
    assert student_ids == [1, 2, 5]
    assert scores == [80, 90, 85]


def test_retrieve_missing_dataset(client):
    response = client.get("/datasets/999")
    assert response.status_code == 404


# Optional tests (ungraded)

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_unsupported_extension(client):
    response = client.post(
        "/upload",
        files={"file": ("notes.txt", b"hello", "text/plain")}
    )
    assert response.status_code == 400


def test_invalid_limit(client, uploaded_dataset_id):
    response = client.get(f"/datasets/{uploaded_dataset_id}?limit=0")
    assert response.status_code == 422


def test_process_missing_dataset(client, processing_body):
    response = client.post("/datasets/999/process", json=processing_body)
    assert response.status_code == 404


def test_missing_required_column(client, uploaded_dataset_id, processing_body):
    processing_body["validation"]["required_columns"].append("name")
    response = client.post(
        f"/datasets/{uploaded_dataset_id}/process",
        json=processing_body
    )
    assert response.status_code == 400
    response = client.get(f"/datasets/{uploaded_dataset_id}")
    assert response.json()["total_rows"] == 6


def test_request_ids(client):
    first = client.get("/health")
    second = client.get("/datasets/999")
    first_id = first.headers["X-Request-ID"]
    second_id = second.headers["X-Request-ID"]
    assert len(first_id) == 8
    assert len(second_id) == 8
    assert first_id != second_id
