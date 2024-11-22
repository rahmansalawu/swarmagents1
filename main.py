from dotenv import load_dotenv
import os
from agents import run_content_pipeline

# Load environment variables from .env file
load_dotenv()

# Ensure the API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

def main():
    # Example transcript (replace with your actual transcript)
    transcript = """
    Transcript:
(00:01) OBVIOUSLY, MATT GAETZ IS NO LONGER A CABINET NOMINEE. HE IS ALSO NOT A CURRENT MEMBER OF THE HOUSE OF REPRESENTATIVES, HAVING RESIGNED. IF YOU WERE STILL CHAIRING THIS COMMITTEE, HOW WOULD YOU MOVE FORWARD? >> I WANT TO SAY THERE IS PRECEDENT TO RELEASING COMMITTEE REPORTS AFTER A MEMBER HAS RESIGNED
    """
    
    try:
        print("Starting content pipeline...")
        response = run_content_pipeline(transcript)
        print("Pipeline completed successfully!")
        print("Check the 'outputs' folder for generated files.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()