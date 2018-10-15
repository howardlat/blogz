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
    body = db.Column(db.String(300))
    submitted = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.submitted = False

        
  
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    return render_template('blog.html')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    return render_template('newpost.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method == 'POST':
        title_name = request.form['title']
        body_name = request.form['body']
        newpost = Blog(title_name, body_name)
        db.session.add(newpost)
        db.session.commit()
        
    
    newposts = Blog.query.filter_by(submitted=False).all()
    submitted_newposts = Blog.query.filter_by(submitted=True).all()
    return render_template('blog.html',title="Build A Blog", newposts=newposts, submitted_newposts=submitted_newposts)

@app.route('/add', methods=['POST'])
def add():
    newpost_id = int(request.form['newpost-id'])
    newpost = Blog.query.get(newpost_id)
    newpost.submitted = True
    db.session.add(newpost)
    db.session.commit()

    return redirect('/blog')


if __name__ == '__main__':
    app.run()