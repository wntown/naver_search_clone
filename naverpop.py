import requests
import time
import sys
import json
from urllib import parse
from bs4 import BeautifulSoup
from threading import Thread

mod = sys.modules[__name__]

global totalNewsData
totalNewsData = {}


def getRankList():
    rankList = []
    url = "https://www.naver.com"
    req = requests.get(url)
    soup = BeautifulSoup(req.text,"html.parser")

    for item in soup.select(".ah_roll_area .ah_k"):
        rankList.append(item.text)
    
    return rankList

def append_list(idx,keyword):
    global totalNewsData
    tempList = []

    search_url = "https://search.naver.com/search.naver?where=nexearch&sm=tab_jum&query="+ parse.quote(keyword)
    req = requests.get(search_url)
    soup = BeautifulSoup(req.text,"html.parser")

    for item2,item3 in zip(soup.select("._prs_nws_all dl"),soup.select("._prs_nws_all .thumb img")):
        news_thumb = item3.get("src")
        news_title = item2.select("a")[0].get("title")
        news_des = item2.select("dd")[1].text
        news_link = item2.select("a")[0].get("href")
        
        news_data = {
            "news_thumb" : news_thumb,
            "news_title" : news_title,
            "news_des": news_des,
            "news_link" : news_link,
        }

        tempList.append(news_data)
    
    totalNewsData.update({idx:{"keyword":keyword,"data":tempList}})


def auto_run():
    global totalNewsData
    totalNewsData = {}
    
    rank_list = getRankList()
    # startTime = time.time() #시작한시간

    # 동적 변수 할당 #
    for idx,item in enumerate(rank_list):
        setattr(mod, "th{}".format(idx+1), Thread(target=append_list ,args=(str(idx+1),item)))
        
    # 동적 변수 할당 #

    # 동적으로 생성된 변수(쓰레드) 실행 #

    for idx,item in enumerate(rank_list):
        getattr(mod,  'th{}'.format(idx+1)).start()
        
    for idx,item in enumerate(rank_list):
        getattr(mod,  'th{}'.format(idx+1)).join()

    # 동적으로 생성된 변수(쓰레드) 실행 #

    # endTime = time.time() - startTime # 끝난시간
    # print("총",endTime,"초 소요됬습니다")
    # print(totalNewsData)
    totalNewsData = json.dumps(totalNewsData)

    f = open("new_list.json","w",encoding='utf8')
    f.write(str(totalNewsData))
    f.close()