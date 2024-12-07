from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Todo.db"
db = SQLAlchemy(app)

# initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    done = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists', 'error')
            return redirect(url_for('register'))
        
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login', 'success')
        return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successfull!', 'success')

            next = request.args.get('next')
            return redirect(next) if next else redirect(url_for('add'))
        
        flash('Invalid credentials, please try again.','error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))


@app.route('/', methods = ['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title, desc=desc, user_id=current_user.id)

        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', allTodo=allTodo)


@app.route('/done/<int:sno>', methods = ['GET', 'POST'])
@login_required
def done(sno):
    todo = Todo.query.filter_by(sno=sno, user_id=current_user.id).first()

    if todo:
        todo.done = not todo.done
        db.session.commit()
    return redirect(url_for('add'))


@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
@login_required
def update(sno):
    todo = Todo.query.filter_by(sno=sno, user_id=current_user.id).first()

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo.title = title
        todo.desc = desc
        db.session.commit()
        return redirect(url_for('add'))

    return render_template('update.html',todo=todo)


@app.route('/delete/<int:sno>')
@login_required
def delete(sno):
    todo = Todo.query.filter_by(sno=sno, user_id=current_user.id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('add'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods=['POST'])
@login_required
def search():
    title = request.form.get('search', '').strip()  # Get the search term from the form, default to an empty string
    if title:  # Ensure the search term is not empty
        # Search for tasks that contain the search term and belong to the current user
        results = Todo.query.filter(
            Todo.title.contains(title), 
            Todo.user_id == current_user.id
        ).all()
        return render_template('home.html', allTodo=results, search_term=title)
    
    return redirect(url_for('add'))

if __name__ == "__main__":
    app.run(debug=True)
