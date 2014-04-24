import requests
from secrets import mailgun_key, app_message_key
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='static', static_url_path='')


@app.route("/")
def index():
    return render_template('base.html')


@app.route("/cv/")
def cv():
    return render_template('cv.html')


@app.route("/send-app-message/", methods=['POST'])
def send_app_message():

    # Send an email if all the parameters are there

    for value in ['user_email', 'user_message', 'app_message_key']:
        if value not in request.form.keys():
            return jsonify(message="Unable to send message"), 400

    if request.form["app_message_key"] != app_message_key:
        return jsonify(message="Incorrect key"), 400

    user_email = request.form["user_email"]
    user_message = request.form["user_message"]

    email_text = "User Email:\n %s \n\n User Message:\n %s \n" % (user_email, user_message)

    requests.post(
        "https://api.mailgun.net/v2/sandboxb7645bd943614e39bb23ef85318eb9e1.mailgun.org/messages",
        auth=("api", mailgun_key),
        data={
            "from": "no-reply <no-reply@sandboxb7645bd943614e39bb23ef85318eb9e1.mailgun.org>",
            "to": "Max <max@maxhurl.co.uk>",
            "subject": "Jotter Feedback Message",
            "text": email_text
        }
    )

    return jsonify(message="Message sent"), 200


if __name__ == "__main__":
    app.run(debug=False)
