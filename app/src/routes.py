from app import db
from flask import render_template, flash, redirect, url_for, request, jsonify, send_file, current_app
import uuid
import sqlalchemy as sqla

from app.src import src_blueprint as src
from app.src.forms import ParseForm

import requests
from bs4 import BeautifulSoup #pip install bs4
import pandas
from openpyxl import load_workbook
from werkzeug.utils import secure_filename
import os
from io import StringIO


@src.route('/', methods=['GET', 'POST'])
@src.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@src.route('/parse', methods=['GET', 'POST'])
def parse():   
    form = ParseForm()
    if form.validate_on_submit():
        if form.link.data and form.file.data:

            url = form.link.data
            try:
                load_web_page = requests.get(url, timeout=20)
                load_web_page.raise_for_status()
            except requests.RequestException as e:
                flash(f"Could not fetch that URL: {e}", "warning")
                return redirect(url_for("src.parse"))
            soup_page_parser = BeautifulSoup(load_web_page.content, 'html.parser')
            target_table = soup_page_parser.find("table", {"class": "datatable"})
            if target_table is None:
                flash('Could not find a table with class="datatable".', 'warning')
                return redirect(url_for('src.parse'))
            data_frame = pandas.read_html(StringIO(str(target_table)))[0] #extract from first table found with that name
            print(data_frame.head(5))

            
            upload = form.file.data
            filename = secure_filename(upload.filename)

            if not filename.lower().endswith(".xlsx"):
                flash("Please upload an .xlsx file.", "warning")
                return redirect(url_for("src.parse"))
            
            upload_dir = os.path.join(current_app.instance_path, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            unique_name = f"{uuid.uuid4().hex}_{filename}"

            save_path = os.path.join(upload_dir, unique_name)
            upload.save(save_path)


            sheet_name = "Sheet1"

            wb = load_workbook(save_path)
            if sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
            else:
                ws = wb.create_sheet(sheet_name)

            is_empty = (ws.max_row == 1 and ws.max_column == 1 and ws["A1"].value is None)
            start_row = 1 if is_empty else ws.max_row + 1

            with pandas.ExcelWriter(save_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                data_frame.to_excel(writer, sheet_name=sheet_name, index=False, header=(start_row == 1), startrow=start_row-1)

            return send_file(save_path, as_attachment=True, download_name=filename)

        else: 
            flash('Please provide both a link and file.', 'warning')
            return redirect(url_for('src.parse'))
    return render_template('parse.html', form=form)