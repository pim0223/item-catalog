from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import UserMixin, current_user, login_required, login_user, logout_user, LoginManager
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
from flask import redirect, url_for, flash, render_template
from src.models import User, OAuth
from src import db, app

bp = make_google_blueprint(
    client_id="1060097984595-boqo8n931lbivhtmce05qcara5ecjo6u.apps.googleusercontent.com",
    client_secret="QdqSqXdoj4QiEcNQqY2mN9rc",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
)

login_manager = LoginManager(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

bp.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(bp)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Google.", category="error")
        return False

    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info from Google."
        flash(msg, category="error")
        return False

    google_info = resp.json()
    google_user_id = str(google_info["id"])

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=google_user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=google_user_id,
            token=token,
        )

    if oauth.user:
        # If this OAuth token already has an associated local account,
        # log in that local user account.
        login_user(oauth.user)
        flash("Successfully signed in with Google.")

    else:
        # If this OAuth token doesn't have an associated local account,
        # create a new local user account for this user. We can log
        # in that account as well, while we're at it.
        user = User(email=google_info["email"])
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])

        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in with Google.")

    # Return false to flask - dance as we handle the token saving
    return False

@app.route("/")
def index():
    # import ipdb; ipdb.set_trace()
    return render_template("oauth.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))