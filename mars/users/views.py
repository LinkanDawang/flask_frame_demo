from flask import jsonify, request, session

from mars.routes import api
from mars import db, logger, redis_store
from mars.users.models import UsersModel


@api.route('/register', methods=['POST'])
def register():
    params = request.get_json()
    # 获取参数
    username = params.get('username')
    realname = params.get('realname')
    mobile = params.get('mobile')
    id_char = params.get('id_char')
    pwd = params.get('password')

    user = UsersModel(username=username, realname=realname, mobile=mobile, id_char=id_char)
    user.password = pwd

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(e)
        return jsonify(errno=400, errmsg='mysql添加失败')

    try:  # 创建用户后自动登入
        session['user_id'] = user.id
        session['user_name'] = user.username
        session['mobile'] = user.mobile
    except Exception as e:
        logger.error(e)
        return jsonify(errno=400, errmsg='session设置失败')

    return jsonify(errcode=200, errmsg='ok')


@api.route('/login', methods=['POST'])
def login():
    params = request.get_json()
    mobile = params.get('mobile')
    password = params.get('password')

    if not all([mobile, password]):
        return jsonify(errno=400, errmsg='参数不全')

    try:
        err_count = redis_store.get('err_count_%s' % mobile)
    except Exception as e:
        logger.error(e)
        return jsonify(errno=400, errmsg='获取错误')

    if err_count and int(err_count) >= 5:
        return jsonify(errno=400, errmsg='错误次数上限')

    # 获取用户
    try:
        user = UsersModel.query.filter_by(mobile=mobile).first()
    except Exception as e:
        logger.error(e)
        return jsonify(errno=400, errmsg='查询失败')

    if user is None:
        return jsonify(errno=400, errmsg='用户不存在')
    else:
        if not user.check_password_hash(password):
            try:
                redis_store.incr('err_count_%s' % mobile)  # incr方法为自增方法
                redis_store.expire('err_count_%s' % mobile, 86400)
            except Exception as e:
                logger.error(e)
            return jsonify(errno=400, errmsg='密码输入错误')

    try:
        session['user_id'] = user.id
        session['user_name'] = user.username
        session['mobile'] = user.mobile
    except Exception as e:
        logger.error(e)
        return jsonify(errno=400, errmsg='session设置失败')

    try:
        redis_store.delete('err_count_%s' % mobile)
    except Exception as e:
        logger.error(e)
        return jsonify(errno=400, errmsg='session设置失败')

    return jsonify(errno=200, errmsg='登入成功')


@api.route('/sessions', methods=['GET'])
def check_login():
    username = session.get('user_name')
    user_id = session.get('user_id')
    mobile = session.get('mobile')

    print(username, user_id, mobile)

    return jsonify(errno=200, errmsg='ok')

