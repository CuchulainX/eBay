# coding: utf-8


import urllib
import re
from StringIO import StringIO
import gzip
import logging


def gethtml(url):
    """
    :param url:
    :return:
    """
    print u'正在读取网页...'
    p = urllib.urlopen(url, proxies={'http': 'http://192.168.11.49:3128'})
    html = p.read()
    print u'网页读取完成。'
    return html


def uncompress(html):
    """
    :param html: 卖家网页源码，gzip压缩文档
    :return: 解压缩后的网页源码
    """
    buf = StringIO(html)
    f = gzip.GzipFile(fileobj=buf)
    html2 = f.read()
    return html2


def item_sold(html):
    """
    :return: 销量
    """
    s = re.findall(r'(\d+) sold', html)
    if s:
        return int(s[0])


def item_loacation(html):
    """
    :return:
    """
    s = re.findall(r'', html)
    return s


def store_list(keyword):
    keyword_url = 'http://stores.ebay.com/_si.html?tokenstring=VFrYUAwAAAA%3D&_sofindtype=7' \
                  + '&_nkw=%s&rd=ON' % urllib.quote(keyword)
    html = gethtml(keyword_url)
    storename = re.findall(r'<span content="(.*?)" itemprop="name"', html, re.DOTALL)
    storeurl = re.findall(r'href="(http://stores.ebay.com/.*?)" itemprop="url"', html, re.DOTALL)
    r = []
    for i in range(0,len(storename)):
        tmp = {}
        tmp['storename'] = storename[i]
        tmp['storeurl'] = storeurl[i]
        r.append(tmp)
    return r


def store_feedback(storename):
    _store_url = 'http://stores.ebay.com/%s' % storename
    raw = gethtml(_store_url)
    try:
        html = uncompress(raw)
    except IOError:
        html = raw
    finally:
        print u'网页下载完成。'

    feedback_score1 = re.findall('feedback score is (\d+)', html)
    feedback_score2 = re.findall('Feedback Score Of (\d+)', html)
    feedback_rate1 = re.findall('has ([\d\.]+%)', html)
    feedback_score = feedback_score1 + feedback_score2
    feedback_rate = feedback_rate1
    if len(feedback_score):
        score = feedback_score[0]
    else:
        score = None
    if len(feedback_rate):
        rate = feedback_rate[0]
    else:
        rate = None
    return score, rate


# url = 'http://www.ebay.com/itm/281589160700'
# html = gethtml(url)
# s = parse_sold(html)

# 解析某一关键词的匹配卖家列表
#_url = 'http://stores.ebay.com/_si.html?tokenstring=VFrYUAwAAAA%3D&_sofindtype=7&_nkw=hand+dryer&rd=ON'
# STORES = store_list(_url)













