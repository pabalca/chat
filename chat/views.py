from flask import abort, flash, redirect, render_template, session, url_for, request
from sqlalchemy import or_

from chat import app
from chat.models import User, Message, db
from chat.forms import LoginForm, RegisterForm, MessageForm, SearchForm
from chat.decorators import login_required

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
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
        challenge = form.challenge.data
        users = User.query.all()
        for user in users:
            if user.verify_password(challenge):
                session["logged_in"] = True
                session["user"] = user.id
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
    messages = Message.query.order_by(Message.created_at.desc())
    if form.validate_on_submit():
        who = session.get("user")
        to = form.to.data
        text = form.text.data
        m = Message(who=who, to=to, text=text)
        db.session.add(m)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("index.html", form=form, messages=messages)


@app.route("/clear/<message_id>", methods=["GET", "POST"])
@login_required
def clear(message_id):
    r = Message.query.get(message_id)
    db.session.delete(r)
    db.session.commit()
    flash(f"Your message <{message_id}> is deleted.")
    return redirect(url_for("index"))
