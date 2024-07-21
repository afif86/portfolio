import os
from flask import Flask, render_template, send_from_directory
import requests
from dotenv import load_dotenv


# creates a Flask application requiremnts
app = Flask(__name__)

load_dotenv()
URL = os.getenv('URL', default='http://localhost:5000/')  
IMAGE_URL = os.getenv('IMAGE_URL', default='http://localhost:5000/')          


def query_maker(keys: list) -> str:
    
    def get_populate(name: str) -> str:
        if name == "table":
            return "populate[table][populate][about][populate][template][populate]=*"
        return f"populate[{name}][populate]=*"

    output = ""
    for i, k in enumerate(keys):
        if i==0:
           output= "?" + get_populate(k)
        else:
            output = output + "&" + get_populate(k)

    return output


# get data from the form admin panel 
def get_data(path, keys: list=[]): 
    res = requests.get(URL+ path + query_maker(keys))
    if res.status_code != 200:
        return None
    data = res.json().get('data', {})
    if isinstance(data, dict): # if it's single-collection like home
        return data.get("attributes", {})
    return data

MENU = get_data('menu' , ['menu', 'logo'])
FOOTER = get_data('footer')
SOCIAL = [i.get('attributes', {}) for i in get_data('socials')]
HOME = get_data('home', ['eduinfo', 'skills', 'image', 'table', 'source', 'blog']) 
ABOUT = get_data('about', ['image', 'my_story_1', 'my_story_2', 'skill', 'hobby1_img',
                            'hobby2_img', 'hobby3_img', 'hobby4_img']) 
POSTS = get_data('posts', ['image', 'categories'])
EDUINFO = HOME.get('eduinfo', [])  
CONTACT = get_data('contact', ['contact_image'])
PORTFOLIO = get_data('portfolio', [])


# TODO: remove blog from home. 

@app.route('/')
def index():
    return render_template('index.html', menu=MENU, home=HOME, 
                           social=SOCIAL, image_url=IMAGE_URL, eduinfo=EDUINFO,
                             footer=FOOTER, posts= POSTS)

@app.route('/about')
def about():
    return render_template('about.html', about=ABOUT, menu=MENU, social=SOCIAL,
                           image_url=IMAGE_URL, footer=FOOTER)

@app.route('/contact')
def contact():
    return render_template('contact.html', contact=CONTACT, menu=MENU, social=SOCIAL, 
                           image_url=IMAGE_URL, footer=FOOTER)

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', menu=MENU, footer=FOOTER, 
                           social=SOCIAL, image_url=IMAGE_URL)

# Custom static data
@app.route('/uploads/<path:filename>')
def custom_static(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    app.run(debug=True)
