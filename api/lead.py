"""Vercel serverless — B2C lead capture. POST /api/lead"""
import os, json, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import BaseHTTPRequestHandler

SMTP_HOST = "mail.privateemail.com"
SMTP_PORT = 587
FROM_ADDR = "hello@vlmcreateflow.com"
FROM_PASS = os.getenv("SMTP_HELLO_PASS", "Vlmcreateflow1!")
NOTIFY    = ["tylarkin@vlmcreateflow.com", "virallensemediavlm@gmail.com"]

def _send(subject, body, to):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = FROM_ADDR
    msg["To"]      = to
    msg.attach(MIMEText(body, "plain"))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls(); s.login(FROM_ADDR, FROM_PASS); s.sendmail(FROM_ADDR, to, msg.as_string())

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body    = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        name    = body.get("name", "")
        email   = body.get("email", "")
        company = body.get("company", "")
        first   = name.split()[0] if name else "there"

        for addr in NOTIFY:
            try:
                _send(
                    f"New B2C Lead — {name} @ {company}",
                    f"New CreateFlow Lead\n\nName: {name}\nEmail: {email}\nCompany: {company}\nSource: vlmcreateflow.com",
                    addr
                )
            except: pass

        try:
            _send(
                "Welcome to CreateFlow — let's build your engine",
                f"""Hey {first},

You're in. I'll reach out within a few hours to kick off your onboarding.

Here's what happens next:
- We jump on a quick call to scope your brand
- Your AI avatar gets built from your reference photos
- Content starts flowing within the week

If you have reference photos, brand assets, or content examples you want me to look at before we talk — just reply and send them over.

Talk soon.

— Ty
Viral Lense Media
hello@vlmcreateflow.com
""",
                email
            )
        except: pass

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
