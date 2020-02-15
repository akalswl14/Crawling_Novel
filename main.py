#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import pandas as pd
import time
import re

RESULT_PATH = '/Users/carly/Development/crawling3/results'
f = open("/Users/carly/Development/crawling3/results/_text.txt", 'w', encoding='utf-8')
start = time.time()
origin = 'https://novel.naver.com'
ExcelData = []


# In[2]:


# page = 1
# # 완결탭에 있는 소설 가져옴.
# url = "https://novel.naver.com/webnovel/finish.nhn?page="+str(page)
# req = requests.get(url)
# cont = req.content
# soup = BeautifulSoup(cont, 'html.parser')
# l = soup.select(".list_item")
# # l[0]['href'] # 링크 가져오기.
# origin = 'https://novel.naver.com'
# url_novel = origin + l[0]['href']
# req_novel = requests.get(url_novel)
# cont_novel = req_novel.content
# soup_novel = BeautifulSoup(cont_novel,'html.parser')
# # soup_novel
# l = soup_novel.select(".list_item")
# # l[0]['href'] # 소설 1화 가져오기
# url_detail = origin + l[0]['href']
# # url_detail
# # num_epi = soup_novel.select('.total')[0].text
# # num_epi = int(num_epi[1:len(num_epi)-1])
# # num_epi
# # _req = requests.get(url_detail)
# # _cont = _req.content
# # _soup = BeautifulSoup(_cont,'html.parser')
# # title = _soup.select('.tit_book')[0].text
# # epi_title = _soup.select('#topVolumeList')[0].text
# # epi_title = epi_title[:epi_title.find('회차 더보기')]
# # _soup.select(".detail_view_content")[0].text
# l[-1]


# In[3]:


def find_novel():
    page = 1
    text =''
    while page < 25 :
        print(page)
        # 완결탭에 있는 소설 가져옴.
        url = "https://novel.naver.com/webnovel/finish.nhn?page="+str(page)
        req = requests.get(url)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')
        li_novel = soup.select(".list_item")
        for novel in li_novel:
            novel = origin + novel['href']
            text += get_novel(novel)
            #리스트 합칠거라서 += 붙일수 있으면 append
        page += 1
    #특수문자 빼는 부분 여기에 넣기
    text = re.sub('\r+','',text)
    text = re.sub('\n{2,}','',text)
    text = re.sub('…+','.',text)
    text = re.sub('["“”‘’()]+','',text)
    text = re.sub('\.[\.,!?]','.',text)
    text = re.sub('\*+',' ',text)
    text = re.sub('\s{2,}',' ',text)
    f.write(text)
    f.close()


# In[4]:


def get_novel(novel):
    req = requests.get(novel)
    cont = req.content
    soup = BeautifulSoup(cont,'html.parser')
    epis = soup.select(".volumeComment .list_item")
    # 긁어온 부분
    page = 2
    num_epi = soup.select('.total')[0].text
    num_epi = int(num_epi[1:len(num_epi)-1])
    text = ''
    print(len(epis))
    print(num_epi)
    while(len(epis)<num_epi):
        req = requests.get(novel + '&page='+str(page))
        print(novel + '?page='+str(page))
        cont = req.content
        soup = BeautifulSoup(cont,'html.parser')
        epis += soup.select(".volumeComment .list_item")
        print(page)
        print(len(epis))
        page+=1
    for epi in epis :
        epi = origin + epi['href']
        print(epi)
        text += get_epi(epi)
    return text


# In[5]:


def get_epi(epi):
    #info은 소설명, 에피소드명이 담겨있는 리스트
    info = []
    req = requests.get(epi)
    cont = req.content
    soup = BeautifulSoup(cont,'html.parser')
    title = soup.select('.tit_book')[0].text
    epi_title = soup.select('#topVolumeList')[0].text
    epi_title = epi_title[:epi_title.find('회차 더보기')]
    info.append(title)
    info.append(epi_title)
    text = soup.select(".detail_view_content")[0].text + '\n'
    ExcelData.append(info)
    print(info)
    return text


# In[6]:


def excel_make(ExcelData):
    col = ['제목','에피소드']
    df = pd.DataFrame(ExcelData,columns=col)
    df.to_csv(RESULT_PATH+'/_Excel_Novel.csv',encoding='utf-8-sig')


# In[7]:


def main():
    find_novel()
    excel_make(ExcelData) #엑셀로 만들기


# In[8]:


main()
print("소요시간 :", time.time() - start)


# In[ ]:





# In[ ]:




