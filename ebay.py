# coding: utf-8


import urllib
import re
from StringIO import StringIO
import gzip
import logging
from bs4 import BeautifulSoup as bs
import math
import time


logging.basicConfig(level=logging.INFO)


def db_update():
    pass  # todo 上传数据


def gethtml(url):
    logging.info(u'正在读取网页...')
    p = urllib.urlopen(url, proxies={'http': 'http://192.168.11.49:3128'})
    html = p.read()
    logging.info(u'网页读取完成。')
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


def int_item(storename):
    list_url = 'http://www.ebay.com/sch/m.html?_nkw=&_armrs=1&_from=&_ssn='+storename
    html = gethtml(list_url)
    sp = bs(html)
    span = sp.find('span', {'class': 'rcnt'})
    if span:
        tmp = span.text
        item_cnt = int(tmp.replace(',', ''))
    return item_cnt


def list_store(keyword):
    """
    :param keyword: 关键词
    :return: 返回匹配指定关键词的店铺列表
    """
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


def list_item_bypage(storename, page_ind, ipg=200):
    # 抓取指定页的listing
    date = time.strftime('%Y-%m-%d')
    itemlist = []
    kw = {}
    store_list_url = ('http://www.ebay.com/sch/m.html?_nkw=&_armrs=1&_from=&_ssn=%s&_pgn=%d' \
            + '&_ipg=%d&_skc=%d&rt=nc&_sop=10') % (storename, page_ind, ipg, ipg*(page_ind-1))
    html = gethtml(store_list_url)
    sp = bs(html)
    li = sp.findChildren('li',id=re.compile('item'))
    for i in li:
        kw['storename'] = storename
        kw['date'] = date
        kw['img'] = i.find('img').get('src')
        kw['listingid'] = i.get('listingid')
        kw['url'] = i.find('a').get('href')
        kw['title'] = i.find('h3').text
        sold = re.findall('(\d+) sold', i.text)
        if sold:
            kw['sold'] = sold[0]
        else:
            kw['sold'] = ''
        kw['ourl'] = store_list_url
        is_bids = re.findall('bids', i.text)
        if is_bids:
            kw['isBids'] = 1
        else:
            kw['isBids'] = 0
        kw['category'] = ''
        kw['creatingDate'] = ''
        itemlist.append(kw)
    return itemlist


def list_item(storename):
    ipg = 200
    itemlist = []
    item_cnt = int_item(storename)
    page_cnt = int(math.ceil(1.0*item_cnt/ipg))
    for i in range(1, page_cnt+1):
        logging.info(u'  正在出来第'+str(i)+u'个目录页...')
        tmp_list = list_item_bypage(storename, i)
        itemlist += tmp_list
    return itemlist


def item_price(x, inputtype='itemID'):
    if inputtype == 'itemID':
        html = gethtml('http://www.ebay.com/itm/'+x)
    else:
        html = x
    s = re.findall(r'itemprop="price"  style="">(.*?)</span>', html)  # 匹配价格
    if s:
        return s[0]


def item_sold(x, inputtype='itemID'):
    """
    :param x: itemID 或者 网页源码
    :param inputtype: 指定x是itemID还是网页源码
    :return: 解析出的销售量
    """
    if inputtype == 'itemID':
        html = gethtml('http://www.ebay.com/itm/'+x)
    else:
        html = x
    s = re.findall(r'(\d+) sold', html)

    if s:
        return int(s[0])
    else:
        return 0


def item_location(html):
    """
    :return: item的发货地址
    """
    s = re.findall(r'<div class="iti-eu-bld-gry ">(.*?)</div>', html)
    if s:
        return s[0]


def store_feedback(storename):
    _store_url = 'http://stores.ebay.com/%s' % storename
    raw = gethtml(_store_url)
    try:
        html = uncompress(raw)
    except IOError:
        html = raw
    finally:
        logging.info(u'网页下载完成。')

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















