from google.adk.agents import LlmAgent
from tools import list_inspection_reports, read_inspection_report

root_agent = LlmAgent(
    name="infrastructure_query_assistant",
    model="gemini-2.5-flash",
    tools=[list_inspection_reports, read_inspection_report],
    instruction=(
        "You are an intelligent assistant for a facilities management team. "
        "1. Use `list_inspection_reports` to find available Markdown files. "
        "2. Use `read_inspection_report` to read the exact details of a file. "
        "3. Summarize the findings clearly, noting any high-severity hazards."
    )
)