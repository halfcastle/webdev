
from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")
    #return "hi there"


def get_message_db():
  if 'message_db' not in g:
    g.message_db = sqlite3.connect("messages_db.sqlite")
  cmd = "CREATE TABLE IF NOT EXISTS messages (id INT, handle TEXT, message TEXT)"
  cursor = g.message_db.cursor()
  cursor.execute(cmd)

  return g.message_db

def insert_message(request):
  messagey=request.form["message"]
  namey=request.form["name"]
  db=get_message_db()
  cursor = db.cursor()
  cursor.execute("SELECT COUNT(*) FROM messages;")
  row_n=cursor.fetchone()[0] + 1 #setting id number as 1+number of rows
  cursor.execute("INSERT INTO messages (id, message, handle) VALUES (?, ?, ?)", (row_n, messagey, namey))
  db.commit()
  db.close()

@app.route('/submit/', methods=['POST', 'GET'])
def submit():
  if request.method == 'GET':
    return render_template('submit.html')
  else:
    insert_message(request)
    return render_template("submit.html", thanks=True)
    #also returns message thanking user for their submissions

def random_messages(n):
  db = get_message_db()
  cursor = db.cursor()
  cursor.execute("SELECT COUNT(*) from messages")
  row_n=cursor.fetchone()[0]
  if n>row_n:
    n=row_n
  randMessages=cursor.execute(f"SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}").fetchall()
  db.close()
  return randMessages

@app.route('/view/')
def viewy():
  display=random_messages(5)
  return render_template("view.html", messages=display)
 
