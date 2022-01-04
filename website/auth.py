from flask import Blueprint, render_template, request, flash, url_for
from sqlalchemy.sql.operators import exists
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
#from website import app
from .models import Student
from .views import views
from . import db, get_google_provider_cfg, client, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from flask_login import login_user, login_required, logout_user, current_user
import requests
import json

auth = Blueprint('auth', __name__)

@auth.route("/sign-up", methods=['GET', 'POST'])
@auth.route("/sign-up/", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        pass1 = request.form.get("password1")
        pass2 = request.form.get("password2")
        grad_year = int(request.form.get("grad-year"))
        # interests = request.form.get("interests")
        # skills = request.form.get("skills")
        # create new student

        user = Student.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(fname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif pass1 != pass2:
            flash('Passwords don\'t match.', category='error')
        elif len(pass1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_student = Student(email=email, first_name=fname, last_name=lname, password=generate_password_hash(
                pass1, method='sha256'), graduation_year=grad_year)
            # adds the new profile
            db.session.add(new_student)
            db.session.commit()
            # logs in user before creating new profile with current user's id
            login_user(new_student, remember=True)
            #new_profile = Profile(graduation_year=grad_year, interests=interests, skills=skills, user_id=current_user.id)
            #db.session.add(new_profile)
            db.session.commit()
            flash("Account Created!", category="success")
            return redirect(url_for("views.home"))
    return render_template("sign-up.html", title="Sign Up", user=current_user)

# @auth.route("/login", methods=['GET', 'POST'])
# @auth.route("login/", methods=['GET', 'POST'])
# def login():
#     return render_template("login.html", title="Login")

@auth.route('/login', methods=['GET', 'POST'])
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@auth.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        # picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    #user = Student(id=unique_id, full_name=users_name, email=users_email)
    # adds user to the db if the user is not already there
    # checks to see if the user already exists by comparing the email
    user = Student.query.filter_by(email=users_email).first()
    print(user)
    # if the user doesn't exist, it creates a new user and adds it to the database
    if not user:
        user = Student(google_id=unique_id, full_name=users_name, email=users_email)
        db.session.add(user)
        db.session.commit()
    # logs in user
    login_user(user)
    # redirects to home page
    return redirect(url_for('views.home'))
    #Student.create(unique_id, users_name, users_email)



    # if request.method == 'POST':
    #     email = request.form.get('email')
    #     password = request.form.get('password')

    #     user = Student.query.filter_by(email=email).first()
    #     if user:
    #         if check_password_hash(user.password, password):
    #             flash('Logged in successfully!', category='success')
    #             login_user(user, remember=True)
    #             return redirect(url_for('views.home'))
    #         else:
    #             flash('Incorrect password, try again.', category='error')
    #     else:
    #         flash('Email does not exist.', category='error')

    # return render_template("login.html", user=current_user, title="Login")


# @auth.route('/admin-sign-up/')
# @auth.route('/admin-sign-up')
# def admin_sign_up():
#     if request.method == 'POST':
#         email = request.form.get("email")
#         fname = request.form.get("fname")
#         lname = request.form.get("lname")
#         pass1 = request.form.get("password1")
#         pass2 = request.form.get("password2")
#         access_code = request.form.get("access-code")

#         admin = Stud.query.filter_by(email=email).first()
#         if admin:
#             flash('Email already exists.', category='error')
#         elif len(email) < 4:
#             flash('Email must be greater than 3 characters.', category='error')
#         elif len(fname) < 2:
#             flash('First name must be greater than 1 character.', category='error')
#         elif pass1 != pass2:
#             flash('Passwords don\'t match.', category='error')
#         elif len(pass1) < 7:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
#             new_user = User(email=email, first_name=fname, last_name=lname, password=generate_password_hash(
#                 pass1, method='sha256'))
#             # adds the new profile
#             db.session.add(new_user)
#             db.session.commit()
#             # logs in user before creating new profile with current user's id
#             login_user(new_user, remember=True)
#             new_profile = Profile(graduation_year=grad_year, interests=interests, skills=skills, user_id=current_user.id)
#             db.session.add(new_profile)
#             db.session.commit()
#             flash("Account Created!", category="success")
#             return redirect(url_for("views.home"))

#     return render_template("admin-sign-up.html", user=current_user, title="Admin Resigistration")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))