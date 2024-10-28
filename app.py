from flask import Flask, flash, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tagline@localhost:5432/flask_demo'

db = SQLAlchemy(app)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String(200), nullable=False)
  description = db.Column(db.String(300), nullable=False)

with app.app_context():
  db.create_all()
  db.create_all()

@app.get('/')
def home():
  return render_template('home.html')

@app.get('/posts')
def posts():
  posts = Post.query.all()
  post_list = [{'id': post.id, 'title': post.title, 'description': post.description} for post in posts]
  return render_template('posts.html', posts=post_list), 200

@app.route('/posts/create', methods=['GET', 'POST'])
def create():
  if request.method == 'POST':
    form_data = request.form
    title = form_data.get('title')
    description = form_data.get('description')
    if not title or not description:
      flash("Title and description are required!")
      return render_template('create.html'), 400

    new_post = Post(title=title, description=description)
    db.session.add(new_post)
    db.session.commit()
    flash("Post created successfully.")
    return redirect(url_for('posts'))

  return render_template('create.html')

@app.route('/posts/<int:id>/update', methods=['GET', 'POST'])
def update(id):
  post = Post.query.get_or_404(id)
  if request.method == 'POST':
    title = request.form.get('title')
    description = request.form.get('description')

    if not title or not description:
      flash("Title and description are required!")
      return render_template('update.html', post=post), 400

    post.title = title
    post.description = description
    db.session.commit()

    flash("Post updated successfully.")
    return redirect(url_for('posts'))

  return render_template('update.html', post=post)


@app.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully.")
    return redirect(url_for('posts'))
