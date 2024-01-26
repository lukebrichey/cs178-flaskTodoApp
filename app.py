from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Example of Flask extension
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Template rendering and passing data to templates
@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)

# URL to Python function mapping (Route handling)
@app.post("/add")
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
