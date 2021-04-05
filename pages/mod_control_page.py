from tools.log import logged, logger
from tools.mods import get_flag_DEV_MODE, set_flag_DEV_MODE

from flask import Blueprint
mod_control_page = Blueprint('mod_control_page', __name__, template_folder='templates')

@mod_control_page.route('/set_DEV_MODE_True', methods=['GET'])
@logged
def setDEBUG_True():
    set_flag_DEV_MODE(True)
    return 'DEBUG = True'


@mod_control_page.route('/set_DEV_MODE_False', methods=['GET'])
@logged
def setDEBUG_False():
    set_flag_DEV_MODE(False)
    return 'DEBUG = False'


@mod_control_page.route('/get_DEV_MODE_Flag', methods=['GET'])
@logged
def get_debug():
    logger.info(get_flag_DEV_MODE())
    return 'DEBUG = {0}'.format(get_flag_DEV_MODE())