import smtplib
import ssl


class emailAlert:
    def __init__(self, subject, message):
        port = 465
        smtp_server = "smtp.gmail.com"
        sender_email = "futuroglobalcheck@gmail.com"  # Enter your address
        receiver_email = 'clicksfamilycontact@gmail.com'  # Enter receiver address
        password = 'imihmqdaiidjabtw'
        message_to_send = f"""\
        Subject: {subject}

        {message}"""

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message_to_send)
