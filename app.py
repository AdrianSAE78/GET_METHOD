from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)

@app.route("/")
def index():
    with app.app_context():
        db.create_all()
    
    url = "https://jsonplaceholder.typicode.com/posts"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()

        if not Post.query.first():
            for item in data[:10]:
                post = Post(userId=item["userId"], title=item["title"], body=item["body"])
                db.session.add(post)
            db.session.commit()

        posts = Post.query.all()
        return render_template("index.html", posts=posts)
        
    except requests.RequestException as e:
        return f"Error al obtener datos: {e}", 500
    except Exception as e:
        return f"Error interno: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)