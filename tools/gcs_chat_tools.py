import google.auth
from google.cloud import storage

# Dynamically resolve the Project ID and Bucket Name
_, PROJECT_ID = google.auth.default()
OUTPUT_BUCKET_NAME = f"school-infra-reports-cv-{PROJECT_ID}"

storage_client = storage.Client()

def list_inspection_reports() -> str:
    """Lists all available infrastructure inspection reports."""
    try:
        bucket = storage_client.bucket(OUTPUT_BUCKET_NAME)
        # List only .md files
        blobs = bucket.list_blobs()
        files = [blob.name for blob in blobs if blob.name.endswith('.md')]
        
        if not files:
            return "No reports found."
        
        return "Available reports:\n" + "\n".join(files)
    except Exception as e:
        return f"Error accessing reports: {str(e)}"

def read_inspection_report(filename: str) -> str:
    """Reads the contents of a specific Markdown inspection report from GCS."""
    try:
        bucket = storage_client.bucket(OUTPUT_BUCKET_NAME)
        blob = bucket.blob(filename)
        
        if not blob.exists():
            return f"Error: '{filename}' not found in {OUTPUT_BUCKET_NAME}."
            
        return blob.download_as_text()
    except Exception as e:
        return f"Error reading report: {str(e)}"