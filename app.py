import os
import json
import threading
from flask import Flask
from zyndai_agent.agent import AgentConfig, ZyndAIAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_tavily import TavilySearch

# 1. IDENTITY SETUP
private_key = os.environ.get("ZYND_AGENT_PRIVATE_KEY")
key_path = os.path.abspath("agent_keypair.json")
if private_key:
    with open(key_path, "w") as f:
        json.dump({"private_key": private_key}, f)
    os.environ["ZYND_AGENT_KEYPAIR_PATH"] = key_path

# 2. FLASK FOR RENDER HEALTH CHECK
app = Flask(__name__)


@app.route('/')
def health():
    return "OK", 200


# 3. ZYND AGENT SETUP
def run_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
    tools = [TavilySearch(max_results=3)]
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an elite Autonomous OSINT Investigator."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    executor = AgentExecutor(agent=create_tool_calling_agent(llm, tools, prompt), tools=tools)

    config = AgentConfig(
        name="osint-investigator",
        description="Autonomous OSINT Analyzer",
        category="security",
        webhook_host="0.0.0.0",
        webhook_port=5001,  # Agent runs on 5001
        registry_url="https://zns01.zynd.ai",
        auto_reconnect=True
    )
    zynd_agent = ZyndAIAgent(config)
    zynd_agent.set_langchain_agent(executor)
    zynd_agent.start()


if __name__ == "__main__":
    # Start Agent in background
    threading.Thread(target=run_agent, daemon=True).start()
    # Start Flask on Render's port
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)