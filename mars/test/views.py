from flask import jsonify, current_app

from mars.routes import api
from mars import redis_store, logger


@api.route('/index', methods=['GET'])
def index():
    """write you func"""

    return jsonify(errcode=200, errmsg="ok")

