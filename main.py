from flask import g, jsonify, Response
from tools.log import logged
from db.creating_scratch import init_db, db_proxy
import db.creating_scratch as creating_scratch
from globals import app as application
from globals import model
import pages
from tools.mods import get_flag_LOCAL_MODE
from tools.log import logger
import sys
#from model import PricePredictor
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
    return 'Hello'

if __name__ == "__main__":
    application.run(port=5000 if len(sys.argv) == 1 else int(sys.argv[1]), threaded=True)
