from google.adk import Agent
from google.adk.tools import google_search
from antigravity.prompts.templates import FINANCIAL_PROMPT
from antigravity.agents.gateway import gateway

# Declaring the agent cleanly with zero custom function overhead
adk_finance = Agent(
    name="EcoFinanceArbitrageur",
    model="gemini-2.5-flash",
    instruction="Execute real-time commodity research and construct risk reports using google_search.",
    tools=[google_search]
)

def run_finance_analysis(diagnostic_data: str, location: str = "") -> str:
    """
    Formats the instructional template directly and ships it to the ADK execution engine.
    Accepts location data context to align seamlessly with app.py layout requirements.
    """
    # Guardrail: Do not execute or call the API if prior diagnostic steps failed or are empty
    if not diagnostic_data or "Error" in diagnostic_data:
        return "Error: Cannot calculate financial risk reports without valid pathology data."

    try:
        # Standardize the location fallback text string cleanly if empty
        location_context = location.strip() if (location and hasattr(location, "strip")) else "Unknown/Global Location"
        
        # Safely compile the structured prompt variables to execute the gate query
        formatted_prompt = FINANCIAL_PROMPT.format(
            diagnostic_data=diagnostic_data.strip(), 
            location=location_context
        )
        
        # Explicitly passing image=None ensures that Gateway.py's kwargs logic 
        # handles it safely as a text-only execution branch, matching pathologist structures.
        return gateway.generate_response(adk_finance, formatted_prompt, image=None)
        
    except Exception as e:
        # Prevent runtime crashes from downstream API/network failures
        return f"Error during financial analysis: {str(e)}"