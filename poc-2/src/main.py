import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

app = FastAPI(title="Python Calculator Hosted Agent")

# Define request/response models conforming to the Responses protocol
class AgentRequest(BaseModel):
    input: str
    session_id: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    output_text: str

def calculate(expression: str) -> str:
    """Evaluates a basic mathematical expression safely."""
    # Restrict characters allowed for basic math safety
    allowed_chars = set("0123456789+-*/(). ")
    if not all(c in allowed_chars for c in expression):
        return "Error: Invalid characters in mathematical expression."
    try:
        # Evaluate safely using Python's built-in evaluator for basic math
        result = eval(expression, {"__builtins__": {}}, {})
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error performing calculation: {str(e)}"

@app.post("/responses", response_model=AgentResponse)
async def handle_responses(req: AgentRequest):
    user_input = req.input.strip()
    
    # Simple keyword/intent parsing or you can plug in an LLM client 
    # connected via aiProject environment variables.
    if "calculate" in user_input.lower() or any(op in user_input for op in ["+", "-", "*", "/"]):
        # Extract expression or pass text directly if it's purely mathematical
        # For this example, let's assume the user typed a raw expression or prompt like "calculate 45 * 2"
        # A lightweight parsing logic:
        expression_candidate = "".join([c for c in user_input if c in set("0123456789+-*/(). ")])
        
        if expression_candidate.strip():
            answer = calculate(expression_candidate.strip())
            return AgentResponse(output_text=answer)

    # Default fallback / conversational response
    return AgentResponse(
        output_text=(
            f"Hello! I am your Python calculation agent deployed on Microsoft Foundry. "
            f"You asked: '{user_input}'. Try asking me to calculate something, like '150 * 4 + 20'."
        )
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Foundry hosted agents listen on port 8088 locally during `azd ai agent run`
    port = int(os.environ.get("PORT", 8088))
    uvicorn.run(app, host="0.0.0.0", port=port)