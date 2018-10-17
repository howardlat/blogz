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
    

    def __init__(self, title, body):
        self.title = title
        self.body = body
                
  
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    title = ""
    body = ""
    if len(title) == 0 or len(body) == 0:
        error = "Please enter a title or body"
        return redirect('/newpost', error=error)       
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        newpost = Blog(title, body)
        db.session.add(newpost)
        db.session.commit()                                          
        return redirect('/blog')
    return render_template('newpost.html')

            
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('blog.html',title="Build A Blog")


if __name__ == '__main__':
    app.run()