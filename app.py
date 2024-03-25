from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():  
    return render_template("index.html", title="Homepage")

@app.route('/about')
def about():  
    return render_template("about.html", title="About Us")

@app.route('/contact')
def contact():  
    return render_template("contact.html", title="Contact Us")

@app.route('/photogallery') 
def photogallery(): 
    return render_template("photogallery.html", title="Photo Gallery")


if __name__ == '__main__':
    app.run()
