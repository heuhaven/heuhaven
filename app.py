from flask import Flask, render_template, request, redirect
from cs50 import SQL
import os

app = Flask(__name__)

db = SQL("sqlite:///art.db")
app.config["UPLOAD_FOLDER"] = "static/uploads"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gallery")
def gallery():
    artworks = db.execute("SELECT * FROM artworks")
    return render_template("gallery.html", artworks=artworks)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        category = request.form.get("category")
        description = request.form.get("description")

        image = request.files["image"]
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], image.filename))

        db.execute(
            """
            INSERT INTO artworks (title, category, description, image)
            VALUES (?, ?, ?, ?)
            """,
            title,
            category,
            description,
            "uploads/" + image.filename
        )

        return redirect("/gallery")

    return render_template("add.html")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    db.execute("DELETE FROM artworks WHERE id = ?", id)
    return redirect("/gallery")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        title = request.form.get("title")
        category = request.form.get("category")
        description = request.form.get("description")

        db.execute(
            """
            UPDATE artworks
            SET title = ?, category = ?, description = ?
            WHERE id = ?
            """,
            title,
            category,
            description,
            id
        )

        return redirect("/gallery")

    artwork = db.execute(
        "SELECT * FROM artworks WHERE id = ?", id
    )

    return render_template("edit.html", artwork=artwork[0])

    
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
