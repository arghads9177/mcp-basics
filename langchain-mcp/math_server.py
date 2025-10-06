# A MCP server containing math tools
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math MCP")

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract two numbers."""
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        return float("inf")
    return a / b

@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Raise a number to a power."""
    return base ** exponent

@mcp.tool()
def sqrt(value: float) -> float:
    """Calculate the square root of a number."""
    if value < 0:
        return float("nan")
    return value ** 0.5

# The transport="stdio" argument tells the server to:

# Use standard input/output (stdin and stdout) to receive and respond to tool function calls.
if __name__ == "__main__":
    mcp.run(transport="stdio")