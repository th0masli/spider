# -*- coding: utf-8 -*-
import MySQLdb
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='main.log',
                    filemode='w')


def get_database():
    err = None
    for i in range(3):
        try:
            db = MySQLdb.connect(host="host", user="username", passwd="password",
                                 db="database_name", charset="utf8")
            err = None
            break
        except Exception, e:
            info = "get_database try %d times!" % i
            logging.info(info)
            err = str(e)
    if err is None:
        logging.info("Database connected!")
        return db
    else:
        logging.error("get_database error: " + err)
        return None


def close_database(db):
    err = None
    for i in range(3):
        try:
            db.close()
            err = None
            break
        except Exception, e:
            info = "close_database try %d times!" % i
            logging.info(info)
            err = str(e)
    if err is None:
        logging.info("Database closed!")
    else:
        logging.error("close_database error: " + err)


def grab_or_not(db, class_id):
    """
    Check if it has been crawled；
    :param db: databse connection
    :param class_id: id
    :return: return True if crawled, otherwise return False
    """
    cursor = db.cursor()
    sql = 'SELECT class_id FROM class_iciba WHERE class_id=%d;' % class_id
    cursor.execute(sql)
    res = cursor.fetchall()
    if len(res) == 0:
        return False
    else:
        return True


if __name__ == '__main__':
    db = get_database()
    mark = grab_or_not(db, 16)
    print mark
    close_database(db)
