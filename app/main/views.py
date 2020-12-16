from flask import render_template, url_for
from . import main

@main.route('/')
def index():

    title = 'Home-  Welcome to The House Space Website'
    return render_template('index.html', title = title)
