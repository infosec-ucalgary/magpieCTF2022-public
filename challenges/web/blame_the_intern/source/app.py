import os
import random
from flask import Flask, render_template_string, request

# Base flask app
app = Flask(__name__)

# Handle app state
STATE = {
    "success": False,
    "id": 56645,
    "username": "timtheintern",
    "secret": "THISISASUPERSECRETKEY",
    "flag": os.environ['FLAG']
}

def gen_useless_flag():
    PREFIX="fake{"
    SUFFIX="}"
    return PREFIX + str(random.randint(1000000,10000000)) + SUFFIX

# Handle requests to /
@app.route("/")
def index():
    return render_template_string("<!DOCTYPE html>" \
                                  "<htmL>" \
                                  "<head>" \
                                  "<title>Flag Licenser</title>" \
                                  '<link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet">' \
                                  "</head>" \
                                  "<body>" \
                                  "<!-- This is our default flask template -->" \
                                  "<!-- Remove template string rendering or sanitize input before pushing to production. -->" \
                                  "<div class='w-full md:w-1/3 mx-auto my-8 text-center bg-gray-300 border-0 rounded-xl p-4'>" \
                                  "<span class='text-4xl'>Input license key:</span><br>" \
                                  "<span class='text-xl'>Enter the license key to retrieve its respsective flag.</span><br>" \
                                  "<form action='submit' method='post'>" \
                                  "<input class='my-2' type='text' name='try'/><br>" \
                                  "<input class='my-2' type='submit'/>" \
                                  "</form>" \
                                  "</div>" \
                                  "</body>" \
                                  "</html>", state=STATE)


# Handle POST requests to /submit
@app.route("/submit", methods=["POST"])
def submit():
    result=request.form.to_dict(flat=False)
    STATE['result'] = result
    input_string = f"{result['try'][0]}"
    count_string = f"{gen_useless_flag()}"
    return render_template_string("<!DOCTYPE html>" \
                                  "<html>" \
                                  "<head>" \
                                  "<title>Flag Licenser</title>" \
                                  '<link href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css" rel="stylesheet">' \
                                  "<head>" \
                                  "<body>" \
                                  "<!-- This is our default flask template -->" \
                                  "<!-- Remove template string rendering or sanitize input before pushing to production. -->" \
                                  "<div class='w-full lg:w-1/3 mx-auto my-8 bg-gray-300 lg:border-0 lg:rounded-xl p-4'>" \
                                  "<div class='text-center'>" \
                                  "<span class='text-4xl'>Results</span><br>" \
                                  f"<span class='text-md'>Your key is: </span><br>" \
                                  f"<span class='text-xl font-bold'>{input_string}</span><br>" \
                                  "<span class='text-md'>The flag is: </span><br>" \
                                  f"<span class='text-xl font-bold'>{count_string}</span><br>" \
                                  "</div>" \
                                  "<a class='button' href='/'>Try Again</a>" \
                                  "</div>" \
                                  "</body>" \
                                  "</html>", state=STATE)


# Main
if __name__== "__main__":
    app.run(debug=True, host="0.0.0.0")
