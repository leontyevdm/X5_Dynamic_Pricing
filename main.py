from flask import g, jsonify, Response
from tools.log import logged
from db.creating_scratch import init_db, db_proxy
import db.creating_scratch as creating_scratch
from globals import app as application
import pages
from tools.mods import get_flag_LOCAL_MODE
from tools.log import logger
from model import fit_cached_models
import sys
from globals import *
from model import PricePredictor
from datetime import datetime as date

@application.errorhandler(Exception)
def handle_error(error):
    if get_flag_LOCAL_MODE():
        raise error
    else:
        logger.error("Fatal error in main loop", show_exc_info=True)

    response = Response(str(error), 500)
    return response


@application.route('/', methods=['GET'])
def describe():
    # cache models test
    origin = 'MOW'
    dest = 'LED'
    # '%d.%m.%y'
    current_date = '12.4.21'
    current_date = date.strptime(current_date, '%d.%m.%y')
    flight_date = '30.4.21'
    flight_date = date.strptime(flight_date, '%d.%m.%y')
    print(get_model().predict_actual_queried_prices_for(origin, dest, current_date, flight_date, 3, None))
    return 'Hello'


if __name__ == "__main__":
    fit_cached_models()
    application.run(port=5000 if len(sys.argv) == 1 else int(sys.argv[1]), threaded=True)
