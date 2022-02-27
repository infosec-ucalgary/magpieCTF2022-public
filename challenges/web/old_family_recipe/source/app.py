from flask import Flask, render_template_string, session, request, send_from_directory
from flask.templating import render_template

app = Flask(__name__, static_folder='static')

app.secret_key = "flour_sugar_chocolate_and_lotsalove"
expected_browser = "Mozilla/4.0 (compatible; MSIE 6.01; Windows NT 6.0)"

@app.route("/", methods=['GET','POST'])
def index():
    if "admin" not in session:
        session["admin"] = False
    if request.method == 'POST':
        session['username'] = request.form['username']
        if session["admin"] == True:
            return render_template("acct.html")
        else:
            return render_template("invalid.html")
                
    return render_template("login.html")

@app.route("/robots.txt")
@app.route("/sitemap.xml")
def robotsNeedLoveToo():
    if request.headers.get("User-Agent") == expected_browser:
        return send_from_directory(app.static_folder, "robots.txt")
    else:
        return render_template_string("Unknown User-Agent! Supported Browsers: Internet Explorer 6.01")

if __name__== "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)