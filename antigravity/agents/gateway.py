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
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
    def generate_response(self, agent_instance: Agent, prompt: str, **kwargs) -> str:
        """
        Accepts dynamic execution parameters (like image payload data buffers).
        """
        # Capture optional image bytes sent from multimodal channels
        uploaded_image = kwargs.get("image", None)

        if self.api_key:
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
        # Note: Standard Ollama generation endpoint handles text-fallback processing
        url = "http://localhost:11434/api/generate"
        payload = {"model": "gemma4", "prompt": prompt, "stream": False}
        try:
            response = httpx.post(url, json=payload, timeout=30.0)
            return response.json().get("response", "Gateway routing failure.")
        except Exception as err:
            return f"Critical Engine Error: Both Cloud ADK and Local Fallback channels are offline. ({err})"

gateway = LLMGateway()