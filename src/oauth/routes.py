# Routes and functionality needed for OAuth login

from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import UserMixin, current_user, login_required, \
                        login_user, logout_user
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
from flask import redirect, url_for, flash, render_template
from src.models import User, OAuth
from src import db, login_manager


# Functionality to load user from the db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# On unauthorized access, return to homepage
@login_manager.unauthorized_handler
def unauthorized():
    flash('You need to be logged in to view this page')
    return redirect(url_for('index'))


bp = make_google_blueprint(
    client_id="""1060097984595-boqo8n931lbivhtmce05qcara
                5ecjo6u.apps.googleusercontent.com""",
    client_secret="QdqSqXdoj4QiEcNQqY2mN9rc",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ]
)

bp.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)


# Create or login user after successful OAuth authentication
@oauth_authorized.connect_via(bp)
def google_logged_in(blueprint, token):

    # No token received
    if not token:
        flash("Failed to log in with Google.", category="error")
        return False

    # User info was not fetched from Google
    response = blueprint.session.get("/oauth2/v2/userinfo")
    if not response.ok:
        msg = "Failed to fetch user info from Google."
        flash(msg, category="error")
        return False

    google_info = response.json()
    google_user_id = str(google_info["id"])

    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=google_user_id,
    )

    # Get the associated OAuth token if it exists
    try:
        oauth = query.one()

    # Else, create it
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=google_user_id,
            token=token,
        )

    # If a user is associated to this account, log in that user
    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with Google.")

    # Else, create a user with the email from the Google response
    else:
        user = User(email=google_info["email"])
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()

        # Log in the new user
        login_user(user)
        flash("Successfully signed in with Google.")

    return False


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))
