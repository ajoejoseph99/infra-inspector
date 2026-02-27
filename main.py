from fastapi import FastAPI, Request
from google.adk.runners import InMemoryRunner
from google.genai import types
from google.cloud import storage
from inspector_agent import inspector

app = FastAPI()
storage_client = storage.Client()

@app.post("/")
async def eventarc_webhook(request: Request):
    headers = request.headers
    bucket_name = headers.get("ce-source").split("buckets/")[1]
    file_name = headers.get("ce-subject").split("objects/")[1]  
    
    # Ignore anything that isn't an image
    if not file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        return {"status": "Ignored non-image file"}

    # Download the raw image bytes into memory
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    image_bytes = blob.download_as_bytes()
    
    runner = InMemoryRunner(agent=inspector, app_name="infra_app")
    session_id = f"session-{file_name.replace('/', '-')}"
    
    # Create the multimodal payload
    user_message = types.Content(
        role="user", 
        parts=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            types.Part.from_text(text=f"Please inspect this infrastructure photo (filename: {file_name}) and save the markdown report.")
        ]
    )
    
    # Execute the agent workflow
    await runner.session_service.create_session(
        app_name="infra_app", user_id="webhook_system", session_id=session_id
    )
    async for event in runner.run_async(
        user_id="webhook_system", session_id=session_id, new_message=user_message
    ):
        print(f"Agent Action: {event}")
        
    return {"status": "Inspection complete"}