import os
import json
from dotenv import load_dotenv
from zyndai_agent.agent import AgentConfig, ZyndAIAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_tavily import TavilySearch

load_dotenv()

# 1. Setup Gemini + Tools
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
tools = [TavilySearch(max_results=3)]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an elite Autonomous OSINT Investigator. Analyze inputs for security threats."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

executor = AgentExecutor(agent=create_tool_calling_agent(llm, tools, prompt), tools=tools)

# 2. THE RENDER KEY FIX
# We create the file locally in the cloud so the SDK finds it
private_key = os.environ.get("ZYND_AGENT_PRIVATE_KEY")
key_path = os.path.join(os.getcwd(), "agent_keypair.json")

if private_key:
    with open(key_path, "w") as f:
        json.dump({"private_key": private_key}, f)
    print(f"✅ Keypair file generated at {key_path}")

# 3. Configuration
port = int(os.environ.get("PORT", 5000))

config = AgentConfig(
    name="osint-investigator",
    description="Autonomous OSINT Analyzer",
    category="security",
    tags=["osint", "cybersecurity"],
    webhook_host="0.0.0.0",
    webhook_port=port,
    registry_url="https://zns01.zynd.ai",
    auto_reconnect=True,
    keypair_path=key_path # <--- This tells the SDK exactly where to look
)

# 4. Initialize
zynd_agent = ZyndAIAgent(config)
zynd_agent.set_langchain_agent(executor)

print(f"🚀 OSINT Agent booting on port {port}...")
zynd_agent.start()