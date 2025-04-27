import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage

# Name: Yekai
# Date: 2025/4/27

round_count = 0
max_rounds = 4
Sampling_interval = 3 * 60 * 60


def callback(channel):
    global round_count
    current_time = time.time()

    # check the time block
    if not hasattr(callback, 'last_detection_time'):
        callback.last_detection_time = 0

    if current_time - callback.last_detection_time >= Sampling_interval and round_count < max_rounds:
        callback.last_detection_time = current_time
        round_count += 1

        if GPIO.input(channel):
            send_email("Lack of water")
        else:
            send_email("Enough water")

        print(f"Detection {round_count}/{max_rounds} has completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # calculate the need to continue
        if round_count >= max_rounds:
            print("All detections completed.")
            GPIO.cleanup()
            exit()


def send_email(content):
    # Set the sender email and password and recipient email
    from_email_addr = "2981634913@qq.com"
    from_email_pass = "jiamian30"
    to_email_addr = "740918391@qq.com"

    # Create a message object
    msg = EmailMessage()

    # Set the email body
    msg.set_content(content)

    # Set sender and recipient
    msg['From'] = from_email_addr
    msg['To'] = to_email_addr

    # Set your email subject
    msg['Subject'] = 'Detect whether the plant needs watering'

    # Connecting to server and sending email
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)

    # Login to the smtp server
    server.login(from_email_addr, from_email_pass)

    # Send the message
    server.send_message(msg)
    print('Email sent')

    # Disconnect from the Server
    server.quit()


if __name__ == '__main__':
    # GPIO SETUP
    channel = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN)

    callback(channel)

    GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # detect the pin goes high or low
    GPIO.add_event_callback(channel, callback)  # set call back function

    print(f"Monitoring started.I will check every 3 hours, total {max_rounds} times.")

    try:
        while True:

            current_time = time.time()
            if hasattr(callback, 'last_detection_time') and \
                    current_time - callback.last_detection_time >= Sampling_interval and \
                    round_count < max_rounds:
                callback(channel)

            time.sleep(1)
    except KeyboardInterrupt:
        print("Program interrupted by user")
        GPIO.cleanup()
