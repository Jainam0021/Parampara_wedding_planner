from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ---------------- ROUTES ---------------- #
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ---------------- CONTACT FORM SUBMIT ---------------- #
@app.route("/submit-contact", methods=["POST"])
def submit_contact():
    data = request.form

    try:
        message = Mail(
            from_email=os.getenv("SENDGRID_FROM_EMAIL"),
            to_emails=os.getenv("SENDGRID_TO_EMAIL"),
            subject="📩 New Wedding Inquiry - Parampara",
            plain_text_content=f"""
New Event Inquiry Received 🎉

Full Name: {data.get('fullName')}
Phone: {data.get('phone')}
Email: {data.get('email')}
Event Date: {data.get('eventDate')}
Event City: {data.get('eventCity')}
Event Type: {data.get('eventType')}
Guests: {data.get('guestCount')}

Description:
{data.get('description')}
"""
        )

        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)

        print("✅ Email sent via SendGrid")
        return jsonify({"success": True}), 200

    except Exception as e:
        print("❌ SendGrid Error:", e)
        return jsonify({"success": False}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
