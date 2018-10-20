from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:herman24@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')
        
    def __init__(self, username, password):
        self.username = username
        self.password = password
                       
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    owner = User.query.filter_by(username=session['username']).first()
        
    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        if len(title) < 1 or len(body) < 1:
            error = "Please enter a title or body"
            return render_template('newpost.html', error=error) 
                    
        title = request.form['title']
        body = request.form['body']
        id = request.args.get('id')
        newpost = Blog(title, body, owner)
        db.session.add(newpost)
        db.session.commit()
        id = newpost.id
        id = str(id)                                          
        return redirect("/post?id=" + id)

       
    return render_template('newpost.html')

@app.route('/post', methods=['GET'])
def post():
    id = request.args.get('id')               
    submitted_blogs = Blog.query.filter_by(id=id).all() 
    return render_template('post.html', submitted_blogs=submitted_blogs)
                      
@app.route('/', methods=['POST', 'GET'])
def index():
    encoded_error = request.args.get("error")
    return render_template('blog.html',title="Build A Blog", error=encoded_error and cgi.escape(encoded_error, quote=True))

if __name__ == '__main__':
    app.run()