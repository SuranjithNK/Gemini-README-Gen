import os
import glob
from google import genai
from google.genai.errors import APIError

def get_repo_structure():
    """Scans the repository and returns a string representation of the file structure."""
    
    # Exclude common build/config directories and the .git folder
    ignore_patterns = ['.git', '__pycache__', 'node_modules', '.github', '.venv', '*.log']
    
    structure = "Repository File Structure and Content Snippets:\n\n"
    
    for root, dirs, files in os.walk('.'):
        # Exclude ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_patterns]
        
        level = root.count(os.sep)
        indent = '  ' * level
        
        # Add directory to structure
        structure += f"{indent}📦 {os.path.basename(root)}/\n"
        
        for f in files:
            if not any(pat in f for pat in ignore_patterns):
                file_path = os.path.join(root, f)
                structure += f"{indent}  📄 {f}\n"
                
                # For a few key files, include content snippets for context
                if f in ['package.json', 'requirements.txt', 'Dockerfile']:
                    try:
                        with open(file_path, 'r') as file:
                            content = file.read(500) # Read up to 500 characters
                            structure += f"{indent}    (Snippet: {content.strip()[:100]}...)\n"
                    except Exception as e:
                        structure += f"{indent}    (Error reading file: {e})\n"
                        
    return structure

def generate_readme_content(repo_context, api_key):
    """Calls the Gemini API to generate the README content."""
    
    if not api_key:
        print("Error: GEMINI_API_KEY is not set.")
        return "# Error: API Key Missing"

    try:
        # Initialize the Gemini client
        client = genai.Client(api_key=api_key)

        prompt = (
            "You are an expert GitHub documentation writer. Your task is to generate a detailed "
            "and professional README.md file in Markdown format for the following repository. "
            "Analyze the structure and snippets provided to determine the project's language, purpose, "
            "and necessary setup steps. Do not include a 'Contributing' or 'License' section "
            "as they are already handled by GitHub. Focus on a strong title, a clear overview, "
            "and practical usage instructions. The generated README should replace the existing one.\n\n"
            "--- REPOSITORY CONTEXT ---\n"
            f"{repo_context}\n"
            "--------------------------\n\n"
            "Generate the full Markdown content for the new README.md now:"
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',  # A fast and capable model for text generation
            contents=prompt,
        )
        
        # Strip any leading/trailing markdown fences if the model adds them
        content = response.text.strip()
        if content.startswith('```markdown') and content.endswith('```'):
             content = content[12:-3].strip()

        return content

    except APIError as e:
        print(f"Gemini API Error: {e}")
        return f"# Error Calling Gemini API\n\nDetails: {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"# An Unexpected Error Occurred\n\nDetails: {e}"


def main():
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        print("GEMINI_API_KEY environment variable not found. Skipping README generation.")
        return

    print("1. Scanning repository structure...")
    repo_context = get_repo_structure()
    
    print("2. Generating README content via Gemini...")
    new_readme_content = generate_readme_content(repo_context, api_key)
    
    # Check if the generated content is an error message or valid Markdown
    if new_readme_content and not new_readme_content.startswith("# Error"):
        # Write the new content to the README.md file in the root
        with open('README.md', 'w') as f:
            f.write(new_readme_content)
        print("✅ Successfully generated and updated README.md")
    else:
        print("❌ Failed to generate README. See logs for error details.")

if __name__ == "__main__":
    main()

