import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Bypasses Meta's gate while keeping the native PyTorch structure
MODEL_ID = "project-free-llama/Llama-Guard-3-1B"

print("Initializing local un-gated Llama Guard 3 pipeline...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

# Determine the best concrete device available explicitly to avoid meta-tensor traps
device = "cuda" if torch.cuda.is_available() else "cpu"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16
).to(device) # Directly mount onto a clean, concrete device footprint

def run_input_guardrail(user_input: str) -> str:
    """
    Evaluates raw user string prompts against Llama Guard 3 taxonomy rules.
    Returns "PASSED" if safe, otherwise returns an explicit block error string.
    """
    messages = [
        {"role": "user", "content": user_input}
    ]
    
    # Formats the chat template using native MLCommons safety prompts
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt"
    ).to(device) # Send directly to the concrete device (e.g., 'cuda' or 'cpu')
    
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=10, pad_token_id=0)
        
    # Isolate newly predicted token strings
    generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
    verdict = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
    
    # Check for failure signature
    if "unsafe" in verdict.lower():
        return f"Security Boundary: Request blocked by Llama Guard 3. Code Classification: {verdict}"
        
    return "PASSED"