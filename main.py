from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import smtplib
import datetime

app = FastAPI()

# Define a request body model
class EmailRequest(BaseModel):
    name: str
    department: str
    year: str
    college_id: str
    block_name: str
    room_no: str
    problem: str
    media: str
    date: str

# Define your email sending logic
def send_email(request: EmailRequest):
    subject = "Complaint Request"
    body = """
    Hello,
    
    This is a Complaint request from {name}.
    
    Department: {department}
    Year: {year}
    College ID: {college_id}
    Block Name: {block_name}
    Room Number: {room_no}
    Date: {date}
    
    Problem Description:
    {problem}
    
    Media: {media}
    
    Please take the necessary action.
    
    Regards,
    Maintenance Team
    """

    recipient_list = [
        {'email': 'ratheeshraju2003@gmail.com', 'hierarchy': 1},
        {'email': 'ratheeshraju01@gmail.com', 'hierarchy': 2},
        {'email': 'ratheeshaids@gmail.com', 'hierarchy': 3}
    ]
    interval = 10 # Interval in seconds between each recipient

    stop_sending = False

    try:
        # Connect to the email server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your email server details
        server.starttls()
        server.login('ratheeshraju2003@gmail.com', 'lndzbnurfdzklcdu')  # Replace with your email credentials

        for recipient in recipient_list:
            if stop_sending:
                break

            recipient_email = recipient.get('email')

            # Compose the email message
            message = f"Subject: {subject}\n\n{body.format(**request.dict())}"

            try:
                # Send the email
                server.sendmail('ratheeshraju2003@gmail.com', recipient_email, message)

                # Create and start the timer
                end_time = datetime.datetime.now() + datetime.timedelta(seconds=interval)
                while datetime.datetime.now() < end_time:
                    pass

                # Ask if the recipient responded
                response = input("Did the recipient respond to the email? (yes/no): ")

                if response.lower() == "yes":
                    stop_sending = True
                    print(f"Response received from: {recipient_email}")
                elif response.lower() == "no":
                    print(f"No response received from: {recipient_email}. Sending email to the next recipient.")

            except smtplib.SMTPException as e:
                raise HTTPException(status_code=500, detail=f"Failed to send email to: {recipient_email}. Error message: {str(e)}")

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred while sending email to: {recipient_email}. Error message: {str(e)}")

    except smtplib.SMTPException as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to the email server. Error message: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while connecting to the email server. Error message: {str(e)}")

    finally:
        try:
            server.quit()
        except:
            pass

# Define your API endpoint
@app.post("/send-email")
async def send_email_endpoint(request: EmailRequest):
    send_email(request)
    return {"message": "Email sent successfully"}

