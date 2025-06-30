import requests
import sqlite3
import subprocess
from utils.email_utils import send_email

'''This script fetches the latest drug recall data from the FDA API, generates AI summaries using Ollama LLaMA3, 
and stores the data in a SQLite database. If new recalls are found, it sends an email alert with the details.'''

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
    
        
# Fetch the latest drug recall data from the FDA API (10 most recent recalls)
url = "https://api.fda.gov/drug/enforcement.json?sort=report_date:desc&limit=10"
# We use the requests library to fetch the data from the FDA API
response = requests.get(url)
# Make it into a JSON object
data = response.json()

# Connect to the SQLite database 
conn = sqlite3.connect('data/recalls.db')
# create the cursor object to execute SQL commands
cursor = conn.cursor()



#Insert the data into the database
results = data.get('results', [])
#Counter for inserted records
inserted = 0

#A list to store AI summaries for email alert. Each item is a tuple of (brand_name, ai_summary)
ai_summaries = []


# This for loop iterates through each recall in the results
# and attempts to insert it into the database.
for recall in results:
    try:
        # Generate AI summary for the reason for recall
        ai_summary = generate_ai_summary(recall.get('reason_for_recall'))

        # Insert the recall data into the database
        cursor.execute('''
            INSERT INTO recalls (recall_number, brand_name, generic_name, classification, reason_raw, reason_ai, recall_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            recall.get("recall_number"),
            # Use the first 120 characters of the product description
            recall.get("product_description", "").split(",")[0][:120],
            recall.get('generic_name'),
            recall.get('classification'),
            recall.get('reason_for_recall'),
            ai_summary,
            recall.get('report_date')
            
        ))

        # Append the brand name and AI summary to the list for email alert
        ai_summaries.append((recall.get("product_description", ""), ai_summary))

        #Update the inserted counter
        inserted += 1
    
    # If a duplicate record is found, skip it and print a message
    except sqlite3.Error as e:
        print(f"Skipped duplicate: {recall.get('recall_number')}")

# Commit the changes to the database
conn.commit()

# Print the number of records inserted
#conn.close()
print(f"Inserted {inserted} records into the database.")

conn.close()


# If new recalls were inserted, prepare and send the email alert
if inserted > 0:

    # Prepare the email body with the brand names and AI summaries
    # Each line will contain the brand name and the AI summary
    body_lines = [f"{brand}\nSummary: {summary}" for brand, summary in ai_summaries]

    # Join the lines with double newlines for better readability
    alert_body = "Hello this RX-Recall_Watch. Here are the latest recalls!\n\n" + "New recall(s) found:\n\n" + "\n---------------------\n".join(body_lines)
    # Send the email alert
    send_email(
        subject="New Drug Recall Alert",
        body=alert_body
    )

# If no new recalls were added, print a message
else:
    print("No new recalls added. No email sent.")
