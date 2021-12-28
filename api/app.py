from flask import Flask
import db

app = Flask(__name__)

@app.route("/")
def test():
    return "Connected to the data base!"

if __name__ == '__main__':
    app.run()
