from flask import Flask, redirect, request, render_template_string
import random
from datetime import datetime

app = Flask(__name__)

# List of random redirect links
links = [
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://www.reddit.com",
    "https://www.openai.com",
    "https://www.youtube.com"
]

# Store logs in memory (or extend to a database later)
visit_log = []

# HTML page for homepage
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
    return redirect(random.choice(links))

@app.route("/logs")
def logs():
    return "<br>".join(visit_log) if visit_log else "No visits yet."
