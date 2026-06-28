import streamlit as st
import asyncio
from PIL import Image

# CRITICAL: Load environment variables BEFORE importing antigravity layers
from dotenv import load_dotenv
import os
load_dotenv()

# Import decoupled layers from the antigravity module
from antigravity.security.guardrails import run_input_guardrail  # Llama Guard 3 Layer
from antigravity.services.location import fetch_background_location
from antigravity.agents.pathologist import run_pathology_analysis
from antigravity.agents.finance import run_finance_analysis

# Page config layout configuration
st.set_page_config(page_title="Agri-Health-Finance Dashboard", layout="wide", page_icon="🌿")

st.title("🌿 Unified Agri-Health-Finance Dashboard")
st.caption("Decentralized Multi-Agent Workspace secured by Llama Guard 3 & Driven by Model Context Protocol.")

# Sidebar telemetry details
st.sidebar.header("📡 Automated Telemetry")
if "detected_location" not in st.session_state:
    with st.spinner("Resolving coordinates silently..."):
        st.session_state.detected_location = asyncio.run(fetch_background_location())

st.sidebar.success(f"Captured Target Region:\n**{st.session_state.detected_location}**")

# ============================================================================
# GOOGLE API KEY MANAGEMENT PERIMETER
# ============================================================================
st.sidebar.header("🔑 Authentication Gateway")
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input(
        "Enter Google API Key",
        type="password",
        help="Required to clear and execute cloud-backed agent pipelines when local channels are offline."
    )
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        st.sidebar.success("Key injected into active session runtime.")
else:
    st.sidebar.success("Authenticated via system environment variables.")

# ============================================================================
# STATE INITIALIZATION & REFRESH LOGIC (Clears old responses automatically)
# ============================================================================
if "pathology_results" not in st.session_state:
    st.session_state.pathology_results = None
if "financial_results" not in st.session_state:
    st.session_state.financial_results = None

# Layout columns for input interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🌾 Diagnostic Intake Portal")
    
    # Whenever a new file is uploaded, reset execution states to clear stale layouts
    uploaded_image = st.file_uploader(
        "Upload an image of the crop anomaly:", 
        type=["jpg", "jpeg", "png"],
        on_change=lambda: st.session_state.update({"pathology_results": None, "financial_results": None})
    )
    
    if uploaded_image:
        st.image(Image.open(uploaded_image), caption="👀 Live Preview: Target Sample Context", use_container_width=True)
        
    user_text = st.text_area(
        "Provide details regarding changes in pattern, soil, or behavior:", 
        placeholder="e.g., Circular rings forming on lower tomato canopy.",
        on_change=lambda: st.session_state.update({"pathology_results": None, "financial_results": None})
    )

# Execution Trigger
if st.button("Launch Multi-Agent Deep Execution", type="primary"):
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("❌ Critical Engine Error: Both Cloud ADK and Local Fallback channels are offline. Please input a valid Google API key in the sidebar to authenticate infrastructure pipelines.")
    elif not user_text and not uploaded_image:
        st.warning("Please provide a text description or upload a sample image to begin.")
    else:
        try:
            # Clean old response variables before processing a new query
            st.session_state.pathology_results = None
            st.session_state.financial_results = None
            
            # 1. Structural Security Engine Execution
            context_string = f"{user_text} [Image attached: {uploaded_image is not None}]"
            
            with st.spinner("🔒 Evaluating security profiles via Llama Guard 3..."):
                guard_status = run_input_guardrail(context_string)
                
            # Intercept execution if the input flags an exploit category
            if guard_status != "PASSED":
                st.error(f"🛑 {guard_status}")
                st.toast("Security Intervention triggered.", icon="🚨")
            else:
                st.toast("Security Cleared. Routing through MCP Client Tools...", icon="🛡️")
                
                # 2. Run Diagnostic Chain (Updated to cleanly pass the image payload)
                with st.spinner("🔬 Invoking Pathologist Model..."):
                    st.session_state.pathology_results = run_pathology_analysis(
                        user_text=user_text, 
                        location=st.session_state.detected_location,
                        uploaded_image=uploaded_image
                    )
                    
                # 3. Run Financial Sourcing Chain
                with st.spinner("💸 Analyzing Commodities & Fixing Index Insurance Metrics..."):
                    st.session_state.financial_results = run_finance_analysis(
                        st.session_state.pathology_results, 
                        st.session_state.detected_location
                    )
                    
        except ValueError as security_err:
            st.error(f"Security validation failure: {security_err}")
        except Exception as general_err:
            st.error(f"Execution processing error encountered: {general_err}")

# ============================================================================
# INTERACTIVE REPORTING CONTAINER LAYOUT (Renders only when responses exist)
# ============================================================================
if st.session_state.pathology_results and st.session_state.financial_results:
    with col2:
        st.subheader("📊 Network Diagnostic and Asset Optimization Brief")
        
        # Split reporting layout inside the active side screen column
        with st.expander("🩺 Botanical Diagnosis & Organic Remedies", expanded=True):
            st.markdown(st.session_state.pathology_results)
            
        with st.expander("📋 Insurance Strategy & Commodities Hedging", expanded=True):
            st.markdown(st.session_state.financial_results)
            
        # Display explicit structural liability disclaimers cleanly at the footer baseline
        st.markdown("---")
        st.caption("⚖️ **System Boundary Disclaimers:**")
        st.caption("1. **Agronomy:** Remedies and diagnostic insights are synthetic model summaries. Cross-verify with real field testing.")
        st.caption("2. **Finance:** Commodities sell targets, hedging rates, and micro-insurance estimates are simulated options and do not constitute professional financial advice.")