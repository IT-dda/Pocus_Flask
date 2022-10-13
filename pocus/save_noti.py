from .database import Database

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

    pk = db.executeAll("SELECT LAST_INSERT_ID()")

    return pk[0]['LAST_INSERT_ID()']
