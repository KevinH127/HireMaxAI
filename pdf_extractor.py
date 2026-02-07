import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
# Currently, 1.5 Pro is the best model for PDF/Vision tasks. 
# Change this to 'gemini-2.5-pro' if/when it becomes available to you.
MODEL_ID = "gemini-2.5-pro" 

SYSTEM_INSTRUCTION = """
    # ROLE
    You are a deterministic PDF-to-LaTeX conversion engine.

    # OBJECTIVE
    Convert the provided PDF document into LaTeX source code that reproduces the document EXACTLY.

    # STRICT REQUIREMENTS
    You MUST preserve everything exactly as it appears in the PDF.

    DO NOT summarize.
    DO NOT paraphrase.
    DO NOT rewrite.
    DO NOT correct grammar.
    DO NOT interpret meaning.
    DO NOT simplify formatting.
    DO NOT omit any content.

    # CONVERSION RULES
    1. Convert ALL visible content into LaTeX.
    - text
    - headings
    - paragraphs
    - fonts (bold, italic, underline, small caps, etc.)
    - spacing
    - alignment
    - margins
    - page breaks
    - columns
    - tables
    - lists
    - equations
    - symbols
    - footnotes
    - headers/footers
    - images/figures
    - captions
    - page numbers
    - charts/graphics (embed or include as images if needed)

    2. Maintain EXACT layout fidelity.
    - Same line breaks
    - Same page breaks
    - Same spacing
    - Same visual structure
    - Same positioning

    3. Math and formulas:
    - Use proper LaTeX math environments.
    - Preserve notation exactly.

    4. Tables:
    - Recreate using tabular/longtable with identical structure.

    5. Images:
    - Use \\includegraphics.
    - Preserve size and placement.

    6. Fonts and styling:
    - Match font sizes and styles using LaTeX commands or packages.

    7. If any element cannot be represented natively in LaTeX:
    - Reproduce it using the closest LaTeX equivalent or embed as an image.
    - NEVER remove it.

    8. Finally, ensure that the LaTeX code is able to compile with no errors. If errors occur, ONLY MAKE CHANGES TO THE ERROR
        - ensure that none of these changes affect the layout, format, or content  of the file
    
    # OUTPUT FORMAT
    Return ONLY valid LaTeX code.
    Do NOT include explanations.
    Do NOT include markdown.
    Do NOT include commentary.

    Start directly with:
    \\documentclass{article}

    End with:
    \\end{document}

    # SUCCESS CONDITION
    Compiling the LaTeX must produce a document that is visually indistinguishable from the original PDF.
"""

def main(pdf_path, api_key):
    client = genai.Client(api_key=api_key)

    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} not found.")
        return

    try:
        print(f"--- Step 1: Uploading '{pdf_path}' to Gemini ---")
        
        # Upload the file to Gemini
        # The API will process the PDF pages as visual/multimodal input
        file_ref = client.files.upload(
            file=pdf_path,
            config={'mime_type': 'application/pdf'}
        )
        
        print(f"File uploaded. URI: {file_ref.uri}")
        print(f"--- Step 2: Generating LaTeX with {MODEL_ID} ---")

        # Generate content
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[
                file_ref,
                "Convert this PDF document into LaTeX code."
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.0, # Deterministic
            )
        )

        # Output the raw result
        if response.text:
            output_filename = os.path.splitext(pdf_path)[0] + "_gemini.tex"
            
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            
            print(f"--- Success! ---")
            print(f"Raw LaTeX saved to: {output_filename}")
        else:
            print("Error: Model returned no text.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    API_KEY = os.getenv("GEMINI_API_KEY")
    pdf_file = 'KevinHuang_Resume2026.pdf'
    main(pdf_file, API_KEY)

