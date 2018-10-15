from flask import Flask, request, redirect, render_template, url_for
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
    

    def __init__(self, title, body):
        self.title = title
        self.body = body
                
  
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == 'POST':
        return render_template('blog.html')
    title = request.form['title']
    return redirect(url_for('newpost', title=title))

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title_form = request.form.get('title')
    title = request.args.get('title')
    return render_template('newpost.html', title=title, title_form=title_form)


@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method == 'POST':
        title_name = request.form['title']
        body_name = request.form['body']
        newpost = Blog(title_name, body_name)
        db.session.add(newpost)
        db.session.commit()
        
    
    newposts = Blog.query.all()
    return render_template('blog.html',title="Build A Blog", newposts=newposts)


if __name__ == '__main__':
    app.run()