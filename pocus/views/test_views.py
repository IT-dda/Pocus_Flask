from ..database import Database
from flask import Blueprint

bp = Blueprint('test', __name__, url_prefix='/test')
db = Database()


# INSERT 함수 예제
@bp.route('/insert', methods=['GET'])
def insert():
    sql = "INSERT INTO pocus.User(id, password) VALUES('testtestid', '1234')"
    db.execute(sql)
    db.commit()

    sql = "SELECT * FROM pocus.User"
    row = db.executeAll(sql)

    return f'{row}'


# SELECT 함수 예제
@bp.route('/select', methods=['GET'])
def select():
    sql = "SELECT * FROM pocus.User"
    row = db.executeAll(sql)

    return f'{row}'


# UPDATE 함수 예제
@bp.route('/update', methods=['GET'])
def update():
    sql = "UPDATE pocus.User SET password='%s' WHERE id='testtestid'" % ('0000')
    db.execute(sql)
    db.commit()

    sql = "SELECT * FROM pocus.User"
    row = db.executeAll(sql)

    return f'{row}'
