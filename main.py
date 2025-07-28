from flask import Flask, render_template, request, redirect, flash, url_for, json, jsonify, session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os

with open ("config.json" , "r") as c:
    url= json.load(c)["urls"]

app = Flask(__name__)
app.secret_key = "dev"

#configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flaskapp"
app.config["UPLOAD_FOLDER"] = url["upload_location"]

mysql = MySQL(app)

from flask import request, render_template

@app.route("/")
def home():
    # Read pagination config
    limit = int(url['no_posts'])  
    page = request.args.get("page", 1, type=int)  

    offset = (page - 1) * limit

    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM posts")
    total_posts = cur.fetchone()[0]
    total_pages = (total_posts + limit - 1) // limit

    # Get only required posts
    cur.execute(f"SELECT * FROM posts ORDER BY date DESC LIMIT %s OFFSET %s", (limit, offset))
    posta_data = cur.fetchall()
    cur.close()

    post_data = []
    for row in posta_data:
        post_data.append({
            "sno": row[0],
            "title": row[1],
            "slug": row[2],
            "content": row[3],
            "img_file": row[4],
            "author": row[5],
            "date": row[6],
            "sub": row[7]
        })

    return render_template("index.html", url=url, post_data=post_data, page=page, total_pages=total_pages)


@app.route("/about")
def about():
    return render_template("about.html", url=url)

@app.route("/dashboard" , methods=['GET','POST'])
def dashboard():
    if ('user' in session and session ['user'] == url['user']):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM posts;")
        data = cur.fetchall()
        cur.close()
        post_data = []
        for row in data:
            post_data.append({
                "sno": row[0],
                "title": row[1],
                "slug": row[2],
                "content": row[3],
                "img_file": row[4],
                "author":row[5],
                "date": row[6],
                "sub": row[7] 
            })
        return render_template('dashboard.html',url=url,post_data=post_data)

    if request.method=='POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if (username == url['user'] and userpass == url['pass']):
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM posts;")
            data = cur.fetchall()
            cur.close()
            post_data = []
            for row in data:
                post_data.append({
                    "sno": row[0],
                    "title": row[1],
                    "slug": row[2],
                    "content": row[3],
                    "img_file": row[4],
                    "author":row[5],
                    "date": row[6],
                    "sub": row[7] 
                })
            session['user'] = username
            return render_template('dashboard.html', url = url,post_data=post_data)
        else:
            return render_template("login.html", url=url)
    
    return render_template("login.html", url=url)

@app.route("/logout", methods=["POST","GET"])
def logout():
    session.pop('user', None)
    return redirect(url_for("dashboard"))

@app.route("/edit/<int:sno>" , methods=['GET','POST'])
def edit (sno):
    if ('user' in session and session ['user'] == url['user']):
        if request.method=='POST':
            title = request.form.get('title')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_file = request.form.get('img_file')
            author = request.form.get('author')
            sub = request.form.get('sub')

            cur = mysql.connection.cursor()
            if sno == 0:
                cur.execute("""
                INSERT INTO posts (title, slug, content, img_file, author, sub)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, (title, slug, content, img_file, author, sub)) 
                mysql.connection.commit()
                cur.close()

                flash("Submitted successfully!")
                return redirect(url_for("dashboard"))
            else:
                # UPDATE
                cur.execute("""
                    UPDATE posts SET title=%s, slug=%s, content=%s, img_file=%s, author=%s, sub=%s WHERE sno=%s
                """, (title, slug, content, img_file, author, sub, sno))
                mysql.connection.commit()
                cur.close()
                flash("Post updated successfully!")
                return redirect(url_for("dashboard"))

        else:
            cur = mysql.connection.cursor()
            cur.execute(f"""SELECT * FROM posts where sno = {sno} LIMIT 1;""")
            row = cur.fetchone()
            cur.close()
            if row:
                post_data = {
                    "sno": row[0],
                    "title": row[1],
                    "slug": row[2],
                    "content": row[3],
                    "img_file": row[4],
                    "author":row[5],
                    "date": row[6],
                    "sub": row[7] 
                }
            
                return render_template("edit.html",url=url,post_data=post_data,sno=sno)
            elif sno==0:
                post_data = {
                    "sno": "",
                    "title": "",
                    "slug": "",
                    "content": "",
                    "img_file": "",
                    "author": "",
                    "date": "",
                    "sub": ""
                }
                return render_template ("edit.html",url=url, sno=sno, post_data=post_data)
    return redirect(url_for("dashboard"))

@app.route("/delete/<int:sno>" , methods=['GET','POST'])
def delete (sno):
    if ('user' in session and session ['user'] == url['user']):
        cur = mysql.connection.cursor()
        cur.execute(f"""DELETE FROM posts where sno = {sno} LIMIT 1;""")
        mysql.connection.commit()
        cur.close()
        flash("Post deleted successfully!")
        return redirect(url_for("dashboard"))
    return redirect(url_for("dashboard"))

@app.route("/contact")
def contact():
    return render_template("contact.html", url=url)

@app.route("/submit", methods=["POST"])
def submit():
    name2 = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    msg = request.form["message"]

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO contacts (name, phone_num, msg, email)
        VALUES (%s, %s, %s, %s)
    """, (name2, phone, msg, email)) 
    mysql.connection.commit()
    cur.close()

    flash("Submitted successfully!") 
    return redirect(url_for("contact"))


@app.route("/posts", methods=["GET"])
def posts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts ORDER BY date DESC;")
    data = cur.fetchall()
    cur.close()
    post_data = []
    for row in data:
        post_data.append({
            "sno": row[0],
            "title": row[1],
            "slug": row[2],
            "content": row[3],
            "img_file": row[4],
            "author":row[5],
            "date": row[6],
            "sub": row[7] 
        })
    return render_template("allposts.html",post_data=post_data,url=url)

@app.route("/post/<string:post_slug>", methods=["GET"])
def post(post_slug):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE slug = %s LIMIT 1", (post_slug,))
    row = cur.fetchone()
    cur.close()

    if row:
        post_data = {
            "sno": row[0],
            "title": row[1],
            "slug": row[2],
            "content": row[3],
            "img_file": row[4],
            "author":row[5],
            "date": row[6],
            "sub": row[7] 
        }
    else:
        post_data = None

    return render_template("post.html", post_data=post_data, url=url) 


@app.route("/uploader" , methods = ["GET","POST"])
def uploader():
    if ('user' in session and session ['user'] == url['user']):
        if (request.method == "POST"):
            f = request.files["file1"]
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename)))   
            flash("Uploaded successfully!") 
            return redirect(url_for("dashboard"))
        
    return redirect(url_for("dashboard"))



@app.route("/error")
def error():
    return render_template("error.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("enf.html"), 404

if __name__ == "__main__":
    app.run("0.0.0.0",debug=True)





