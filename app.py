import streamlit as st
from agents import run_content_pipeline
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

def display_file_contents(filepath):
    """Display file contents with proper formatting."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            st.code(content, language="text")  # Better formatting for output
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")

def display_pipeline_progress(files):
    """Display pipeline progress with file contents."""
    expected_files = [
        "01_transcript_review.txt",
        "02_content_analysis.txt",
        "03_audience_research.txt",
        "04_perspective_strategy.txt",
        "05_content_outline.txt",
        "06_first_draft.txt",
        "07_edited_content.txt",
        "08_compliance_review.txt",
        "09_final_content.txt"
    ]
    
    # Create columns for progress tracking
    cols = st.columns(len(expected_files))
    
    # Show progress for each expected file
    for i, expected_file in enumerate(expected_files):
        with cols[i]:
            if expected_file in files:
                st.success("✅")
            else:
                st.error("❌")
            st.write(f"Step {i+1}")

def main():
    st.title("AI Content Pipeline")
    
    with st.expander("ℹ️ Pipeline Steps", expanded=False):
        st.write("""
        1. Transcript Review
        2. Content Analysis
        3. Audience Research
        4. Perspective Strategy
        5. Content Outline
        6. First Draft
        7. Editing
        8. Compliance Review
        9. Final Content
        """)
    
    transcript = st.text_area(
        "Enter your transcript:",
        height=200,
        placeholder="Paste your transcript here..."
    )
    
    if st.button("Process Transcript"):
        if transcript.strip():
            try:
                progress_placeholder = st.empty()
                status_text = st.empty()
                
                # Process the transcript
                with st.spinner("Running AI pipeline..."):
                    result = run_content_pipeline(transcript)
                    
                    if result["status"] == "success":
                        st.success("✅ Pipeline completed!")
                        
                        # Show pipeline progress
                        display_pipeline_progress(result["files"])
                        
                        # Display outputs in order
                        st.subheader("📑 Pipeline Outputs")
                        if os.path.exists("outputs"):
                            files = sorted(os.listdir("outputs"))
                            for file in files:
                                with st.expander(f"📄 {file.replace('.txt', '')}"):
                                    display_file_contents(os.path.join("outputs", file))
                        
                        status_text.success("All outputs generated and displayed!")
                    else:
                        st.error(f"Pipeline failed: {result['message']}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a transcript first!")

if __name__ == "__main__":
    main() 