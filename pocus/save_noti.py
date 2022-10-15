from .database import Database


def table_log(p1, p2, p3):
    db = Database()
    sql = "INSERT INTO pocus.Log(user_id, warning, isUpper) VALUES (%s, '%s', %s)" % (p1, p2, p3)
    db.execute(sql)
    db.commit()

    pk = db.executeAll("SELECT LAST_INSERT_ID()")

    db.close()

    return pk[0]['LAST_INSERT_ID()']


def table_ss(p1, s1, s2, s3, s4):
    db = Database()
    sql = "INSERT INTO pocus.SS(log_id, ss1, ss2, ss3, ss4) VALUES (%s, %s, %s, %s ,%s)" % (p1, s1, s2, s3, s4)
    db.execute(sql)
    db.commit()

    pk = db.executeAll("SELECT LAST_INSERT_ID()")

    db.close()

    return pk[0]['LAST_INSERT_ID()']
