from flask import Blueprint


api = Blueprint('api', __name__)
from mars.test import views
from mars.users import views


@api.after_request
def after_request(response):
    """默认返回类型: text/html text/plain, 统一修改为json"""
    if response.headers.get('Content-Type').startswith('text'):
        response.headers['Content-Type'] = 'application/json'
    return response

