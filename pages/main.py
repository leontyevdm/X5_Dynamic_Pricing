from globals import get_app

from pages.mod_control_page import mod_control_page
from pages.db_page import db_page
from pages.main_page import main_page
from pages.sign_page import sign_page

get_app().register_blueprint(mod_control_page)
get_app().register_blueprint(db_page)
get_app().register_blueprint(main_page)
get_app().register_blueprint(sign_page)