import os
import json
from dotenv import load_dotenv
from zyndai_agent.agent import AgentConfig, ZyndAIAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_tavily import TavilySearch

load_dotenv()

# 1. THE RENDER KEY FIX (Nuclear Option)
private_key = os.environ.get("ZYND_AGENT_PRIVATE_KEY")
key_path = os.path.abspath("agent_keypair.json")

if private_key:
    # Create the actual JSON file the SDK expects
    with open(key_path, "w") as f:
        json.dump({"private_key": private_key}, f)

    # FORCE the environment variable so the SDK finds it globally
    os.environ["ZYND_AGENT_KEYPAIR_PATH"] = key_path
    print(f"✅ Keypair forced to environment at: {key_path}")

# 2. Setup Gemini + Tools
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
tools = [TavilySearch(max_results=3)]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an elite Autonomous OSINT Investigator."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

executor = AgentExecutor(agent=create_tool_calling_agent(llm, tools, prompt), tools=tools)

# 3. Port Configuration
port = int(os.environ.get("PORT", 5000))

# We leave keypair out of AgentConfig because we forced the ENV variable above
config = AgentConfig(
    name="osint-investigator",
    description="Autonomous OSINT Analyzer",
    category="security",
    tags=["osint", "cybersecurity"],
    webhook_host="0.0.0.0",
    webhook_port=port,
    registry_url="https://zns01.zynd.ai",
    auto_reconnect=True
)

# 4. Initialize
zynd_agent = ZyndAIAgent(config)
zynd_agent.set_langchain_agent(executor)

# --- ADD THIS PART TO PASS RENDER HEALTH CHECK ---
@zynd_agent.webhook_app.route('/')
def health_check():
    return "Agent is Online", 200
# ------------------------------------------------

print(f"🚀 OSINT Agent booting on port {port}...")
zynd_agent.start()