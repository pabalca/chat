from flask import abort, flash, redirect, render_template, session, url_for, request
from sqlalchemy import or_

from chat import app
from chat.models import User, Message, db
from chat.forms import MessageForm, SearchForm


@app.route("/", methods=["GET", "POST"])
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
def clear(message_id):
    r = Message.query.get(message_id)
    db.session.delete(r)
    db.session.commit()
    flash(f"Your message <{message_id}> is deleted.")
    return redirect(url_for("index"))