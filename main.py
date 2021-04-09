from flask import g, jsonify, Response
from tools.log import logged
from db.creating_scratch import init_db, db_proxy
import db.creating_scratch as creating_scratch
from globals import app as application
import pages # for init pages
from tools.mods import get_flag_LOCAL_MODE
from tools.log import logger
import sys
from model import PricePredictor
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

@application.before_request
@logged
def before_request():
    '''
    Before request handling you should connect to db
    :return:
    '''

    if 'db' not in g:
        init_db()
        g.db = db_proxy

    g.db.connect(True)

@application.after_request
@logged
def after_request(response):
    '''
    Close db after a request
    :param response:
    :return:
    '''
    g.db.close()
    return response

if __name__ == "__main__":
    creating_scratch.create_or_connect_to_db()
    global model
    model=PricePredictor()
    model.fit()

    global app
    app=application.run(port=5000 if len(sys.argv) == 1 else int(sys.argv[1]), threaded=True)
