from google.adk.agents import LlmAgent
from tools import save_markdown_report

inspector = LlmAgent(
    name="infrastructure_inspector",
    model="gemini-3-flash-preview",
    tools=[save_markdown_report],
    instruction=(
        "You are an expert structural inspector assessing physical infrastructure. "
        "When provided with an image, analyze it for damage, safety hazards, or required upgrades. "
        "1. Generate a structured Markdown report with headers for: Observation, Severity (Low/Medium/High), and Recommended Fix. "
        "2. ALWAYS use the `save_markdown_report` tool to save your final formatted report."
    )
)
