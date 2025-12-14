from app import db
from flask import render_template, flash, redirect, url_for, request, jsonify
import sqlalchemy as sqla

from app.src import src_blueprint as src

@src.route('/', methods=['GET', 'POST'])
def index():
    form = None
    return render_template('index.html', form=form)

@src.route('/upload', methods=['GET', 'POST'])
def upload():   
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')