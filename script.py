import pandas as pd
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime

# In a production setup, replace this list with a News API call
data = [
    ["MeltPlan", "AI-native construction planning", "Kanav Hasija", "linkedin.com/in/kanavhasija"],
    ["FREED", "Debt relief platform", "Ritesh Srivastava", "linkedin.com/in/ritesh-srivastava-freed"],
    ["Spintly", "IoT smart building security", "Rohin Parkar", "linkedin.com/in/rohinparkar"]
]

# Create Excel
df = pd.DataFrame(data, columns=["Company Name", "Description & USP", "Founder Name", "LinkedIn Profile Link"])
filename = f"Startup_Funding_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
df.to_excel(filename, index=False)

# Email logic
msg = EmailMessage()
msg['Subject'] = f"Startup Funding Report - {datetime.now().strftime('%d %b %Y')}"
msg['From'] = os.environ.get('GMAIL_USER')
msg['To'] = "venkatacharan010@gmail.com"
msg.set_content("Attached is today's report on newly funded Indian startups.")

with open(filename, 'rb') as f:
    msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename=filename)

# Connect to Gmail SMTP
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(os.environ.get('GMAIL_USER'), os.environ.get('GMAIL_PASSWORD'))
    smtp.send_message(msg)
