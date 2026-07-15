import smtplib

EMAIL = "ronitx2005@gmail.com"
PASSWORD = "rrxafxklqnkvbekd"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.ehlo()

server.login(EMAIL, PASSWORD)

print("LOGIN SUCCESS")

server.quit()