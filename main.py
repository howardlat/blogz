from flask import Flask, request, redirect, render_template
import cgi
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:herman24@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(400))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/newpost')
def newpost():
    return render_template('newpost.html')

@app.route('/', methods=['POST'])
def error():

    title = request.form['title']
    title_error = ""
    if len(title) < 1:
        title_error = "Please enter a title"
                  
    body = request.form['body']
    body_error = ""
    if len(body) < 1:
        body_error = "Please enter a body"

    #if not title_error and not body_error:
        #return [blog.name for blog in Blog.query.all()]

    #else:
        return render_template('newpost.html',
        title_error=title_error,
        body_error=body_error)

    
@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = blog_name
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()
    encoded_error = request.args.get("error")
    return render_template('blog.html',title="Build A Blog", blogs=blogs, error=encoded_error and cgi.escape(encoded_error, quote=True))


if __name__ == '__main__':
    app.run()