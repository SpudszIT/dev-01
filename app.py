from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # for sessions

# Minimal in-memory user "database"
users = {}


@app.route("/dashboard")
def dashboard():
    # Check if user is logged in
    if "user" not in session:
        return redirect(url_for("signin"))

    user_email = session["user"]
    return render_template("dashboard.html", email=user_email)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email not in users or users[email] != password:
            error = "Invalid email or password."
        else:
            session["user"] = email
            return redirect(url_for("home"))

    return render_template("sign-in.html", error=error, email=request.form.get("email"))

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        # Simple validation
        if not email or not password or not confirm:
            error = "All fields are required."
        elif password != confirm:
            error = "Passwords do not match."
        elif email in users:
            error = "Email already registered."
        else:
            users[email] = password  # save user
            session["user"] = email  # log them in
            return redirect(url_for("home"))

    return render_template("register.html", error=error, email=request.form.get("email"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/games")
def games():
    return render_template("games.html")

@app.route("/movies")
def movies():
    return render_template("movies.html")

@app.route("/books")
def books():
    return render_template("books.html")

if __name__ == "__main__":
    app.run(debug=True)
