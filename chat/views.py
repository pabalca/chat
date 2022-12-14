from flask import abort, flash, redirect, render_template, session, url_for, request
from sqlalchemy import or_, and_
from datetime import datetime

from chat import app
from chat.models import User, Message, db
from chat.forms import LoginForm, RegisterForm, MessageForm, SearchForm
from chat.decorators import login_required


def convert_timedelta(when):
    now = datetime.now()
    duration = now - when
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)

    if hours < 1:
        return f"~{minutes}m"
    elif hours < 2:
        return f"~{hours}h:{minutes}m"
    elif hours > 24:
        return f"~{days}d"
    else:
        return f"~{hours}h"


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.lower()
        password = form.password.data
        u = User(username=username, pwd=password)
        db.session.add(u)
        db.session.commit()
        flash(f"Your user <{username} is saved.")
        return redirect(url_for("register"))
    return render_template("register.html", form=form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    session["logged_in"] = False
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        challenge = form.challenge.data
        users = User.query.all()
        for user in users:
            if user.verify_password(challenge) and user.username == username:
                session["logged_in"] = True
                session["user"] = user.id
                session["username"] = user.username
                return redirect(url_for("index"))
    return render_template("login.html", form=form, session=session)


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # search_form = SearchForm()
    form = MessageForm()
    whoami = User.query.filter(User.id == session.get("user")).first().username

    messages = (
        Message.query.order_by(Message.created_at.desc())
        .filter(or_(Message.who == whoami, Message.to == whoami))
        .all()
    )

    # get the people you have had contact
    contact_with = set()
    for mes in messages:
        contact_with.add(mes.who)
        contact_with.add(mes.to)

    contacts = []
    for contact in contact_with:
        last_message = (
            Message.query.order_by(Message.created_at.desc())
            .filter(
                or_(
                    and_(Message.who == whoami, Message.to == contact),
                    and_(Message.who == contact, Message.to == whoami),
                )
            )
            .first()
        )
        if last_message:
            contacts.append(
                {
                    "username": contact,
                    "text": last_message.text,
                    "last_talker": last_message.to
                    if contact == last_message.who
                    else last_message.who,
                    "last": last_message.created_at,
                    "last_fmt": convert_timedelta(last_message.created_at)
                }
            )

        # order contacts by last
        contacts = sorted(contacts, key=lambda d: d["last"], reverse=True)

    if form.validate_on_submit():
        who = whoami
        to = form.to.data
        text = form.text.data
        m = Message(who=who, to=to, text=text)
        db.session.add(m)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template(
        "index.html", form=form, messages=messages, contacts=contacts
    )


@app.route("/c/<friend>", methods=["GET", "POST"])
@login_required
def conversation(friend):
    form = MessageForm()
    whoami = User.query.filter(User.id == session.get("user")).first().username
    form.to.data = friend
    messages = (
        Message.query.order_by(Message.created_at.desc())
        .filter(
            or_(
                and_(Message.who == whoami, Message.to == friend),
                and_(Message.who == friend, Message.to == whoami),
            )
        )
        .all()
    )

    if form.validate_on_submit():
        who = whoami
        to = friend
        text = form.text.data
        m = Message(who=who, to=to, text=text)
        db.session.add(m)
        db.session.commit()
        return redirect(url_for("conversation", friend=friend))
    return render_template(
        "conversation.html", form=form, messages=messages, friend=friend
    )


@app.route("/clear/<message_id>", methods=["GET", "POST"])
@login_required
def clear(message_id):
    r = Message.query.get(message_id)
    db.session.delete(r)
    db.session.commit()
    flash(f"Your message <{message_id}> is deleted.")
    return redirect(url_for("index"))
