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

def check_data(s1, s2, s3, s4):
    db = Database()
    sql = "SELECT COUNT(*) from pocus.log left outer join pocus.ss on log.log_id = ss.log_id where ss.ss1 = %s and ss.ss2 = %s and ss.ss3 = %s and ss.ss4 = %s and log.date BETWEEN DATE_ADD(NOW(), INTERVAL -10 SECOND) AND DATE_ADD(NOW(), INTERVAL 10 SECOND)" % (s1, s2, s3, s4)
    rows = db.executeAll(sql)
    db.close()
    return rows

def delete_duplicate(user_id):
    db = Database()
    
    sql = "DELETE s from pocus.ss s, pocus.log a, pocus.log b where s.log_id = a.log_id and a.log_id > b.log_id and a.user_id = %s and b.user_id = %s and a.isUpper = 0 and b.isUpper = 0 and a.date = b.date" % (user_id, user_id)
    rows = db.executeAll(sql)
    db.commit()

    sql = "DELETE a from pocus.log a, pocus.log b where a.log_id > b.log_id and a.user_id = %s and b.user_id = %s and a.isUpper = 0 and b.isUpper = 0 and a.date = b.date" % (user_id, user_id)
    rows = db.executeAll(sql)
    db.commit()

    db.close()
    return rows
