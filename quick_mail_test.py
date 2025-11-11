from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# --- Gmail SMTP (SSL 465) ---
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,        # SSL OR TLS (not both)
    MAIL_USE_TLS=False,
    MAIL_USERNAME="labibafarah2998@gmail.com",
    MAIL_PASSWORD="fpxabbmgzipkiifj",   # <-- paste the app password here (no spaces)
    MAIL_DEFAULT_SENDER=("Sensor App", "labibafarah2998@gmail.com"),
)

mail = Mail(app)

with app.app_context():
    msg = Message(
        subject="SMTP OK?",
        recipients=["your_other_email@example.com"],   # where to send the test
        body="Hello from Flask-Mail via Gmail SMTP."
    )
    mail.send(msg)
    print("Sent!")
