from flask import Blueprint, request
from ..database import Database

bp = Blueprint('noti', __name__, url_prefix='/noti')
db = Database()

def table_log(p1, p2, p3):
    sql = f"INSERT INTO pocus.Log(user_id, warning, isUpper) VALUES ({p1}, '{p2}', {p3})"
    db.execute(sql)
    db.commit()

    pk = db.executeAll("SELECT LAST_INSERT_ID()")

    return pk[0]['LAST_INSERT_ID()']

def table_ss(p1, s1, s2, s3, s4):
    sql = f"INSERT INTO pocus.SS(log_id, ss1, ss2, ss3, ss4) VALUES ({p1}, {s1}, {s2}, {s3}, {s4})"
    db.execute(sql)
    db.commit()

    row = db.executeAll("SELECT * FROM pocus.SS")

    return f'{row}'

@bp.route('/', methods=['GET'])
def noti_get():
    return 'Notifications'


@bp.route('/save', methods=['POST'])
def noti_test():
    req = request.get_json()

    user_id = req['user_id']
    warning = req['warning']
    isUpper = req['isUpper']
    print(user_id, warning, isUpper)
    print(type(user_id), type(warning), type(isUpper)) # str, str, str
    pk = table_log(user_id, warning, isUpper)
    print(pk)

    if isUpper == '0':
        ss1 = req['ss1']
        ss2 = req['ss2']
        ss3 = req['ss3']
        ss4 = req['ss4']
        table_ss(pk, ss1, ss2, ss3, ss4)

    return 'done'
