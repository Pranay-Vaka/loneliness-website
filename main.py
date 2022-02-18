import unique_id
import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages
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

        for i in Posts.query.all():
            
            if result_id == i.post_id:

                get_unique_id("post")
                run = False
                break

        if run:
            return result_id
    

    elif post_type == "comment":

        result_id = unique_id.comment_id()

        for i in Comments.query.all():
            
            if result_id == i.comment_id:

                get_unique_id("comment")
                run = False
                break
        
        if run:
            return result_id
    

def get_comment_by_id(post_id):
    
    result = []

    for i in Comments.query.all():
        
        if i.post_id == post_id:
            result.append(i)

    return result

def return_all_posts():
    
    final_list = []

    for i in Posts.query.all():
        final_list.append({"post_object": i, "comment_objects": get_comment_by_id(i.post_id)})
    
    return final_list

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods = ["GET", "POST"])
def home_page():
    if request.method == "POST":
        x = datetime.datetime.now()
        name = request.form["name"]
        text = request.form["text"]
        date_time = f"{str(x.day)}/{str(x.month)}/{str(x.year)} {str(x.hour)}:{str(x.minute)}"
        post_id = request.form["post_id"]
        comment_id = get_unique_id("comment") 
        
        if (name or title or text) != "":
            comment = Comments(post_id = post_id, comment_id = comment_id, name = name, date_time = date_time, text = text)
            db.session.add(comment)
            db.session.commit()
            
    return render_template("home.html", posts = return_all_posts()) 


@app.route("/post", methods = ["GET", "POST"])
def post_page():
    message = ""
    if request.method == "POST":
        x = datetime.datetime.now()
        name = request.form["name"]
        title = request.form["title"]
        text = request.form["text"]
        date_time = f"{str(x.day)}/{str(x.month)}/{str(x.year)} {str(x.hour)}:{str(x.minute)}"
        post_id = get_unique_id("post")

        if (name or title or text) == "":
            message = "You must provide a name, a title and some text"
            return render_template("post.html", message = message)

        else:
            post = Posts(post_id = post_id, name = name, date_time = date_time, title = title, text = text)
            db.session.add(post)
            db.session.commit()
            return render_template("post.html", message = message)
    else:
        return render_template("post.html", message = message)


if __name__ == "__main__":
    app.run(debug = True)
