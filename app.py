"""
Visi standartiniai veiksmai su db, prijungsim šablone css
"""
from models import db, Projektas
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# fizinės db prijungimas, configas
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projektai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# paleidžiam db
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    search_text = request.args.get("searchlaukelis")
    if search_text:
        filtered_rows = Projektas.query.filter(Projektas.pavadinimas.ilike(f"{search_text}%"))
        return render_template("index.html", projects=filtered_rows)
    else:
        all_projects = Projektas.query.all()
        return render_template("index.html", projects=all_projects)


@app.route("/projektas/<int:row_id>")
def one_project(row_id):
    project = Projektas.query.get(row_id)
    if project:
        return render_template("one_project.html", project=project)
    else:
        return f"Projekto su id {row_id} neegzistuoja"


@app.route("/projektas/redaguoti/<int:row_id>", methods=["get", "post"])
def update_project(row_id):
    project = Projektas.query.get(row_id)
    if not project:
        return f"Projekto su id {row_id} neegzistuoja"

    if request.method == "GET":
        return render_template("update_project_form.html", project=project)

    elif request.method == "POST":
        name = request.form.get("pavadinimaslaukelis")
        price = float(request.form.get("kainalaukelis"))
        project.pavadinimas = name
        project.kaina = price
        db.session.commit()
        return redirect(url_for("home"))  # nukreipimas į home funkcijos endpointą
        # return redirect(f"/projektas/{row_id}")  # variantas nukreipimo į vieno projekto rodymą


@app.route("/projektas/trynimas/<int:row_id>", methods=["POST"])
def delete_project(row_id):
    project = Projektas.query.get(row_id)
    if not project:
        return f"Projekto su id {row_id} neegzistuoja"
    else:
        db.session.delete(project)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/projektas/naujas", methods=["GET", "POST"])
def create_project():
    if request.method == "GET":
        return render_template("create_project_form.html")
    if request.method == "POST":
        name = request.form.get("pavadinimaslaukelis")
        price = float(request.form.get("kainalaukelis"))
        if name and price:
            new_project = Projektas(pavadinimas=name, kaina=price)
            db.session.add(new_project)
            db.session.commit()
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(port=5001, debug=True)
