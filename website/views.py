from re import S
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login.utils import login_required
from flask_migrate import current
from . import db, admin, mail, s
from flask_mail import Message
from flask_login import current_user
from .models import Student, Record
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql import func
#from website import app

views = Blueprint('views', __name__)

@views.route("/")
@login_required
def home():
    #users = db.session.query(User, Profile).outerjoin(Profile, Profile.user_id == User.id)
    # for user in users:
    #     print(user)
    # gets all of the records for the current student
    #if current_user.is_authenticated:
    sum = db.session.query(func.sum(Record.hours).filter(Record.student_id==current_user.id).label("sum"))
    sum = sum.scalar()
    records = Record.query.filter_by(student_id=current_user.id)
    return render_template("index.html", title="Home", user=current_user, records=records, sum=sum)

@views.route("/request-hours", methods=['GET', 'POST'])
@views.route("/request-hours/", methods=['GET', 'POST'])
def request_hours():
    if request.method == "POST":
        # creates new service record
        org_name = request.form.get("org-name")
        hours = int(request.form.get("hours"))
        activity = request.form.get("activity")
        supervisor_email = request.form.get("supervisor-email")
        # print(org_name)
        # print(hours)
        # print(activity)
        # print(supervisor_email)

        new_record = Record(organization_name=org_name, hours=hours, activity=activity,
         supervisor_email=supervisor_email, student_id=current_user.id)
        # adds the record to the db and commits it
        db.session.add(new_record)
        db.session.commit()
        flash("Your request has  been submitted.", category="success")
        record_id = new_record.id
        token = s.dumps(supervisor_email)
        link = url_for('views.verify_hours', token=token, record_id=record_id, _external=True)
        msg = Message("Verify Service Hours",
                  sender="gritzpython@gmail.com",
                  recipients=["yairgritzman@gmail.com"])
        msg.body = "{} is requesting community service hours. Please click the link to verify: {}".format(current_user.full_name, link)
        #msg.html = ""
        mail.send(msg)
        records = Record.query.filter_by(student_id=current_user.id)
        return redirect(url_for("views.home"))
    return render_template("request-hours.html", title="Request Hours", user=current_user)

@views.route('/verify-hours/<token>/<int:record_id>', methods=['GET', 'POST'])
def verify_hours(token, record_id):
    current_record = Record.query.get(record_id)
    if request.method == "POST":
        isValid = request.form.get("isValid")
        print(isValid)
        supervisor_notes = request.form.get("notes")
        print(supervisor_notes)
        # adds the notes to the record
        current_record.supervisor_notes = supervisor_notes
        # if not valid, set the value to invalid
        if isValid == "yes":
            current_record.is_verified = True
        db.session.commit()
        return "Thank you for your response!"
    email = s.loads(token)
    # current_record.is_verified = True
    return render_template("verify-hours.html", user=current_user, title="Verify Hours")

# adds the admin view
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Record, db.session))
