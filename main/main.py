from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world"

@app.route("/{Stock}")
def about(Stock):
    return render_template(f"Stock/Details/{Stock}.html")


if __name__ == '__main__':
   app.run()