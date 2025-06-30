import subprocess

# Function to generate AI summary using Ollama LLaMA3
def generate_ai_summary(text):
    #Runs Ollama LLaMA3 locally and returns a one-sentence summary.

    try:
        # Use subprocess to call Ollama with the given prompt
        prompt = f"Summarize this drug recall reason in one sentence, simply and clearly:\n{text}"
        
        # Call the Ollama command to generate the summary
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding ='utf-8',
            errors = "replace",
            check=True
        )
        # return the generated summary
        return result.stdout.strip()
    
    # Handle errors if Ollama command fails
    except subprocess.CalledProcessError as e:
        print("Ollama error:", e.stderr)
        return "AI summary failed"
    