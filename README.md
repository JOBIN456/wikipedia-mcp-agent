# 🚀 FastAPI + FastMCP + LangChain Wikipedia Agent

An AI-powered Wikipedia research agent demonstrating how **FastAPI, FastMCP, LangChain, and LangGraph** can work together to build a modular tool-using AI application.

The project exposes Wikipedia capabilities through an **MCP (Model Context Protocol) server** and allows a LangChain/LangGraph agent to automatically discover and use those tools.

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │       User           │
                    │   Natural Language   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │    Application API   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   LangChain Agent    │
                    │      LangGraph       │
                    └──────────┬───────────┘
                               │
                         MCP Protocol
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastMCP         │
                    │     MCP Server       │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
             ┌──────────────┐      ┌──────────────┐
             │   Wikipedia  │      │   Wikipedia  │
             │    Search    │      │     Page     │
             └──────────────┘      └──────────────┘
```

---

## ✨ Features

* 🤖 LLM-powered Wikipedia research
* 🔌 Model Context Protocol (MCP) integration
* ⚡ FastAPI application layer
* 🧠 LangChain agent integration
* 🔄 LangGraph ReAct agent
* 🔎 Wikipedia search tool
* 📄 Wikipedia page retrieval tool
* 🔗 MCP tool discovery
* 📡 stdio-based MCP communication
* 🧩 Modular architecture that can easily support additional tools

---

## 🛠️ Tech Stack

| Technology         | Purpose                            |
| ------------------ | ---------------------------------- |
| Python             | Core programming language          |
| FastAPI            | API/application layer              |
| FastMCP            | MCP server and tool implementation |
| LangChain          | LLM and tool integration           |
| LangGraph          | Agent workflow                     |
| Requests           | Wikipedia API requests             |
| Wikipedia REST API | External knowledge source          |

---


## 🔧 MCP Tools

The FastMCP server exposes two tools.

### `search_wikipedia`

Searches Wikipedia for a given topic.

```python
@mcp.tool
def search_wikipedia(query: str):
    ...
```

Example:

```text
Search Wikipedia for Albert Einstein
```

The agent can automatically decide to call:

```text
search_wikipedia("Albert Einstein")
```

---

### `get_wikipedia_page`

Retrieves the content of a specific Wikipedia page.

```python
@mcp.tool
def get_wikipedia_page(title: str):
    ...
```

Example:

```text
Get the Wikipedia page for Artificial Intelligence
```

The agent can call:

```text
get_wikipedia_page("Artificial Intelligence")
```

---

## 🔄 How MCP Works in This Project

The MCP server runs using:

```python
mcp.run(transport="stdio")
```

The LangChain client connects to the MCP server:

```python
client = MultiServerMCPClient(
    {
        "wikipedia": {
            "command": "python",
            "args": ["server.py"],
            "transport": "stdio",
        }
    }
)
```

The client then discovers the available MCP tools:

```python
tools = await client.get_tools()
```

These tools are passed to the LangGraph agent:

```python
agent = create_react_agent(
    model,
    tools
)
```

The LLM can then decide which tool to use based on the user's request.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/langchain-mcp-wikipedia.git
```

```bash
cd langchain-mcp-wikipedia
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
```


## 🧠 Why MCP?

Traditional tool integration often tightly couples an LLM application with individual APIs.

MCP provides a standardized way to expose capabilities as tools.

```text
LLM
 │
 ▼
LangChain / LangGraph
 │
 ▼
MCP Client
 │
 ▼
MCP Server
 │
 ├── Wikipedia
 ├── Search
 ├── Database
 ├── APIs
 └── Custom Tools
```

This separation makes tools reusable across different AI applications and agents.

---

## 📌 Key Concepts Demonstrated

This project is useful for learning:

* Model Context Protocol (MCP)
* FastMCP
* MCP servers
* MCP clients
* stdio transport
* LangChain tool integration
* LangGraph agents
* ReAct agents
* FastAPI
* External API integration
* LLM tool calling
* Modular AI agent architecture
