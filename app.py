from flask import Flask , render_template, redirect,url_for, request
from flask_sqlalchemy import SQLAlchemy
from models import Post, Tag,User
from forms import PostForm,SignupForm, LoginForm
from werkzeug.security import generate_password_hash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
import psycopg2
import sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Samuel:5mMdN8QLVMJbtSbRJ-Fz_g@click-wizard-6808.7tc.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=-c+cockroachdb+version+%2722.2.7%27'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db.init_app(app)
# queries = Queries(db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
  return db.session.get(User, int(user_id))


@app.before_request
def before_request():
  g.user = current_user

@app.get('/')
def index():
    render_template('homepage.html')

def create_new_user( username,password):    
    password_hash = generate_password_hash(password)
    db.session.add(User(username =username,password_hash = password_hash))
    db.session.commit()

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
  form = SignupForm()
  error = None

  if form.validate_on_submit():
    create_new_user(form.username.data,form.password.data)
    user = User.query.filter_by(username=form.username.data).first()
    if user:
      login_user(user)
    else:
      error = "unsuccesful"
    return redirect(url_for('dashboard'))
  return render_template("signup.html", form=form, error=error)

def validate_password(email,password):
    
    user_password = db.session.query(User).filter(User.email == email).first()
    if user_password.check_password(password):
      return True
    else:
      return False

@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user:
      if validate_password(form.username.data, form.password.data):
        login_user(user)
        return redirect(url_for('dashboard'))
      else:
        error = "invalid password / user"
    else:
      error = "invalid password / user"

  return render_template("login.html", form=form, error=error)

@app.get('/feed/<int:num_posts>')
@login_required
def feed(num_posts=10):
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(num_posts).all()
    return render_template('feeds',posts=recent_posts)

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        # Create a new post object
        post = Post(title=form.title.data, content=form.content.data, author=current_user)

        # Add tags to the post
        tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        post.tags = tags

        # Add the post to the database
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('new_post.html', title='New Post', form=form)

@app.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
  
    if request.method == 'POST':
        db.session.delete(post)  # delete the post object       
        db.session.commit()  # commit changes to the database
    return redirect(url_for('dashboard'))
    
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
  logout_user()
  g.user = None
  return redirect(url_for('index'))