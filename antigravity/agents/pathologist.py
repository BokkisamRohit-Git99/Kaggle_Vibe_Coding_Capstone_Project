from google.adk import Agent
from google.adk.tools import google_search
from antigravity.prompts.templates import PATHOLOGY_PROMPT
from antigravity.agents.gateway import gateway

adk_pathologist = Agent(
    name="BotanicalPathologist",
    model="gemini-2.5-flash",
    instruction="Identify plant pathogens, viruses, fungi, bacteria diseases and provide sustainable, long term biological remedies. Provide lists of biological pesticides with verified source links.",
    tools=[google_search]
)

def run_pathology_analysis(user_text: str, location: str = "", uploaded_image=None) -> str:
    # Handle missing or empty text variations safely
    cleaned_text = user_text.strip() if user_text else ""
    
    # If there's an image but no text description, supply context so the prompt templates format correctly
    if not cleaned_text and uploaded_image is not None:
        cleaned_text = "Please analyze this uploaded plant image sample to diagnose anomalies."
    elif not cleaned_text and not uploaded_image:
        return "Error: Neither a symptom description nor an image was provided."

    try:
        location_context = location if location else "Unknown/Global Location"
        formatted_prompt = PATHOLOGY_PROMPT.format(
            user_input=cleaned_text,
            location=location_context
        )

        # Handle Multimodal Execution safely
        if uploaded_image is not None:
            # Pass BOTH the structured prompt string and the media data wrapper to the gateway
            return gateway.generate_response(adk_pathologist, formatted_prompt, image=uploaded_image)
        else:
            # Text-only execution
            return gateway.generate_response(adk_pathologist, formatted_prompt)
            
    except Exception as e:
        return f"Error during pathology analysis: {str(e)}"