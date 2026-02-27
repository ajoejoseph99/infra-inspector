from google.cloud import storage

storage_client = storage.Client()
OUTPUT_BUCKET_NAME = "school-infra-reports-cv"

def list_inspection_reports() -> str:
    """Lists all available infrastructure inspection reports."""
    try:
        bucket = storage_client.bucket(OUTPUT_BUCKET_NAME)
        files = [blob.name for blob in bucket.list_blobs() if blob.name.endswith('.md')]
        return "Available reports:\n" + "\n".join(files) if files else "No reports found."
    except Exception as e:
        return f"Error accessing reports: {str(e)}"

def read_inspection_report(filename: str) -> str:
    """Reads the contents of a specific Markdown inspection report."""
    try:
        bucket = storage_client.bucket(OUTPUT_BUCKET_NAME)
        blob = bucket.blob(filename)
        return blob.download_as_text() if blob.exists() else f"Error: '{filename}' not found."
    except Exception as e:
        return f"Error reading report: {str(e)}"