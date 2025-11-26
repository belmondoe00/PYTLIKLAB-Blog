import os
from datetime import datetime
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    comments = db.relationship('Comment', back_populates='post', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'created_at': self.created_at.isoformat()
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    approved = db.Column(db.Boolean, default=False, nullable=False)

    post = db.relationship('Post', back_populates='comments')

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'author': self.author,
            'body': self.body,
            'created_at': self.created_at.isoformat(),
            'approved': self.approved
        }


@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts])

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    if not data or 'title' not in data or 'body' not in data:
        return jsonify({'error': 'Missing title or body'}), 400

    new_post = Post(title=data['title'], body=data['body'])
    db.session.add(new_post)
    db.session.commit()

    response = jsonify(new_post.to_dict())
    response.status_code = 201
    response.headers['Location'] = f'/api/posts/{new_post.id}'
    return response


@app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id, approved=True).order_by(Comment.created_at.asc()).all()
    return jsonify([c.to_dict() for c in comments])

@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    data = request.get_json()
    if not data or 'author' not in data or 'body' not in data:
        return jsonify({'error': 'Missing author or body'}), 400
    
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    new_comment = Comment(
        post_id=post_id,
        author=data['author'],
        body=data['body']
    )
    db.session.add(new_comment)
    db.session.commit()

    response = jsonify(new_comment.to_dict())
    response.status_code = 201
    return response


@app.route('/api/comments/pending', methods=['GET'])
def get_pending_comments():
    comments = Comment.query.filter_by(approved=False).all()
    result = []
    for c in comments:
        c_dict = c.to_dict()
        c_dict['post_title'] = c.post.title
        result.append(c_dict)
    return jsonify(result)

@app.route('/api/comments/<int:comment_id>/approve', methods=['POST'])
def approve_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    comment.approved = True
    db.session.commit()
    
    return jsonify({'message': 'Approved', 'comment': comment.to_dict()}), 200


@app.route('/')
def index():
    if not os.path.exists('static'):
        os.makedirs('static')
    return app.send_static_file('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Post.query.first():
            db.session.add(Post(title="Witamy na Blogu!", body="To jest pierwszy post. Dodaj komentarz, aby przetestować moderację."))
            db.session.commit()
            
    app.run(debug=True, port=5000)