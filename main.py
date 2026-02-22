from flask import Flask, render_template,request,redirect,url_for,flash
import requests
import smtplib
import os




app = Flask(__name__)
# ✅ Add this line (must be before using flash or session)
app.secret_key = "a_very_secret_random_string_12345"

# JSON API with all posts
POSTS_URL = "https://api.npoint.io/50edbc688818f379f5d9"
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

@app.route("/")
def home():
    response = requests.get(POSTS_URL)
    all_posts = response.json()
    return render_template("index.html", all_posts=all_posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        email_message = f"""Subject: New Contact Message

Name: {name}
Email: {email}
Phone: {phone}
Message:
{message}
"""

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,         # You send it from yourself
                to_addrs=MY_EMAIL,          # You receive it yourself
                msg=email_message.encode("utf-8")
            )

        flash("✅ Your message has been sent successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route("/post/<int:post_id>")
def show_post(post_id):
    all_posts = requests.get(POSTS_URL).json()

    # find post by id
    post = next((p for p in all_posts if p["id"] == post_id), None)

    if not post:
        return "Post not found", 404

    return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)
