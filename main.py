from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:herman24@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(600))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog')
def blog():
    newpost = request.form['newpost']
    return render_template('blog.html', newpost=newpost)

@app.route('/newpost')
def newpost():
    return render_template('newpost.html')
    
@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = blog_name
        db.session.add(new_blog)
        db.session.commit()

    
    return render_template('blog.html',title="Build A Blog")


if __name__ == '__main__':
    app.run()