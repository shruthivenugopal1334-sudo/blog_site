from flask import Flask, render_template, request, redirect,jsonify
import sqlite3
from markupsafe import escape
import os

app = Flask(__name__)

# Create database and table if not exists
def init_db():
    conn = sqlite3.connect("blog.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            comment TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# About Page
@app.route("/about")
def about():
    return render_template("about.html")

# Posts Page
@app.route("/posts", methods=["GET", "POST"])
def posts():
    conn = sqlite3.connect("blog.db")
    c = conn.cursor()

    if request.method == "POST":
        name = escape(request.form["name"])
        comment = escape(request.form["comment"])
        c.execute("INSERT INTO comments (name, comment) VALUES (?, ?)", (name, comment))
        conn.commit()
        return redirect("/posts")  # Refresh page to show new comment

    c.execute("SELECT name, comment FROM comments")
    comments = c.fetchall()
    conn.close()

    # Convert to list of dicts for template
    comments_list = [{"name": row[0], "comment": row[1]} for row in comments]
    return render_template("posts.html", comments=comments_list)

# Contact Page
@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
    # Temporary storage for comments
comments = []

# API endpoint for comments
@app.route('/api/comments', methods=['GET', 'POST'])
def api_comments():
    if request.method == 'POST':
        data = request.get_json()  # Receive JSON from frontend
        comments.append(data)      # Save the new comment
        return jsonify({"message": "Comment added!", "comments": comments}), 201
    else:
        return jsonify(comments)   # Return all comments
    

@app.route('/api/contact', methods=['POST'])
def contact_api():
    data = request.get_json()
    # Save the message, or just print for now
    print(data)

    return jsonify({"message": "Message received!"})   

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Render will set PORT, local defaults to 5000
    app.run(host="0.0.0.0", port=port, debug=True)

