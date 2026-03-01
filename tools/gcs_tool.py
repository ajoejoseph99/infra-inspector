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
        
        # Get the base name without any extension
        base_name = filename.split('.')[0]
        
        # Only add the suffix if it isn't already there
        if not base_name.endswith("_inspection"):
            clean_name = f"{base_name}_inspection.md"
        else:
            clean_name = f"{base_name}.md"
            
        blob = bucket.blob(clean_name)
        blob.upload_from_string(report_content, content_type="text/markdown")
        
        return f"Success: Report saved as {clean_name} in {OUTPUT_BUCKET_NAME}."
    except Exception as e:
        return f"Error saving report: {str(e)}"
