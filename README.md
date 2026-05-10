🛡️ Sentinel-OSINT: Autonomous Threat Intelligence Agent
An Entry for the Zynd AI / Aya Hackathon

🚀 Live Agent Details
A2A Endpoint: https://osnit-agent-zyndai.onrender.com/a2a/v1

Identity Card: https://osnit-agent-zyndai.onrender.com/.well-known/agent-card.json

Status: 🟢 Active & Cloud Hosted

🧠 Overview
Sentinel-OSINT is a fully autonomous cybersecurity intelligence agent built on the Zynd AI Framework. It acts as a specialized node in a decentralized agent network, providing real-time vulnerability research and threat analysis.

Unlike traditional chatbots, Sentinel-OSINT is a Headless AI Entity. It is built for Agent-to-Agent (A2A) collaboration, utilizing the JSON-RPC 2.0 protocol to exchange intelligence cryptographically signed by its own Ed25519 identity.

🛠️ Key Capabilities
Autonomous Reasoning: Powered by Gemini 1.5 Flash, the agent decomposes complex security queries into executable research steps via the zyndai-agent SDK.

Real-time OSINT Intelligence: Integrated with Tavily Search to bypass training data cutoffs, retrieving live CVE data and zero-day intelligence.

Self-Sovereign Identity: Operates with a unique ZNS Identity. All communications are authenticated via a private keypair managed through secure cloud environment variables.

Multi-Threaded Cloud Architecture: Implements a sidecar Flask process to maintain 100% Uptime on Render while the agent runs its core logic in a persistent background thread.

🧱 Technical Stack
Core SDK: zyndai-agent

LLM Orchestration: LangChain (Google Generative AI)

Search Engine: Tavily AI

Environment: Python 3.10+ / Render Cloud

Networking: Flask (Health Monitoring) + JSON-RPC (Agent Communication)

📡 How to Interact (For Judges/Developers)
This agent follows the JSON-RPC 2.0 standard. To interact, send a POST request to the /a2a/v1 endpoint.

Example Request (invoke method)
JSON
{
    "jsonrpc": "2.0",
    "method": "invoke",
    "params": {
        "input": "Analyze the latest critical vulnerabilities found in OpenSSL from the last 48 hours."
    },
    "id": 1
}
Discovery
Verify the agent's capabilities and public key by visiting the identity card:
https://osnit-agent-zyndai.onrender.com/.well-known/agent-card.json

🏗️ Local Development & Setup
To run a local instance:

Clone the repository:

Bash
git clone https://github.com/sufiyan-cyber/OSNIT_AGENT_ZYNDAI.git
cd OSNIT_AGENT_ZYNDAI
Install dependencies:

Bash
pip install -r requirements.txt
Environment Variables: Create a .env file with GOOGLE_API_KEY, TAVILY_API_KEY, and ZYND_AGENT_PRIVATE_KEY.

Run:

Bash
python app.py
Developed with ❤️ by Sufiyan Khan S
Pre-Final Year Engineering Student | Cybersecurity & AI Enthusiast
The Oxford College of Engineering, Bangalore
