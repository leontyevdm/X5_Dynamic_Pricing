from globals import get_app
import  json
from pages.mod_control_page import mod_control_page
from pages.db_page import db_page
from pages.main_page import main_page
from pages.ml_model_page import ml_model_page

get_app().register_blueprint(ml_model_page)
get_app().register_blueprint(main_page)