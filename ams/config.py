import os

# Flask-Mail Configuration
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get("manokarthick.ks741@gmail.com")  # Your email address
MAIL_PASSWORD = os.environ.get("hyul ocro hrow bnah")  # Your email password
MAIL_DEFAULT_SENDER = os.environ.get("manokarthick.ks741@gmail.com")
