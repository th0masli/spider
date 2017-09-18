# -*- coding: utf-8 -*-
import re
import logging
import urllib2
import lxml.html

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='main.log',
                    filemode='w')


def get_doc(url):
    """
    get doc through url
    :param url: ip
    :return: doc object for xpath parsing
    """
    err = None
    doc = None
    for i in range(3):
        try:
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
            headers = {"User-Agent": user_agent}
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            content = response.read()
            doc = lxml.html.fromstring(content)
            err = None
            break
        except Exception, e:
            info = "get_doc try %d times!" % i
            logging.info(info)
            err = str(e)
    if err is None:
        return doc
    else:
        logging.error("get_doc error: " + err)
        return None


def get_class_dct():
    """
    get ids and names；
    :return: key: id，value: name
    """
    dct_class_id_name = {}
    url = "http://word.iciba.com/?action=index&reselect=y"
    doc = get_doc(url)
    if doc is None:
        return dct_class_id_name
    err = None
    for i in range(3):
        try:
            lst_id = doc.xpath('//*[@id="mainwordlist"]/li/@class_id')
            lst_has_child = doc.xpath('//*[@id="mainwordlist"]/li/@has_child')
            for j, id in enumerate(lst_id):
                if lst_has_child[j] == '1':
                    xpath_name_1 = '//*[@id="mainwordlist"]/li[@class_id="%s"]/h3/text()' % id
                    name_1 = doc.xpath(xpath_name_1)[0]
                    xpath_id = '//*[@id="mainwordlist"]/li[@class_id="%s"]/div/ol/li/@class_id' % id
                    xpath_name = '//*[@id="mainwordlist"]/li[@class_id="%s"]/div/ol/li/a/h4/text()' % id
                    lst_id_tmp = doc.xpath(xpath_id)
                    lst_name_tmp = doc.xpath(xpath_name)
                    for k in range(len(lst_id_tmp)):
                        dct_class_id_name[int(lst_id_tmp[k])] = (name_1, lst_name_tmp[k])
                else:
                    xpath_name_1 = '//*[@id="mainwordlist"]/li[@class_id="%s"]/h3/text()' % id
                    name_1 = doc.xpath(xpath_name_1)[0]
                    dct_class_id_name[int(id)] = ('', name_1)
            err = None
            break
        except Exception, e:
            info = "get_class_dct try %d times!" % i
            logging.info(info)
            err = str(e)
    if err is not None:
        logging.error("get_class_dct error: " + err)
    return dct_class_id_name


def test():
    url = "http://word.iciba.com/?action=words&class=11&course=1"
    doc = get_doc(url)
    word_list_1_name = doc.xpath('//*[@id="word_list_1"]/li/div[1]/span/text()')
    word_list_2_name = doc.xpath('//*[@id="word_list_2"]/li/div[1]/span/text()')
    word_list_name = word_list_1_name + word_list_2_name
    # word_list_1_sound = doc.xpath('//*[@id="word_list_1"]/li/div[2]/strong/text()')
    # word_list_2_sound = doc.xpath('//*[@id="word_list_2"]/li/div[2]/strong/text()')
    # word_list_sound = word_list_1_sound + word_list_2_sound
    # word_list_1_translation = doc.xpath('//*[@id="word_list_1"]/li/div[3]/span/text()')
    # word_list_2_translation = doc.xpath('//*[@id="word_list_2"]/li/div[3]/span/text()')
    # word_list_translation = word_list_1_translation + word_list_2_translation
    word_list_1_audio = doc.xpath('//*[@id="word_list_1"]/li/div[2]/a/@id')
    word_list_2_audio = doc.xpath('//*[@id="word_list_2"]/li/div[2]/a/@id')
    word_list_audio = word_list_1_audio + word_list_2_audio
    print len(word_list_name)
    for i in range(len(word_list_name)):
        print word_list_name[i].strip(), word_list_audio[i]


if __name__ == '__main__':
    test()
    # tmp = get_class_dct()
    # for k, v in tmp.items():
    #     print "http://word.iciba.com/?action=courses&classid=%d" % k
    #     print v[0], v[1]
