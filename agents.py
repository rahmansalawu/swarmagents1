from swarm import Swarm, Agent
from typing import Optional
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure the API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# Initialize Swarm client (without passing api_key)
client = Swarm()

# Utility Functions for File Operations
def save_output(filename: str, content: str):
    """Save agent output to a text file."""
    os.makedirs("outputs", exist_ok=True)
    filepath = f"outputs/{filename}.txt"
    with open(filepath, "w", encoding='utf-8') as f:
        f.write(content)
    return f"Content saved to {filepath}"

def read_file(filename: str) -> str:
    """Read content from a file."""
    filepath = f"outputs/{filename}.txt"
    try:
        with open(filepath, "r", encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"File {filepath} not found"

# Agent Transfer Functions
def transfer_to_content_analyst():
    """Transfer control to the Content Analyst agent."""
    return content_analyst_agent

def transfer_to_audience_researcher():
    """Transfer control to the Audience Researcher agent."""
    return audience_researcher_agent

def transfer_to_perspective_strategist():
    """Transfer control to the Perspective Strategist agent."""
    return perspective_strategist_agent

def transfer_to_content_outliner():
    """Transfer control to the Content Outliner agent."""
    return content_outliner_agent

def transfer_to_content_writer():
    """Transfer control to the Content Writer agent."""
    return content_writer_agent

def transfer_to_editor():
    """Transfer control to the Editor agent."""
    return editor_agent

def transfer_to_compliance_officer():
    """Transfer control to the Compliance Officer agent."""
    return compliance_officer_agent

def transfer_to_final_preparer():
    """Transfer control to the Final Content Preparer agent."""
    return final_preparer_agent

# Step 1: Transcript Reviewer Agent
transcript_reviewer_agent = Agent(
    name="Transcript Reviewer",
    instructions="""You are a Transcript Reviewer. Your task:
1. Read and analyze the provided transcript
2. Create a detailed summary
3. You MUST save your output by calling: save_output('01_transcript_review', your_summary)
4. Explicitly confirm the save and state you're transferring to Content Analyst

Your output format must be:
{
    "Summary": "...",
    "Key Points": ["...", "..."],
    "Main Themes": ["...", "..."],
    "Notable Quotes": ["...", "..."]
}""",
    functions=[save_output, transfer_to_content_analyst]
)

# Step 2: Content Analyst Agent
content_analyst_agent = Agent(
    name="Content Analyst",
    instructions="""You are a Content Analyst. Your task:
1. Read the previous analysis: read_file('01_transcript_review')
2. Analyze deeply and create insights
3. You MUST save your output by calling: save_output('02_content_analysis', your_analysis)
4. Confirm save and transfer to Audience Researcher

Your output format must be:
{
    "Analysis": "...",
    "Key Insights": ["...", "..."],
    "Content Gaps": ["...", "..."],
    "Recommendations": ["...", "..."]
}""",
    functions=[read_file, save_output, transfer_to_audience_researcher]
)

# Step 3: Audience Researcher Agent
audience_researcher_agent = Agent(
    name="Audience Researcher",
    instructions="""You are an Audience Researcher. Your task:
1. Read previous analyses: read_file('02_content_analysis')
2. Define target audiences and their needs
3. You MUST save your output by calling: save_output('03_audience_research', your_research)
4. Confirm save and transfer to Perspective Strategist

Your output format must be:
{
    "Target Audiences": ["...", "..."],
    "Audience Needs": {"audience1": ["...", "..."], "audience2": ["...", "..."]},
    "Content Recommendations": ["...", "..."]
}""",
    functions=[read_file, save_output, transfer_to_perspective_strategist]
)

# Step 4: Perspective Strategist Agent
perspective_strategist_agent = Agent(
    name="Perspective Strategist",
    instructions="""You are a Perspective Strategist. Your task:
1. Read previous analyses: read_file('03_audience_research')
2. Develop unique content angles and strategy
3. You MUST save your output by calling: save_output('04_perspective_strategy', your_strategy)
4. Confirm save and transfer to Content Outliner

Your output format must be:
{
    "Content Angle": "...",
    "Strategic Approach": "...",
    "Key Messages": ["...", "..."],
    "Unique Insights": ["...", "..."]
}""",
    functions=[read_file, save_output, transfer_to_content_outliner]
)

# Step 5: Content Outliner Agent
content_outliner_agent = Agent(
    name="Content Outliner",
    instructions="""You are a Content Outliner. Your task:
1. Read previous strategy: read_file('04_perspective_strategy')
2. Create detailed content structure
3. You MUST save your output by calling: save_output('05_content_outline', your_outline)
4. Confirm save and transfer to Content Writer

Your output format must be:
{
    "Title": "...",
    "Introduction": ["...", "..."],
    "Main Sections": {
        "Section 1": ["...", "..."],
        "Section 2": ["...", "..."]
    },
    "Conclusion": ["...", "..."]
}""",
    functions=[read_file, save_output, transfer_to_content_writer]
)

# Step 6: Content Writer Agent
content_writer_agent = Agent(
    name="Content Writer",
    instructions="""You are a Content Writer. Your task:
1. Read the outline: read_file('05_content_outline')
2. Write the first complete draft
3. You MUST save your output by calling: save_output('06_first_draft', your_draft)
4. Confirm save and transfer to Editor

Your output format must be:
{
    "Title": "...",
    "Content": "... [full article text] ...",
    "Word Count": "...",
    "Key Takeaways": ["...", "..."]
}""",
    functions=[read_file, save_output, transfer_to_editor]
)

# Step 7: Editor Agent
editor_agent = Agent(
    name="Editor",
    instructions="""You are an Editor. Your task:
1. Read the draft: read_file('06_first_draft')
2. Edit for clarity, style, and coherence
3. You MUST save your output by calling: save_output('07_edited_content', your_edits)
4. Confirm save and transfer to Compliance Officer

Your output format must be:
{
    "Edited Content": "... [full edited text] ...",
    "Changes Made": ["...", "..."],
    "Style Improvements": ["...", "..."],
    "Quality Check": "..."
}""",
    functions=[read_file, save_output, transfer_to_compliance_officer]
)

# Step 8: Compliance Officer Agent
compliance_officer_agent = Agent(
    name="Compliance Officer",
    instructions="""You are a Compliance Officer. Your task:
1. Read edited content: read_file('07_edited_content')
2. Review for compliance and originality
3. You MUST save your output by calling: save_output('08_compliance_review', your_review)
4. Confirm save and transfer to Final Preparer

Your output format must be:
{
    "Compliance Status": "...",
    "Originality Check": "...",
    "Required Changes": ["...", "..."],
    "Approval Status": "..."
}""",
    functions=[read_file, save_output, transfer_to_final_preparer]
)

# Step 9: Final Content Preparer Agent
final_preparer_agent = Agent(
    name="Final Content Preparer",
    instructions="""You are a Final Content Preparer. Your task:
1. Read compliance review: read_file('08_compliance_review')
2. Implement final changes and prepare for publication
3. You MUST save your output by calling: save_output('09_final_content', your_final_version)
4. Confirm completion

Your output format must be:
{
    "Final Title": "...",
    "Abstract": "...",
    "Final Content": "... [complete final text] ...",
    "Publication Notes": ["...", "..."]
}""",
    functions=[read_file, save_output]
)

def run_content_pipeline(transcript: str):
    """
    Run the content pipeline with explicit tracking of each step.
    """
    os.makedirs("outputs", exist_ok=True)
    
    try:
        # Initialize pipeline with clear instructions
        messages = [{
            "role": "user",
            "content": f"""Analyze this transcript following these REQUIRED steps:
1. Create a structured analysis following the format in your instructions
2. Save your output using the save_output function
3. Explicitly confirm the save was successful
4. Transfer to the next agent in the pipeline

Transcript:
{transcript}"""
        }]
        
        # Run the initial agent and track the response
        current_agent = transcript_reviewer_agent
        for _ in range(9):  # Ensure all 9 steps are attempted
            response = client.run(
                agent=current_agent,
                messages=messages
            )
            
            # Update messages with the response
            messages.append({"role": "assistant", "content": response})
            
            # Get the next agent from the response (if any)
            if "next_agent" in response:
                current_agent = response["next_agent"]
            else:
                break
        
        # Return detailed pipeline results
        return {
            "status": "success",
            "message": "Pipeline completed successfully",
            "output_directory": "outputs",
            "files": sorted(os.listdir("outputs")) if os.path.exists("outputs") else [],
            "final_response": response
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Example usage:
# transcript = "Transcript:(00:01) OBVIOUSLY, MATT GAETZ IS NO LONGER A CABINET NOMINEE. HE IS ALSO NOT A CURRENT MEMBER OF THE HOUSE OF REPRESENTATIVES, HAVING RESIGNED. IF YOU WERE STILL CHAIRING THIS COMMITTEE, HOW WOULD YOU MOVE FORWARD? >> I WANT TO SAY THERE IS PRECEDENT TO RELEASING COMMITTEE REPORTS AFTER A MEMBER HAS RESIGNED"
# final_response = run_content_pipeline(transcript)