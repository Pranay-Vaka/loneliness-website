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
        
        return self.post_id 

class Comments(db.Model):

    number = db.Column(db.Integer(), primary_key = True)
    post_id = db.Column(db.String(length = 8), nullable = False)
    comment_id = db.Column(db.String(length = 8), nullable = False)
    date_time = db.Column(db.String(), nullable = False)
    name = db.Column(db.String(length = 100), nullable = False)
    text = db.Column(db.String(length = 100), nullable = False)

    def __repr__(self):

        return self.comment_id


def get_unique_id(post_type):
    
    run = True

    if post_type == "post":

        result_id = unique_id.post_id()

        for i in Posts.query.all().post_id:
            
            if result_id == i:

                get_unique_id("post")
                run = False
                break

        if run:
            return result_id
    

    elif post_type == "comment":

        result_id = unique_id.comment_id()

        for i in Comments.query.all().comment_id:
            
            if result_id == i:

                get_unique_id("comment")
                run = False
                break
        
        if run:
            return result_id
    
def get_post_by_id(post_id):
    
    result = {}

    for i in Posts.query.all():
        
        if i.post_id == post_id:
            result = {"name": i.name, "post_id": i.post_id, "date_time": i.date_time, "title": i.title, "text": i.text}

    return result


def get_comment_by_id(comment_id):
    
    result = {}

    for i in Comments.query.all():
        
        if i.comment_id == comment_id:
            result = {"name": i.name, "post_id": i.post_id, "comment_id": i.comment_id, "date_time": i.date_time, "text": i.text}

    return result

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


if __name__ == "__main__":
    app.run(debug = True)
