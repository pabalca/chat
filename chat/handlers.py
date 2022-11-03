import click

from chat import app
from chat.models import User, Message, db


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Message=Message, User=User)


@app.cli.command()
@click.option("--drop", is_flag=True, help="Create after drop.")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")

    u = User(username="admin", pwd="admin")
    db.session.add(u)
    db.session.commit()
    click.echo("Admin user created.")

