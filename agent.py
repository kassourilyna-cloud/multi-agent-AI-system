import json
import os
from google import genai
from google.genai import types
from tavily import TavilyClient
from dotenv import load_dotenv
from rich import print as rprint

# 1. Load Keys (Supports both your CLI exports and optional .env file)
load_dotenv()

# 2. Initialize Clients
gemini_client = genai.Client() 
tavily_client = TavilyClient() 
MODEL_ID = "gemini-2.5-flash"

def tavily_search_tool(query: str) -> str:
    """
    Searches the internet for information, target audience trends, or competitor insights.
    Args:
        query: The search engine query string.
    Returns:
        A string chunk containing clean web page context and snippets.
    """
    print(f" [Tool Execution] Searching Tavily for: '{query}'")
    try:
        # Performs a clean, optimized search extraction for AI models
        response = tavily_client.search(query=query, search_depth="basic", max_results=3)
        
        results = []
        for result in response.get("results", []):
            results.append(f"Source: {result['url']}\nContent: {result['content']}\n")
        return "\n".join(results) if results else "No clear web results found."
    except Exception as e:
        return f"Error executing search tool: {str(e)}"

RESEARCHER_PROMPT = """
You are a Professional Market Researcher. Your job is to research a product or market topic and output a highly specific marketing brief.
You have access to a web search tool. Use it to look up recent data or angles if the prompt requires it.

You MUST respond ONLY with a JSON object containing these exact keys:
{
  "target_audience": "Detailed description of who this campaign is targeting",
  "pain_points": ["Specific pain point 1", "Specific pain point 2"],
  "marketing_angle": "The unique competitive angle or hook to use"
}
"""

WRITER_PROMPT = """
You are a Creative Content Copywriter. Your goal is to draft copy based on a Researcher's brief and revise it if the Critic gives feedback.
Look closely at the 'Feedback to fix' field. If the critic rejected the previous draft, adapt your copy directly to fix their issues.

You MUST respond ONLY with a JSON object containing these exact keys:
{
  "linkedin_post": "An engaging post with a hook, body, and call to action",
  "email_copy": "A compelling email pitch matching the brief"
}
"""

CRITIC_PROMPT = """
You are a Strict Chief Marketing Editor. Your job is to compare the writer's campaign against the researcher's brief. 
Be highly selective. If the copy is too generic, doesn't address the specific audience pain points, or is boring, REJECT IT.

You MUST respond ONLY with a JSON object containing these exact keys:
{
  "approved": true or false (use exact JSON boolean true/false),
  "feedback": "If approved, say 'Perfect'. If false, give a numbered list of exactly what the writer needs to fix."
}
"""
#  The Multi-Agent Orchestration Loop
def run_campaign_pipeline(product_description):
    print("🚀 Initializing Content Marketing Team...")
    
    # Step 1: Researcher Agent (Runs once, uses Tavily)
    print("\n Step 1: Running Researcher Agent...")
    research_response = gemini_client.models.generate_content(
        model=MODEL_ID,
        contents=f"Analyze this product topic and find relevant user pain points: {product_description}",
        config=types.GenerateContentConfig(
            system_instruction=RESEARCHER_PROMPT,
            tools=[tavily_search_tool], # Gives Gemini the ability to execute the python tool
        
        )
    )
    
    clean_text = research_response.text.replace("```json", "").replace("```", "").strip()
    research_brief = json.loads(clean_text)
    print(" Researcher Brief Generated Successfully.")
    print(research_brief)
    # Initialize our collaboration feedback variables
    critic_feedback = "First draft. No feedback yet."
    current_draft = None
    max_rounds = 3
    
    # Step 2 & 3: The Writer  Critic Iteration Loop
    for round_idx in range(1, max_rounds + 1):
        print(f"\n COLLABORATION ROUND {round_idx} ")
        
        # Call the Writer
        print(" Writer is crafting/revising the copy...")
        writer_input = f"Market Brief: {json.dumps(research_brief)}\nFeedback to fix: {critic_feedback}"
        writer_response = gemini_client.models.generate_content(
            model=MODEL_ID,
            contents=writer_input,
            config=types.GenerateContentConfig(
                system_instruction=WRITER_PROMPT,
                response_mime_type="application/json"
            )
        )
        current_draft = json.loads(writer_response.text)
        
        # Call the Critic
        print(" Critic is analyzing the copy...")
        critic_input = f"Target Brief: {json.dumps(research_brief)}\nWriter's Draft: {json.dumps(current_draft)}"
        critic_response = gemini_client.models.generate_content(
            model=MODEL_ID,
            contents=critic_input,
            config=types.GenerateContentConfig(
                system_instruction=CRITIC_PROMPT,
                response_mime_type="application/json"
            )
        )
        critic_review = json.loads(critic_response.text)
        
        # Check Decision Branch
        if critic_review["approved"]:
            print("\n Campaign Approved by Chief Editor!")
            print("\n FINAL CAMPAIGN")
            rprint(current_draft)
            return current_draft
        else:
            print(f"Rejected by Critic! Feedback: {critic_review['feedback']}")
            critic_feedback = critic_review["feedback"]
            
    print("\nMaximum iterations reached. Returning latest draft version.")
    rprint(current_draft)
    return current_draft


# Run it!
if __name__ == "__main__":
    # Feel free to change this text to test your agents on different topics
    test_product = "An AI-powered calendar app that automatically declines low-priority meetings for software engineers based in 2026."
    run_campaign_pipeline(test_product)