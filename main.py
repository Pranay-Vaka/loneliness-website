import unique_id
import datetime
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
db = SQLAlchemy(app)

class Posts(db.Model):
    number = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.String(length = 8), nullable = False)
    date_time = db.Column(db.String(), nullable = False)
    name = db.Column(db.String(length = 100), nullable = False)
    title = db.Column(db.String(length = 100), nullable = False)
    text = db.Column(db.String(length = 5000), nullable = False)

    def __repr__(self):
        
        return f"{self.post_id}"

    
@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html") 


@app.route("/about")
def about_page():
    return render_template("about_us.html")

@app.route("/post", methods = ["POST", "GET"])
def post_page():
    
    if request.method == "POST":
        name = request.form["name"]
        title = request.form["title"]
        text = request.form["text"]

    else:
        return render_template("post.html")
