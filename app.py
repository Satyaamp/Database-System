from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'admin123'

# Database initialization
def init_db():
    with sql.connect("db3.db") as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                UID INTEGER PRIMARY KEY AUTOINCREMENT,
                UNAME TEXT NOT NULL,
                UENNO INTEGER NOT NULL,
                UADD TEXT NOT NULL,
                UPIN INTEGER NOT NULL
            )
        """)
        con.commit()

# Get database connection
def get_db_connection():
    con = sql.connect("db3.db")
    con.row_factory = sql.Row
    return con

@app.route("/")
@app.route("/index")
def index():
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    con.close()
    return render_template("index.html", datas=data)

@app.route("/ad_user", methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        uname = request.form['uname']
        uenno = request.form['uenno']
        uadd = request.form['uadd']
        upin = request.form['upin']

        # Validate the inputs
        if not uname or not uenno.isdigit() or len(upin) != 6 or not upin.isdigit():
            flash("Invalid input data!", "danger")
            return redirect(url_for("add_user"))  # Redirect to avoid resubmission

        try:
            con = get_db_connection()
            cur = con.cursor()
            cur.execute("INSERT INTO users (UNAME, UENNO, UADD, UPIN) VALUES (?, ?, ?, ?)", 
                        (uname, uenno, uadd, upin))
            con.commit()
            flash("User Added Successfully", "success")
        except sql.Error as e:
            flash(f"Database Error: {str(e)}", "danger")
        finally:
            con.close()

        return redirect(url_for("index"))  # Redirect after adding user to prevent resubmission
    return render_template("ad_user.html")

@app.route("/edit_user/<string:uid>", methods=['POST', 'GET'])
def edit_user(uid):
    if request.method == 'POST':
        uname = request.form['uname']
        uenno = request.form['uenno']
        uadd = request.form['uadd']
        upin = request.form['upin']

        try:
            con = get_db_connection()
            cur = con.cursor()
            cur.execute("UPDATE users SET UNAME = ?, UENNO = ?, UADD = ?, UPIN = ? WHERE UID = ?", 
                        (uname, uenno, uadd, upin, uid))
            con.commit()
            flash("User Updated Successfully", "success")
        except sql.Error as e:
            flash(f"Database Error: {str(e)}", "danger")
        finally:
            con.close()

        return redirect(url_for("index"))  # Redirect after updating user

    # Fetch user data for editing
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE UID = ?", (uid,))
    data = cur.fetchone()
    con.close()

    return render_template("edit_user.html", datas=data)

@app.route("/delete_user/<string:uid>", methods=['GET'])
def delete_user(uid):
    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE UID = ?", (uid,))
        con.commit()
        flash("User Deleted Successfully", "warning")
    except sql.Error as e:
        flash(f"Database Error: {str(e)}", "danger")
    finally:
        con.close()

    return redirect(url_for("index"))  # Redirect to index after deletion

if __name__ == '__main__':
    init_db()  # Initialize database when the app starts
    app.run(debug=True)
