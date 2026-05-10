import os
from dotenv import load_dotenv
from zyndai_agent.agent import AgentConfig, ZyndAIAgent
from zyndai_agent.ed25519_identity import Keypair # Add this import
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_tavily import TavilySearch

load_dotenv()

# 1. Setup Gemini + Tools
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
tools = [TavilySearch(max_results=3)]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an elite Autonomous OSINT Investigator. Analyze inputs for security threats and provide briefings."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

executor = AgentExecutor(agent=create_tool_calling_agent(llm, tools, prompt), tools=tools)

# 2. Render-Specific Identity & Port Configuration
port = int(os.environ.get("PORT", 5000))
private_key_str = os.environ.get("ZYND_AGENT_PRIVATE_KEY")

# Create the keypair object from the Render environment variable
agent_keypair = None
if private_key_str:
    agent_keypair = Keypair.from_private_key(private_key_str)
    print("✅ Identity loaded from Environment Variable")

config = AgentConfig(
    name="osint-investigator",
    description="Autonomous OSINT Analyzer",
    category="security",
    tags=["osint", "cybersecurity"],
    webhook_host="0.0.0.0",
    webhook_port=port,
    registry_url="https://zns01.zynd.ai",
    auto_reconnect=True,
    keypair=agent_keypair # <--- This tells the SDK exactly who we are!
)

# 3. Initialize
zynd_agent = ZyndAIAgent(config)
zynd_agent.set_langchain_agent(executor)

print(f"🚀 OSINT Agent booting on port {port}...")
zynd_agent.start()