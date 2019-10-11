import os
import bs4
from bs4 import BeautifulSoup
import requests

r = requests.get('https://m.dxsbb.com/news/5463.html')
r.encoding = r.apparent_encoding
demo = r.text



def gets(ulist,demo):
    soup = BeautifulSoup(demo, 'html.parser')
    t = soup.find_all('tbody')
    for tr in t[1].children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            ulist.append([tds[0].string, tds[1].string, tds[2].string, tds[3].string, tds[4].string])


def prints(ulist, num):
    #print('{:^10}\t{:^10}\t{:^10}\t{:^10}\t{:^10}'.format('排名','大学名称','分数','星级','层次'))
    for i in range(0, num):
        u = ulist[i]
        print(u[0]+'    '+u[1]+'    '+u[2]+'    '+u[3]+'    '+u[4])



def main():
    uinfo=[]
    gets(uinfo,demo)
    prints(uinfo,20)

main()