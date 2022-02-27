from flask import Flask, render_template
import random, os
import requests
import json

app = Flask(__name__)

fn_res = requests.get("https://www.randomlists.com/data/names-first.json")
first_names = json.loads(fn_res.text)["data"]

ln_res = requests.get("https://www.randomlists.com/data/names-surnames.json")
last_names = json.loads(ln_res.text)["data"]
testimonials = ["I would be lost without Mom & Pops NTF Flags.",
                "Without Mom & Pops NTF Flags, we would have gone bankrupt by now. Your company is truly upstanding and is behind its product 100%. Mom & Pops NTF Flags should be nominated for service of the year.",
                "I made back the purchase price in just 48 hours! I will recommend you to my colleagues. It's all good.",
                "Mom & Pops NTF Flags should be nominated for service of the year. No matter where you go, Mom & Pops NTF Flags is the coolest, most happening thing around! Mom & Pops NTF Flags has really helped our business. Thank you so much for your help.",
                "Man, this thing is getting better and better as I learn more about it. We have no regrets! I'd be lost without Mom & Pops NTF Flags.",
                "I don't know what else to say.",
                "Mom & Pops NTF Flags was the best investment I ever made. Thanks for the great service. I don't always clop, but when I do, it's because of Mom & Pops NTF Flags. No matter where you go, Mom & Pops NTF Flags is the coolest, most happening thing around!",
                "Mom & Pops NTF Flags has completely surpassed our expectations. I can't say enough about Mom & Pops NTF Flags.",
                "We've seen amazing results already. Your company is truly upstanding and is behind its product 100%.",
                "It's all good. You won't regret it.",
                "Mom & Pops NTF Flags should be nominated for service of the year. Very easy to use. Definitely worth the investment. We were treated like royalty.",
                "I can't say enough about Mom & Pops NTF Flags. You guys rock!",
                "It's really wonderful. Mom & Pops NTF Flags is the next killer app. Mom & Pops NTF Flags is both attractive and highly adaptable. I would like to personally thank you for your outstanding product.",
                "I would like to personally thank you for your outstanding product.",
                "I love Mom & Pops NTF Flags. I will let my mum know about this, she could really make use of Mom & Pops NTF Flags!",
                "I bought a Mom & Pops NTF Flag and met the love my life the next day.  I sold it to a Twitter bot who also owned a bunch of ugly monkey jpegs and it paid for our wedding.  Thanks Mom & Pop!",
                "I tweeted to Elon Musk that I couldn't pay my medical bills and he bought me one of these.  Now I own a rhinoceros!",
                "I used to buy and sell QR codes.  But now I only trade in Mom & Pops NFT Flags!",
                "I was walking through the park and someone hit me on the head with a bowling pin.  When I woke up, I owned one of these.  Thanks Mom & Pop!",
                "I keep mine in a binder under my bed next to my Pogs!",
                "When my collection of NFTs of the covers of the Animorph books lost all value, I thought it was over for me.  Then I started buying Mom & Pops NFT Flags and proudly fly paper copies of them from my yatch!",
                "Help, my daughter used my credit card to buy this.  How do I reverse the charge!?",
                "I live by the three N's: Nutritious SpaghettiOs, NCIS: New Orleans, and NFT Flags from Mom & Pops!",
                "They're certainly not crime!",
                "When the tax man came asking about how I'd been making, I showed him my Mom & Pops NFT Flag and now he owns 37 of them!",
                "I used to live with regrets, now I live with the promise of endless possibilities thanks to my Mom & Pops NFT Flag!",
                ]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/turn-key")
def turnkey():
    return render_template("turn-key.html")

@app.route("/mission-impossible")
def missionimpossible():
    return render_template("mission-impossible.html")

@app.route("/momandpops-employees")
def momandpops_employees():
    return render_template("momandpops-employees.html")

@app.route("/NFT")
def NFT():
    fn = first_names[random.randrange(0, len(first_names))]
    ln = last_names[random.randrange(0, len(last_names))]
    name = fn + " " + ln

    price = round(random.uniform(30000.00, 300000.00), 2)

    testimonial = random.choice(testimonials)

    path = os.path.dirname(os.path.abspath(__file__))
    displayNFT = random.choice(os.listdir(str(path) + "/static/img/nft-flags/"))
    return render_template("NFT.html", image=("/static/img/nft-flags/" + str(displayNFT)), buyer=name, price=price, testimonial=testimonial)

if __name__ == '__main__':
	app.run(debug=False)
