"""
Smart Calculator API - FastAPI application.
Accepts expressions like x+y, x+y+z, or any format without spaces.
"""

import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Smart Calculator API")


class CalculateRequest(BaseModel):
    """Request body for the calculate endpoint."""

    calculate: str  # The expression to evaluate (e.g., "5+3", "10*2+5")


def calculate(expression: str) -> float:
    """
    Safely parse and evaluate a mathematical expression.
    Supports: +, -, *, /, parentheses, and decimal numbers.

    Args:
        expression: Math expression as string (e.g., "2+3", "10*2+5", "2+3+4")

    Returns:
        The computed result as a float.

    Raises:
        ValueError: If the expression contains invalid characters.
    """
    # Remove all spaces
    expr = expression.replace(" ", "").strip()

    if not expr:
        raise ValueError("Empty expression")

    # Security: only allow numbers and basic math operators
    if not re.match(r"^[\d\+\-\*\/\(\)\.]+$", expr):
        raise ValueError(
            "Invalid input: only numbers and operators (+, -, *, /) are allowed"
        )

    try:
        result = eval(expr)
        return float(result) if isinstance(result, (int, float)) else result
    except ZeroDivisionError:
        raise ValueError("Division by zero")
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")


@app.post("/calculate")
def calculate_endpoint(request: CalculateRequest):
    """
    Calculate a mathematical expression.
    Send the expression in the request body under the "calculate" key.
    """
    try:
        result = calculate(request.calculate)
        return {"expression": request.calculate, "result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def root():
    """Health check / API info."""
    return {
        "message": "Smart Calculator API",
        "docs": "/docs",
        "endpoint": "POST /calculate with body: {\"calculate\": \"5+3\"}",
    }
