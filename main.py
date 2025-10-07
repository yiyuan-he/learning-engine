from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, tool, create_sdk_mcp_server
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Any

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))

# Helper function with the actual code execution logic
async def execute_student_code(code: str) -> dict[str, Any]:
    """Core logic to execute and test student code"""
    test_cases = [(0, 1), (3, 6), (5, 120)]
    results = []

    try:
        local_scope = {}
        exec(code, local_scope, local_scope)

        if "factorial" not in local_scope:
            results.append("No function named 'factorial' found. Define: def factorial(n):")
        else:
            factorial = local_scope["factorial"]

            all_passed = True
            for n, expected in test_cases:
                try:
                    result = factorial(n)
                    if result == expected:
                        results.append(f"factorial({n}) = {result}")
                    else:
                        results.append(f"factorial({n}) = {result}, expected {expected}")
                        all_passed = False
                except RecursionError:
                    results.append(f"factorial({n}) caused infinite recursion (missing base case?)")
                    all_passed = False
                    break
                except Exception as e:
                    results.append(f"factorial({n}) error: {str(e)}")
                    all_passed = False

            if all_passed:
                results.append("\nAll tests passed!")

        return {
            "content": [{
                "type": "text",
                "text": "\n".join(results)
            }]
        }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error executing code: {str(e)}"
            }]
        }

# Tool wrapper for the agent to use
@tool(
    name="run_student_code",
    description="Execute the student's factorial function against test cases and return results",
    input_schema={
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Python code containing the factorial function to test"
            }
        },
        "required": ["code"]
    }
)
async def run_student_code(args: dict[str, Any]) -> dict[str, Any]:
    """Tool wrapper that calls the helper function"""
    return await execute_student_code(args["code"])

tutor_server = create_sdk_mcp_server(
    name="tutor",
    version="1.0.0",
    tools=[run_student_code]
)

class CodeRequest(BaseModel):
    code:str 

@app.get("/")
async def root():
    return {"message": "Server running!"}

@app.post("/api/run")
async def run(request: CodeRequest):
    """Student manually runs their code to see test results"""
    result = await execute_student_code(request.code)

    text = result["content"][0]["text"]
    return {"result": text}

@app.post("/api/help")
async def help(request: CodeRequest):
    """Student asks for help, agent can run code and provide guidance"""
    options = ClaudeAgentOptions(
        mcp_servers={"tutor": tutor_server},
        allowed_tools=["mcp__tutor__run_student_code"],
        system_prompt="""You are a Socratic coding tutor teaching recursion.
        Your goal: Help students learn through questions and hints, not by giving answers.

        You can run their code to see what's failing. Use that to guide your questions.

        Examples:
        - "I see your code has infinite recursion. What would stop the function from calling itself forever?"
        - "Your base case returns the right value. Now how do we calculate factorial for numbers greater than 1?"
        """
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(
        f"Student needs help.\n\nTheir code:\n```python\n{request.code}\n```"
        )

        final_result = None
        async for message in client.receive_response():
            if hasattr(message, 'result'):
                final_result = message.result

        return {"response": final_result if final_result else "Sorry, I couldn't generate a response."}

class ReflectionRequest(BaseModel):
    code: str
    explanation: str

@app.post("/api/reflect")
async def reflect(request: ReflectionRequest):
    """Evaluate student's explanation of their solution"""
    options = ClaudeAgentOptions(
        system_prompt="""You are evaluating a student's understanding of their recursive factorial solution.

        Your job:
        1. Analyze their explanation for understanding of:
            - Base case (when recursion stops)
            - Recursive case (how it breaks down the problem)
            - How the results combine

        2. Respond with either:
            - If they show strong understanding: Praise them briefly, then give a challenge problem
            - If they have gaps: Ask a targeted follow-up question to address the gap

        Keep responses to 2-3 sentences. Be encouraging but push them to think deeper.
        """
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(
        f"""The student solved factorial with this code:
        ```python
        {request.code}

        Their explanation: "{request.explanation}"

        Evaluate their understanding and respond appropriately.
        """
        )

        final_result = None
        async for message in client.receive_response():
            if hasattr(message, 'result'):
                final_result = message.result

    return {"feedback": final_result if final_result else "Sorry, I couldn't evaluate your explanation."}
