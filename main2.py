#!/usr/bin/env python
# coding: utf-8

# In[9]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import pandas as pd
import time
import re

RESULT_PATH = '/Users/carly/Development/crawling3/results'
f = open("/Users/carly/Development/crawling3/results/text.txt", 'w', encoding='utf-8')
# start = time.time()
origin = 'https://novel.naver.com'
ExcelData = []


# In[3]:


# f = open("/Users/carly/Development/crawling3/results/text.txt", 'r')
# text = f.read()


# In[25]:


page = 1
# 완결탭에 있는 소설 가져옴.
url = "https://novel.naver.com/webnovel/finish.nhn?page="+str(page)
req = requests.get(url)
cont = req.content
soup = BeautifulSoup(cont, 'html.parser')
l = soup.select(".list_item")
# l[0]['href'] # 링크 가져오기.
origin = 'https://novel.naver.com'
url_novel = origin + l[0]['href']
req_novel = requests.get(url_novel)
cont_novel = req_novel.content
soup_novel = BeautifulSoup(cont_novel,'html.parser')
# soup_novel
l = soup_novel.select(".list_item")
# l[0]['href'] # 소설 1화 가져오기
url_detail = origin + l[0]['href']
url_detail
# num_epi = soup_novel.select('.total')[0].text
# num_epi = int(num_epi[1:len(num_epi)-1])
# num_epi
_req = requests.get(url_detail)
_cont = _req.content
_soup = BeautifulSoup(_cont,'html.parser')
title = _soup.select('.tit_book')[0].text
epi_title = _soup.select('#topVolumeList')[0].text
epi_title = epi_title[:epi_title.find('회차 더보기')]
text = _soup.select(".detail_view_content")[0].text


# In[109]:


rtn = re.sub('\r+','',text)
rtn = re.sub('\n{2,}','',rtn)
rtn = re.sub('…+','.',rtn)
rtn = re.sub('["“”‘’()]+','',rtn)
rtn = re.sub('\.[\.,!?]','.',rtn)
rtn = re.sub('\*+',' ',rtn)
rtn = re.sub('\s{2,}',' ',rtn)


# In[110]:


print(rtn)


# In[13]:


print(text)


# In[60]:


rtn


# In[ ]:




