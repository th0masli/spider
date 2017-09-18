# -*- coding: utf-8 -*-
import time
import datetime

from methods import *
from methods2 import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='main.log',
                    filemode='w')


def main():
    origin = 'iciba'
    t0 = time.time()
    db = get_database()
    dct_class = get_class_dct()
    for class_id, class_name_tuple in dct_class.items():
        if grab_or_not(db, class_id):  # skip already crawled pages
            msg = "%d %s %s already grabed!" % (class_id, class_name_tuple[0], class_name_tuple[1])
            logging.info(msg)
            continue
        err_class = None
        class_name_1 = class_name_tuple[0]
        class_name_2 = class_name_tuple[1]
        course = 1
        while True:
            url = "http://word.iciba.com/?action=words&class=%d&course=%d" % (class_id, course)
            doc = get_doc(url)
            if doc is None:
                err_class = 'error'
                continue
            err = None
            for m in range(3):
                try:
                    word_list_1_name = doc.xpath('//*[@id="word_list_1"]/li/div[1]/span/text()')
                    word_list_2_name = doc.xpath('//*[@id="word_list_2"]/li/div[1]/span/text()')
                    word_list_name = word_list_1_name + word_list_2_name
                    word_list_1_sound = doc.xpath('//*[@id="word_list_1"]/li/div[2]/strong/text()')
                    word_list_2_sound = doc.xpath('//*[@id="word_list_2"]/li/div[2]/strong/text()')
                    word_list_sound = word_list_1_sound + word_list_2_sound
                    word_list_1_translation = doc.xpath('//*[@id="word_list_1"]/li/div[3]/span/text()')
                    word_list_2_translation = doc.xpath('//*[@id="word_list_2"]/li/div[3]/span/text()')
                    word_list_translation = word_list_1_translation + word_list_2_translation
                    word_list_1_audio = doc.xpath('//*[@id="word_list_1"]/li/div[2]/a/@id')
                    word_list_2_audio = doc.xpath('//*[@id="word_list_2"]/li/div[2]/a/@id')
                    word_list_audio = word_list_1_audio + word_list_2_audio
                    err = None
                    break
                except Exception, e:
                    err = str(e)
            if err is not None:
                logging.error(err)
                err_class = 'error'
                break
            if len(word_list_name) == 0:
                break
            for i in range(len(word_list_name)):
                err0 = None
                for n in range(3):
                    try:
                        name = word_list_name[i].strip()
                        sound = word_list_sound[i].strip()
                        translation = word_list_translation[i].strip()
                        url_audio = word_list_audio[i]
                        err0 = None
                        break
                    except Exception, e:
                        err0 = str(e)
                if err0 is not None:
                    logging.error(err0)
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor = db.cursor()
                err1 = None
                for j in range(3):
                    try:
                        sql = "INSERT INTO data_iciba " \
                              "(origin, name, url, url_audio, sound, translation, class_id, " \
                              "class_name, father_class_name, create_time, update_time) " \
                              "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', '%s', '%s', '%s') " \
                              "ON DUPLICATE KEY UPDATE " \
                              "url='%s', url_audio='%s', sound='%s', translation='%s', class_id=%d, class_name='%s', " \
                              "father_class_name='%s', update_time='%s';" \
                              % (origin, name, url, url_audio, sound, translation, class_id,
                                 class_name_2, class_name_1, now, now,
                                 url, url_audio, sound, translation, class_id, class_name_2, class_name_1, now)
                        cursor.execute(sql)
                        err1 = None
                        break
                    except Exception, e:
                        name = re.sub(ur"'", ur"\'", name)
                        name = re.sub(ur'"', ur'\"', name)
                        sound = re.sub(ur"'", ur"\'", sound)
                        sound = re.sub(ur'"', ur'\"', sound)
                        translation = re.sub(ur"'", ur"\'", translation)
                        translation = re.sub(ur'"', ur'\"', translation)
                        err1 = str(e)
                if err1 is not None:
                    logging.error("error words: " + name + "***" + translation)
                    logging.error(err1)
                    err_class = "error"
                    break
            for k in range(3):
                try:
                    db.commit()
                    break
                except Exception, e:
                    logging.error(str(e))
                    err_class = "error"
            info = '%d, %s, %s, %d, %d' % (class_id, class_name_1, class_name_2, course, len(word_list_name))
            logging.info(info)
            course += 1
        if err_class is None:  # if no error, save to database
            try:
                cursor = db.cursor()
                sql = "INSERT INTO class_iciba " \
                      "(class_id, class_name, father_class_name) VALUES ('%d', '%s', '%s') " \
                      "ON DUPLICATE KEY UPDATE class_id='%d', class_name='%s', father_class_name='%s';" \
                      % (class_id, class_name_2, class_name_1, class_id, class_name_2, class_name_1)
                cursor.execute(sql)
                db.commit()
            except Exception, e:
                logging.error("Save class information error!")
                logging.error(str(e))
                continue
        else:
            logging.error("class " + str(class_id) + " grab error!")
    close_database(db)
    t1 = time.time()
    msg = "Total time:" + str(t1 - t0)
    logging.info(msg)


if __name__ == '__main__':
    main()
