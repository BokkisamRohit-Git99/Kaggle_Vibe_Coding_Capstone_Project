import os
import httpx
import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

class LLMGateway:
    """
    Manages cloud-to-local fallback routing with complete multimodal data support.
    If Google AI Studio keys fail, requests fallback seamlessly to local Ollama nodes.
    """
    def __init__(self):
        # DO NOT cache the key as a static property here anymore.
        pass
        
    def generate_response(self, agent_instance: Agent, prompt: str, **kwargs) -> str:
        """
        Accepts dynamic execution parameters (like image payload data buffers).
        """
        # DYNAMIC LOOKUP: Fetch the key at execution time to grab the user's frontend input
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        # Sanitize ghost strings or empty strings committed to git templates
        if api_key:
            api_key = api_key.strip()
            if api_key in ["", "google_api_key", "YOUR_API_KEY", "YOUR_API_KEY_HERE"]:
                api_key = None

        # Capture optional image bytes sent from multimodal channels
        uploaded_image = kwargs.get("image", None)

        if api_key:
            try:
                runner = InMemoryRunner(agent=agent_instance, app_name="agri_health_gateway")
                
                session = asyncio.run(runner.session_service.create_session(
                    app_name="agri_health_gateway", 
                    user_id="streamlit_user"
                ))
                
                # Create a dynamic collection of parts for the multimodal payload array
                parts_list = [types.Part.from_text(text=prompt)]
                
                # If an image payload exists, convert it directly to inline bytes 
                if uploaded_image is not None:
                    # Streamlit UploadedFile provides .getvalue() for raw bytes
                    image_bytes = uploaded_image.getvalue()
                    
                    # Track explicit MIME type based on the upload metadata
                    mime_type = uploaded_image.type if hasattr(uploaded_image, "type") else "image/jpeg"
                    
                    # Convert raw memory buffer to a valid Gemini binary block
                    parts_list.append(
                        types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
                    )
                
                # Pack text and optional image elements together cleanly
                content = types.Content(
                    role="user",
                    parts=parts_list
                )
                
                response_text = ""
                for event in runner.run(user_id="streamlit_user", session_id=session.id, new_message=content):
                    if event.content and event.content.parts and event.content.parts[0].text:
                        response_text += event.content.parts[0].text
                
                if response_text.strip():
                    return response_text
                else:
                    raise ValueError("Empty response received from ADK cloud execution layer.")
                    
            except Exception as e:
                print(f"⚠️ Cloud execution failed: {e}. Initiating gateway fallback to Ollama...")
                return self._fallback_to_ollama(prompt)
        else:
            return self._fallback_to_ollama(prompt)

    def _fallback_to_ollama(self, prompt: str) -> str:
        # Resolve network paths contextually based on the hosting cloud environment
        if os.getenv("STREAMLIT_RUNTIME_ENV") == "cloud":
            url = os.getenv("REMOTE_OLLAMA_ENDPOINT", "http://coop-edge-node.local:11434/api/generate")
        else:
            url = "http://localhost:11434/api/generate"
            
        payload = {"model": "gemma4", "prompt": prompt, "stream": False}
        try:
            response = httpx.post(url, json=payload, timeout=30.0)
            return response.json().get("response", "Gateway routing failure.")
        except Exception as err:
            return f"Critical Engine Error: Both Cloud ADK and Local Fallback channels are offline. ({err})"

gateway = LLMGateway()