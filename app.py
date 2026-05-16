import smtplib
import os
import base64
from email.mime.text import MIMEText
from email.mime.image import MIMEImage 
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load credentials
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# --- Configuration (edit these) ---
DATATHON_NAME = "2026 Datathon"
EVENT_DATE = "Saturday, May 22th 2026"
EVENT_LOCATION = "Events on Pine, 140 Pine Ave, 3rd Floor, Downtown Long Beach, CA 90802"
REGISTRATION_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSe8bNOUAhyMWEeTIrmzuxnOP11IybEpifDKTPSOON0iJHupdA/viewform?usp=publish-editor"
SUBJECT = f"You're Accepted to the {DATATHON_NAME}! 🎉"
LOGO_PATH = "imgs/Ai_Logo.png"

# Load recipients
with open("users.txt") as f:
    recipients = [line.strip() for line in f if line.strip()]

def build_email(to_address):
    msg = MIMEMultipart("related")
    msg["Subject"] = SUBJECT
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_address

    # Wrap text + html in an "alternative" part
    alt_part = MIMEMultipart("alternative")
    msg.attach(alt_part)


    # Plain text version
    text = f"""
Congratulations!

We are thrilled to inform you that you have been accepted to the {DATATHON_NAME}!

Event Details:
  Date:     {EVENT_DATE}
  Location: {EVENT_LOCATION}

Please complete your registration using the link below to secure your spot:
{REGISTRATION_LINK}

We look forward to seeing you there!

Best regards,
The {DATATHON_NAME} Team
"""

    # HTML version
    html = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">

  <h2 style="color: #2e7d32;">🎉 Congratulations! You've been accepted!</h2>

  <p>We are thrilled to inform you that you have been accepted to the <strong>{DATATHON_NAME}</strong>!</p>

  <h3 style="color: #444;">Event Details</h3>
  <table style="border-collapse: collapse; width: 100%;">
    <tr>
      <td style="padding: 8px; font-weight: bold;">Date</td>
      <td style="padding: 8px;">{EVENT_DATE}</td>
    </tr>
    <tr style="background-color: #f5f5f5;">
      <td style="padding: 8px; font-weight: bold;">Location</td>
      <td style="padding: 8px;">{EVENT_LOCATION}</td>
    </tr>
  </table>

  <br>
  <img src="cid:new_flyer" alt="Congratulations" style="width: 100px; display: block; margin: 20px auto;">
  <p>Please complete your registration below to secure your spot:</p>

  <a href="{REGISTRATION_LINK}" style="
    display: inline-block;
    background-color: #2e7d32;
    color: white;
    padding: 12px 24px;
    text-decoration: none;
    border-radius: 5px;
    font-size: 16px;
  ">
    Complete Registration
  </a>

  <br><br>
  <p>We look forward to seeing you there!</p>

  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 20px 0;">

  <!-- Logo section -->
  <table style="width: 100%; text-align: center;">
    <tr>
      <td>
        <img src="cid:club_logo" alt="AI Club CSULB" style="width: 150px; margin: 10px auto;">
        <p style="color: #888; font-size: 13px; margin: 4px 0;">
          <strong>The AI Club CSULB Team</strong>
        </p>
        <p style="color: #aaa; font-size: 12px; margin: 2px 0;">
          California State University, Long Beach
        </p>
      </td>
    </tr>
  </table>

</body>
</html>
"""

    #  Attach text and html to alt_part, NOT to msg
    alt_part.attach(MIMEText(text, "plain"))
    alt_part.attach(MIMEText(html, "html"))

    # Actually read and attach the image file
    with open("imgs/new_flyer.jpg", "rb") as img_file:
        img = MIMEImage(img_file.read())
        img.add_header("Content-ID", "<new_flyer>")
        img.add_header("Content-Disposition", "inline")
        msg.attach(img)
    with open(LOGO_PATH, "rb") as logo_file:
        logo = MIMEImage(logo_file.read())
        logo.add_header("Content-ID", "<club_logo>")
        logo.add_header("Content-Disposition", "inline")
        msg.attach(logo)
    return msg

# Send emails
def send_all():
    print(f"Connecting to Gmail SMTP...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print(f"Logged in. Sending to {len(recipients)} recipients...\n")

        successful = []
        failed = []

        for recipient in recipients:
            try:
                msg = build_email(recipient)
                server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
                print(f"  ✓ Sent to {recipient}")
                successful.append(recipient)
            except Exception as e:
                print(f"  ✗ Failed for {recipient}: {e}")
                failed.append(recipient)

    # Summary
    print(f"\n--- Summary ---")
    print(f"Successfully sent: {len(successful)}")
    print(f"Failed:            {len(failed)}")

    # Save failed addresses for retry
    if failed:
        with open("failed.txt", "w") as f:
            f.write("\n".join(failed))
        print(f"Failed addresses saved to failed.txt")

if __name__ == "__main__":
    send_all()