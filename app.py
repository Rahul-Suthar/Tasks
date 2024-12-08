from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'default_uri')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Task(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('add'))
        
        flash('Invalid credentials, please try again.','error')
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password)

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email already exists', 'error')
        return redirect(url_for('login'))
    
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash('Account created successfully! Please login', 'success')
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))


@app.route('/', methods = ['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        if title.strip():
            new_task = Task(title=title, desc=desc, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully', 'success')
        else:
            flash('Title cannot be empty', 'error')

        return redirect(url_for('add'))

    allTask = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html',allTask=allTask)


@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
@login_required
def update(sno):
    task = Task.query.filter_by(sno=sno, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        task.title = title
        task.desc = desc
        db.session.commit()
        flash('Task updated successfully', 'success')
        return redirect(url_for('add'))

    return render_template('update.html',task=task)


@app.route('/delete/<int:sno>')
@login_required
def delete(sno):
    task = Task.query.filter_by(sno=sno, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully', 'success')
    return redirect(url_for('add'))


@app.route('/done/<int:sno>', methods = ['GET', 'POST'])
@login_required
def mark_done(sno):
    task = Task.query.filter_by(sno=sno, user_id=current_user.id).first_or_404()
    task.done = not task.done
    db.session.commit()
    return redirect(url_for('add'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods=['POST'])
@login_required
def search():
    title = request.form.get('search', '').strip()  # Get the search term from the form, default to an empty string
    if not title:
        flash('Search term cannot be empty', 'error')
        return redirect(url_for('add'))
    results = Task.query.filter(Task.title.contains(title), Task.user_id == current_user.id).all()
    return render_template('home.html', allTask=results, search_term=title)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Initialize the database (uncomment during first run)
    with app.app_context():
        db.create_all()
        print("Database created successfully!")

    # Start the app
    app.run(debug=False)
