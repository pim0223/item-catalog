from flask_dance.contrib.google import make_google_blueprint, google
from flask import redirect, url_for

bp = make_google_blueprint(
    client_id="1060097984595-boqo8n931lbivhtmce05qcara5ecjo6u.apps.googleusercontent.com",
    client_secret="QdqSqXdoj4QiEcNQqY2mN9rc",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
)

@bp.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])