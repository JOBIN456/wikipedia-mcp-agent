import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain.agents import create_agent

from dotenv import load_dotenv

load_dotenv()
from schema import ChatRequest

app = FastAPI()

templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)





# Global agent
agent = None


async def initialize_agent():

    global agent

    # MCP client
    client = MultiServerMCPClient(
        {
            "wikipedia": {
                "command": "python",
                "args": ["server.py"],
                "transport": "stdio",
            }
        }
    )

    # Get MCP tools
    tools = await client.get_tools()

    print("Available tools:")

    for tool in tools:
        print("-", tool.name)

    # Groq model
    model = ChatGroq(
        model="qwen/qwen3.6-27b",
        temperature=0,
        reasoning_effort="none"
    )

    # Create agent
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=(
            "You are a Wikipedia assistant. "
            "Always use the Wikipedia tools to answer questions. "
            "Do not answer from your own knowledge."
        )
    )

    print("Agent initialized successfully.")


@app.on_event("startup")
async def startup():

    await initialize_agent()

@app.post("/chat")
async def chat(data: ChatRequest):

    message = data.message.strip()

    print("\n==============================")
    print("USER:", message)
    print("AGENT: starting...")
    print("==============================")

    if not message:
        return {
            "response": "Please enter a message."
        }

    print("AGENT: calling ainvoke...")

    response = await agent.ainvoke(
        {
            "messages": [
                ("user", message)
            ]
        }
    )

    print("AGENT: ainvoke completed")

    print("\nALL MESSAGES:")

    for i, msg in enumerate(response["messages"]):

        print(f"\n--- MESSAGE {i} ---")
        print("TYPE:", type(msg).__name__)

        if getattr(msg, "tool_calls", None):
            print("TOOL CALLS:", msg.tool_calls)

        print("CONTENT:", msg.content)

    final_answer = response["messages"][-1].content

    print("\nFINAL ANSWER:")
    print(final_answer)

    return {
        "response": final_answer
    }