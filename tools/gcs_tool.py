import google.auth
from google.cloud import storage

# Dynamically get the project ID from the environment
_, PROJECT_ID = google.auth.default()

# Define the base bucket name and append the Project ID
OUTPUT_BUCKET_NAME = f"school-infra-reports-cv-{PROJECT_ID}"

storage_client = storage.Client()

def save_markdown_report(filename: str, report_content: str) -> str:
    """Saves the generated Markdown inspection report to Cloud Storage."""
    try:
        bucket = storage_client.bucket(OUTPUT_BUCKET_NAME)
        
        # Ensure a clean .md extension
        clean_name = filename.split('.')[0] + "_inspection.md"
        blob = bucket.blob(clean_name)
        
        # Upload the markdown content
        blob.upload_from_string(report_content, content_type="text/markdown")
        
        return f"Success: Report saved as {clean_name} in {OUTPUT_BUCKET_NAME}."
    except Exception as e:
        return f"Error saving report: {str(e)}"