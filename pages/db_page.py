from tools.log import logged
from db import creating_scratch
from flask import Blueprint
db_page = Blueprint('db_page', __name__, template_folder='templates')

@db_page.route('/show_db', methods=['GET'])
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
