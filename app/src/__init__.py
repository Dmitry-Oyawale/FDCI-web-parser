from flask import Blueprint

src_blueprint = Blueprint('src', __name__)

from app.src import routes