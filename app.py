from flask import Flask , render_template, redirect,url_for, request
from flask_sqlalchemy import SQLAlchemy
from models import Post, Tag
from forms import PostForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Samuel:5mMdN8QLVMJbtSbRJ-Fz_g@click-wizard-6808.7tc.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full'
db = SQLAlchemy(app)

@app.get('/')
def index():
    render_template('homepage.html')

@app.get('/feed/<int:num_posts>')
def feed(num_posts=10):
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(num_posts).all()
    return render_template('feeds',posts=recent_posts)

@app.route('/create_post', methods=['GET', 'POST'])
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
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
  
    if request.method == 'POST':
        db.session.delete(post)  # delete the post object       
        db.session.commit()  # commit changes to the database
        

    return redirect(url_for('dashboard'))