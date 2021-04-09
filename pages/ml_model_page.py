from tools.log import logged, logger
from tools.mods import get_flag_DEV_MODE, set_flag_DEV_MODE

from flask import Blueprint
from db import creating_scratch
ml_model_page = Blueprint('ml_model_page', __name__, template_folder='templates')



@ml_model_page.route('/show_db', methods=['POST'])
@logged
def show_db():
    creating_scratch.see_elem_in_all_tables()
    return '200'

@db_page.route('/create_or_connect_to_db', methods=['GET'])
@logged
def create_db():
    creating_scratch.create_or_connect_to_db()
    return 'ok'

@db_page.route('/reset_db', methods=['GET'])
@logged
def reset_db():
    creating_scratch.reset_db()
    return 'ok'

@db_page.route('/init_db', methods=['GET'])
@logged
def init_db():
    creating_scratch.init_db()
    return 'ok'
