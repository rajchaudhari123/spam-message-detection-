from flask import Flask, render_template, request, redirect, url_for
import pickle
import sklearn
import warnings
import mysql.connector

warnings.filterwarnings("ignore", category=sklearn.exceptions.InconsistentVersionWarning)

app = Flask(__name__)

# Load pre-trained Naive Bayes model
with open("Naive_model.pkl", "rb") as file:
    pipe = pickle.load(file)
try:    # Connect to MySQL with correct credentials

     mydb = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="scam"
)
     mycursor = mydb.cursor()

     mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
except:
    print("not connect")




@app.route('/', methods=["GET", "POST"])
def main_function():
    if request.method == "POST":
        email = request.form.get('email', '')
        if email:
            output = pipe.predict([email])[0]
            return render_template("show.html", prediction=output)
        else:
            return render_template("index.html", error="Email field is empty")
    else:
        return render_template("index.html")

@app.route('/login.html', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username','')
        password = request.form.get('password','')

        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, password)
        mycursor.execute(sql, val)
        mydb.commit()

        return render_template("login.html", username=username)
    else:
        return render_template("login.html")

@app.route('/show.html')
def show():
    return render_template('show.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/sol.html')
def sol():
    return render_template('sol.html')

if __name__ == '__main__':
    app.run(debug=True)
