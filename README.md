# multi-agent-AI-system
# Multi-Agent AI Marketing Campaign System

An automated, cooperative multi-agent system designed to turn raw product concepts into highly targeted marketing assets using real-time search and an iterative editorial loop.

##  Overview
The system automates **end-to-end campaign asset creation**, specifically transforming a raw, high-level product description into a structured market research brief, LinkedIn post, and email campaign.

### Why Multi-Agent ?
* **Specialized Division of Labor:** It splits a complex, multi-step job into highly focused, specialized roles (researching, writing, and editing).
* **Adversarial Feedback Loop:** It utilizes a Writer vs. Critic dynamic to guarantee quality, closely mimicking a real-world agency where creative output must meet strict editorial standards before publication.

##  Agent Architecture & Roles

| Agent | Core Role | Inputs | Outputs | Specialized Tools |
| :--- | :--- | :--- | :--- | :--- |
| **1. Researcher** | Uncovers market facts, target audience insights, and competitor details. | Raw product description | JSON containing: `target_audience`, `pain_points` (list), `marketing_angle` | **`tavily_search_tool`**: A custom Python web search tool. |
| **2. Writer** | Drafts highly engaging social copy and structured emails. | Researcher's JSON brief **AND** any active feedback from the Critic | JSON containing: `linkedin_post`, `email_copy` | *None (creative reasoning)* |
| **3. Critic** | Acts as a strict chief editor to evaluate copy against the research brief. | Researcher's JSON brief **AND** the Writer's latest draft | JSON containing: `approved` (boolean), `feedback` (string) | *None (strict evaluation)* |

---

## Agent Communication & Data Flow

Because this pipeline is orchestrated via standard Python code, agents communicate by passing **structured JSON strings** back and forth using standard JSON schemas at every hand-off.

### How Information Flows:
1. **The Research Phase:** The Researcher returns a JSON block. Python parses this string using `json.loads()`.
2. **The Creative Phase:** The parsed dictionary is converted back into a formatted string using `json.dumps()` and injected directly into the Writer's prompt context alongside the current critique string.
3. **The Editorial Phase:** The Writer's generated JSON response is similarly loaded and dumped directly into the Critic's evaluation prompt.
4. **The Decision Loop:** The Critic's JSON response is parsed to inspect the `"approved"` boolean:
   * **If `False`:** The `"feedback"` string is stored, updating the `critic_feedback` variable, and the loop triggers the Writer for a revised draft.
   * **If `True`:** The loop terminates and the final assets are approved.

##  Frameworks and tools :

* **LLM Engine:** `gemini-2.5-flash` (chosen for its exceptionally fast response times, high context window, low cost, and reliable structural JSON adherence).
* **AI Orchestration:** Google GenAI SDK (utilizing the modern `google.genai` client and `types.GenerateContentConfig` for tool definitions).
* **Search Engine Tool:** Tavily API (via `TavilyClient`) to query the web and gather clean, parsed, developer-friendly Markdown content rather than messy raw HTML.
* **Environment Management:
* **Terminal UI:** `rich` to display colored and formatted JSON print outputs natively in the CLI.


##  Getting Started & How to Run

### 1. Install Dependencies

pip install google-genai tavily-client python-dotenv rich
Set Up Environment Variables
Create a file named .env in the same directory as the script and insert the API keys:

GEMINI_API_KEY=XXXXXXXXXXXXXXXX
TAVILY_API_KEY=XXXXXXXXXXXXXXXX

then run : "python agent.py"

## Challenges :
Lack of Conversational Context: The current model lacks a rolling conversation thread of previous messages, making it harder for the model to see the step-by-step progression of drafts and feedback over multiple loops.

Tool Execution Failures (tavily_search_tool): If Tavily's API keys expire or their servers face downtime, the function catches the error and returns "Error executing search tool: ...". Gemini doesn't realize this is a system crash; it treats the error string as factual search context, leading to poor, confused marketing briefs.

JSON Formatting & Parsing Failures: Relying on raw string conversions can occasionally cause code execution breaks if the model returns malformed JSON brackets.

if i had more time i would try to use frameworks like LangGraph , Use Pydantic to enforce schemas and fix the JSON format failure problem ,Provide the full iteration history so the model sees the progression of drafts and feedback.

## DEMO : 
input : "An AI-powered calendar app that automatically declines low-priority meetings for software engineers based in 2026."
<img width="1366" height="731" alt="multi-agent2" src="https://github.com/user-attachments/assets/2e6be752-3c75-49bf-b340-84c5ea1185af" />
<img width="1366" height="728" alt="multi-agents" src="https://github.com/user-attachments/assets/9a6593e1-af70-4fd7-93ff-84b94924a3d4" />
