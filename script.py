import os
import pandas as pd
import smtplib
from email.message import EmailMessage
from datetime import datetime
from google import genai
from google.genai import types

def generate_report():
    # 1. Initialize Gemini with Search Tool
    client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    prompt = f"""
    Search news for today ({today_date}) from The Economic Times and The Hindu.
    Identify Indian startups that announced VC funding. 
    Return a list of startups with: Company Name, USP, Founder Name, and LinkedIn Link.
    Ensure output is a simple list I can convert to a table.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash", # Use the flash model for speed
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())]
        )
    )
    
    # 2. Logic to Parse Gemini text into a DataFrame (Simplified for this example)
    # Note: In production, use Gemini's 'response_mime_type': 'application/json' for 100% accuracy.
    data = [] # Data parsed from response.text
    
    # 3. Create Excel
    df = pd.DataFrame(data, columns=["Company Name", "USP", "Founder", "LinkedIn"])
    filename = f"Funding_Report_{today_date}.xlsx"
    df.to_excel(filename, index=False)
    
    # 4. Email Delivery
    msg = EmailMessage()
    msg['Subject'] = f"Daily Startup Funding Report - {today_date}"
    msg['From'] = os.environ.get('GMAIL_USER')
    msg['To'] = "venkatacharan010@gmail.com"
    msg.set_content("Attached is today's research on newly funded Indian startups.")

    with open(filename, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename=filename)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.environ.get('GMAIL_USER'), os.environ.get('GMAIL_PASSWORD'))
        smtp.send_message(msg)

if __name__ == "__main__":
    generate_report()
