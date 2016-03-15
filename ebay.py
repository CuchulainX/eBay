# coding: utf-8


import urllib
import re
from StringIO import StringIO
import gzip

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


def parse_sold(html):
    """
    :return: 销量
    """
    s = re.findall(r'(\d+) sold', html)
    if s:
        return int(s[0])


def parse_loacation(html):
    """
    :return:
    """
    s = re.findall(r'', html)
    return s

def parse_store_list(html):
    storename = re.findall(r'<span content="(.*?)" itemprop="name"', html, re.DOTALL)
    storeurl = re.findall(r'href="(http://stores.ebay.com/.*?) itemprop="url"', html, re.DOTALL)
    r = []
    for i in range(0,len(storename)):
        tmp = {}
        tmp['storename'] = storename[i]
        tmp['storeurl'] = storeurl[i]
        r.append(tmp)
    return r


def uncompress(html):
    """
    :param html: 卖家网页源码，gzip压缩文档
    :return: 解压缩后的网页源码
    """
    buf = StringIO(html)
    f = gzip.GzipFile(fileobj=buf)
    html2 = f.read()
    return html2


#url = 'http://www.ebay.com/itm/281589160700'
#html = gethtml(url)
#s = parse_sold(html)

# 解析某一关键词的匹配卖家列表
_url = 'http://stores.ebay.com/_si.html?tokenstring=VFrYUAwAAAA%3D&_sofindtype=7&_nkw=hand+dryer&rd=ON'
store_list = parse_store_list(_url)

# 获取卖家信息
for i in store_list:
    _store_url = 'http://stores.ebay.com/%s' % i['storename']
    html = uncompress(gethtml(_store_url))
    feedback_score = re.findall('feedback score is (\d+)',html)
    feedback_rate = re.findall('has ([\d\.]+%)', html)








