# multi-agent-AI-system
## What task the agents collaborate on and why  chosing it :
The system automates end-to-end campaign asset creation ,specifically transforming a raw, high-level product description into a structured market research brief.
This task is a perfect use case for multi-agent collaboration because:
It splits a complex, multi-step job into specialized roles (researching, writing, and editing).
It utilizes an adversarial feedback loop (Writer vs. Critic) to guarantee quality, mimicking a real-world agency where creative output must meet strict editorial standards before publication.

## Each agent's role, inputs, outputs, and tools: 
1.reasercher :Uncovers market facts, audience insights, and competitor details , inputs A raw product description and outputs A JSON object containing: target_audience, pain_points (list), and marketing_angle using tool "tavily_search_tool: A custom Python function allowing web search" .
2. writer :Drafts highly engaging social copy , inputs The Researcher's JSON brief AND any active feedback from the Critic. outputs A JSON object containing: linkedin_post and email_copy
3. Critic :Acts as a strict chief editor to evaluate the writer’s work against the research brief. inputs The Researcher's JSON brief AND the Writer's latest draft. outputs A JSON object containing: approved (boolean) and feedback (string).
## How agents communicate : 
Because this pipeline is orchestrated via standard Python code, agents communicate by passing structured JSON strings back and forth.
The format: Standard JSON schemas are used at every hand-off.
How information flows:

The Researcher returns a JSON block. Python parses this string using json.loads().

The parsed dictionary is then converted back into a formatted string using json.dumps() and injected directly into the Writer's prompt context alongside the current critique string.

The Writer's generated JSON response is similarly loaded and dumped directly into the Critic's evaluation prompt.

The Critic's JSON response is parsed to inspect the "approved" boolean. If False, the "feedback" string is stored, updating the critic_feedback variable for the next round.

## How to run: 
necessary installations : pip install google-genai tavily-client python-dotenv rich
Set Up Environment Variables
Create a file named .env in the same directory as the script and insert the API keys:

GEMINI_API_KEY=XXXXXXXXXXXXXXXX
TAVILY_API_KEY=XXXXXXXXXXXXXXXX

then run : "python agent.py"

## The tools, models, or frameworks relied on :
LLM Engine: gemini-2.5-flash (chosen for its exceptionally fast response times, high context window, low cost, and reliable structural JSON adherence).

AI Orchestration Platform: Google GenAI SDK (specifically utilizing the modern google.genai client and types.GenerateContentConfig for tool definitions).

Search Engine Tool: Tavily API (via TavilyClient) to query the web and gather clean, parsed, developer-friendly Markdown content rather than messy raw HTML.

Environment Management: python-dotenv to safely inject system variables from the local .env file.

Terminal UI: rich to display colored and formatted JSON print outputs natively in the CLI.

## Challenges :
*Lack of Conversational Context : building a conversation thread of previous messages ,so the model sees the progression of drafts and feedback.
*Tool Execution Failures : tavily_search_tool If Tavily's API keys expire, or their servers face downtime, the function will catch the error and return the string "Error executing search tool: ..." to Gemini.
Gemini doesn't know this is a crash. It treats the error string as the actual search result and tries to write its research brief based on the words "Error executing search tool" .This leads to poor, confused marketing briefs.
JSON Formatting & Parsing Failures

if i had more time i would try to use frameworks like LangGraph , Use Pydantic to enforce schemas and fix the JSON format failure problem ,Provide the full iteration history so the model sees the progression of drafts and feedback.

## DEMO : 
input : "An AI-powered calendar app that automatically declines low-priority meetings for software engineers based in 2026."
<img width="1366" height="731" alt="multi-agent2" src="https://github.com/user-attachments/assets/2e6be752-3c75-49bf-b340-84c5ea1185af" />
<img width="1366" height="728" alt="multi-agents" src="https://github.com/user-attachments/assets/9a6593e1-af70-4fd7-93ff-84b94924a3d4" />
