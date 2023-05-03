#voorbeeld

from flask import Flask
from flask import render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
app.config[
    "SECRET_KEY"
] = "adc2d8261c603fc1079b04fe4bcd38d37ecbae27d288ad1480ca06b4bd0acf06"
db.init_app(app)


class ProgrammingLanguage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)


@app.cli.command("db-init")
def db_init():
    with app.app_context():
        db.create_all()
        db.session.execute(
            insert(ProgrammingLanguage),
            [
                {"name": "Python"},
                {"name": "Myrddin"},
                {"name": "Ocaml"},
            ],
        )
        db.session.commit()


@app.route("/")
def all_pl():
    results = db.session.execute(
        db.select(ProgrammingLanguage).order_by(ProgrammingLanguage.name)
    ).scalars()
    return render_template("list.html", programming_languages=results)


@app.route("/pl", methods=["GET", "POST"])
def create_pl():
    if request.method == "POST":
        new_name = request.form["name"]
        if not new_name:
            flash("A name is required!")
        result = ProgrammingLanguage(name=new_name)
        db.session.add(result)
        db.session.commit()
        flash(f"Created {new_name}.")
        return redirect(url_for("show_pl", id=result.id))

    return render_template("create.html")


@app.route("/pl/<int:id>")
def show_pl(id):
    result = db.get_or_404(ProgrammingLanguage, id)
    return render_template("show.html", programming_language=result)


@app.route("/pl/edit/<int:id>", methods=["GET", "POST"])
def edit_pl(id):
    result = db.get_or_404(ProgrammingLanguage, id)

    if request.method == "POST":
        new_name = request.form["name"]
        if not new_name:
            flash("A name is required!")
        old_name = result.name
        result.name = new_name
        db.session.commit()
        flash(f"Updated {old_name} to {new_name}.")
        return redirect(url_for("show_pl", id=result.id))

    return render_template("edit.html", programming_language=result)


@app.route("/pl/delete/<int:id>")
def delete_pl(id):
    result = db.get_or_404(ProgrammingLanguage, id)
    db.session.delete(result)
    db.session.commit()
    flash(f"Deleted {result.name}.")
    return redirect(url_for("all_pl"))