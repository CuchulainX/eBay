# coding: utf-8


import urllib
import re


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

def parse_store(html):
    storename = re.findall(r'<span content="(.*?)" itemprop="name"', html, re.DOTALL)
    storeurl = re.findall(r'href="(http://stores.ebay.com/.*?) itemprop="url"', html, re.DOTALL)
    r = []
    for i in range(0,len(storename)):
        tmp = {}
        tmp['storename'] = storename[i]
        tmp['storeurl'] = storeurl[i]
        r.append(tmp)
    return r



url = 'http://www.ebay.com/itm/281589160700'
html = gethtml(url)
s = parse_sold(html)

url = 'http://stores.ebay.com/_si.html?tokenstring=VFrYUAwAAAA%3D&_sofindtype=7&_nkw=hand+dryer&rd=ON'
store = parse_store(url)





