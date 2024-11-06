from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    done = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


with app.app_context():
    db.create_all()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/user')
def user():
    return redirect('/')

@app.route('/', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title, desc=desc)

        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('home.html', allTodo=allTodo)


@app.route('/done/<int:sno>', methods = ['GET', 'POST'])
def done(sno):
    todo = Todo.query.filter_by(sno=sno).first()

    if todo:
        todo.done = not todo.done
        db.session.commit()
    return redirect('/')


@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search/<title>', methods=['GET','POST'])
def dis(title):
    if request.method == 'POST':
        title = request.form['search']
        todo = Todo.query.filter_by(title=title).all()
        return render_template('home.html', allTodo=todo)

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
