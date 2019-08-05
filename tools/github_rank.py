import requests
import time
import os
import json
import sqlite3
import sys
import re
import codecs
from itertools import islice
from bs4 import BeautifulSoup
import execjs
import hashlib   

language='Objective-C'
stars='800'
page_start=100
page_end=100
l_a_start=0

url = 'https://github.com/search?utf8=%E2%9C%93&q=language%3A'+language + '+stars%3A%3E'+stars+'&type='


db_base_path = './'
file_dir = './'
file_parent_dir = '../'

base_url ='https://github.com'

execute_str="CREATE TABLE rankDetail(\
ID  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
name  TEXT UNIQUE,\
link  TEXT,\
des  TEXT,\
star  TEXT);"

#创建DB
def creat_database(path):
    conn_b = sqlite3.connect(path)
    print("Opened database successfully")
    c1 = conn_b.cursor()
    try:
        c1.execute(execute_str)
        conn_b.commit()
        conn_b.close()
    except sqlite3.OperationalError:
        print(file_dir)
        conn_b.close()


def insert_data(data):
    # print(data)
    conn1 = sqlite3.connect(path_b)
    c1 = conn1.cursor()
    name=data["name"]
    link=data["link"]
    star=data["star"]
    des=data["des"]

    strsql = "INSERT INTO rankDetail (name,link,star,des) VALUES ('" + name + "','" + link + "','"+star + "','"+des +"')"
    try:
        c1.execute(strsql)
        conn1.commit()
        conn1.close()
    except sqlite3.IntegrityError or sqlite3.OperationalError:
        conn1.close()

def par_html(html):
    soup_b=BeautifulSoup(html,'lxml')
    p=l_a_start
    a1_list=soup_b.find_all("li", class_="repo-list-item d-flex flex-column flex-md-row flex-justify-start py-4 public source")

    for a0_text in a1_list[l_a_start:]:
        p=p+1
        print(str(p))
        aa=a0_text.find("div", class_="col-12 col-md-8 pr-md-3")
        str_b=a0_text.find("div", class_="pl-2 pl-md-0 text-right flex-auto min-width-0")
        star_n=str_b.find("a",class_="muted-link")
        star=star_n.text
        name_h3=aa.find("h3")
        a_link=name_h3.find("a", class_="v-align-middle")
        link=base_url+a_link["href"]

        name_author=a_link.text
        name= name_author.split('/')[-1]
        if name:
            print(name)
        else:
            name=imageUrl.split('/')[-2]

        des_n=aa.find("p", class_="col-12 col-md-9 d-inline-block text-gray mb-2 pr-4")
        des=''
        if des_n:
            des=des_n.text

        name=name.strip()
        name.replace('\n','')
        link=link.strip()
        link.replace('\n','')
        star=star.strip()
        star.replace('\n','')
        des=des.strip()
        des=des.replace('\n','')
        des=des.replace("'", "")

        data_t={
        "name":name,
        "link":link,
        "star":star,
        "des":des,
        }
        insert_data(data_t)

def handle_request(h_url,p):
    url=h_url + '&p=' + str(p)
    response_b =requests.get(url)
    response_b.encoding="utf-8"
    html_doc_b = response_b.text
    return html_doc_b


def get_db_data():
    conn1 = sqlite3.connect(path_b)
    c1 = conn1.cursor()
    strsql = "select ID,name,link,star,des from rankDetail"
    list=[]
    try:
        c1.execute(strsql)
        conn1.commit()
        for row in c1:
            idint = row[0]
            name = row[1]
            link = row[2]
            star = row[3]
            des = row[4]
            dic={
                "idint":idint,
                "name":name,
                "link":link,
                "star":star,
                "des":des,
            }
            list.append(dic)

        conn1.close()
    except sqlite3.IntegrityError or sqlite3.OperationalError:
        conn1.close()

    return list


def make_mark_down():
    list = get_db_data()
    str_f=language + 'Stars 1000以内排名整理<br/>|ID|Name|Describe|Stars<br/>|---|---|---|---|<br/>'
    for dic in list[0:]:
        idint = dic["idint"]
        name = dic["name"]
        link = dic["link"]
        star = dic["star"]
        des = dic["des"]
        str_f=str_f+'|'+str(idint)+'|['+name+']('+link+')|'+des+'|'+star+'|<br/>'
    return str_f

def write_to_file(str_f):
    readme_dir =file_parent_dir + language + '/' + 'README.md'
    with open(readme_dir, "w", encoding='utf-8') as f:
        f.write(str(str_f))
        f.close()


if __name__ == "__main__":
    path_b=db_base_path+"rank-"+language+'.db'
    creat_database(path_b)
    for p_n in range(page_start,page_end):
        html_doc_b = handle_request(url,p_n)
        par_html(html_doc_b)
        time.sleep(2)

    str_mark = make_mark_down()
    write_to_file(str_mark)

