
# coding: utf-8

# In[6]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import matplotlib.pyplot as plt
from PIL import Image
import lxml.html
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import sqlite3
import tqdm

get_ipython().magic('matplotlib inline')


# ## phantomJS
# ### desired capabilities
# - UA指定

# In[7]:


def show_img(path):
    img = Image.open(path)
    plt.figure(figsize=(20,10))
    plt.imshow(img)
#     plt.cla('all')


# ## クローリング&スクレイピング

# In[63]:


import pandas as pd
for i in pd.date_range('20170401','20170816'):
    print(i.strftime('%Y-%m-%d'))


# In[ ]:


import pandas as pd
import urllib.request
import sqlite3

des_cap = dict(DesiredCapabilities.PHANTOMJS)
des_cap['phantomjs.page.settings.userAgent'] = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/28.0.1500.52 Safari/537.36'
)
 
driver = webdriver.PhantomJS(desired_capabilities=des_cap)

# 画像ファイル名とview数の対応づけ
cnt = 0

conn = sqlite3.connect("naver_views.db")
cur = conn.cursor()
cur.execute("""create table if not exists views (id int, view int)""")

for i in pd.date_range('20170401','20170816'):
    date_str = i.strftime('%Y-%m-%d')
    main_url = 'http://naver-matome.appspot.com/?category=&type=view&filterDate={}'.format(date_str)
    urls = []
    views = []
    
    # ページオープン&パース
    driver.get(main_url)
    data = driver.page_source
    bs = BeautifulSoup(data,"lxml")

    # 画像URL&view数取得
    for i in bs.find_all(attrs={"class":"article"}):
        urls.append(i.find("img")['src'])
        views.append(i.find("span",attrs={"style":"margin:10px 5px 10px 10px;color:#FF8C00"}).text)
    
    views = [int(v.split()[1].strip()) for v in views]
    
    # 画像ファイルのURLを開く
    for i,url in enumerate(urls):
        try:
            request = urllib.request.urlopen(url)
        except:
            continue
    
        # 画像保存
        f = open('2ch/{}.jpg'.format(cnt), "wb")
        f.write(request.read())

        # ファイルを閉じる
        f.close()
        
        # 保存した画像と同じIDでview数保存
        cur.execute("""insert into views values ({0},{1})""".format(cnt, views[i]))
    
        cnt += 1
    
conn.close()
driver.quit()


# In[37]:


main_url = 'http://naver-matome.appspot.com/?category=&type=view&filterDate=2017-08-14'
 
des_cap = dict(DesiredCapabilities.PHANTOMJS)
des_cap['phantomjs.page.settings.userAgent'] = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/28.0.1500.52 Safari/537.36'
)
 
driver = webdriver.PhantomJS(desired_capabilities=des_cap)

views = []

# トップページ開く
driver.get(main_url)
# driver.save_screenshot('./2ch/main.png')

data = driver.page_source
bs = BeautifulSoup(data,"lxml")
for i in bs.find_all(attrs={"class":"article"}):
    views.append(i.find("span",attrs={"style":"margin:10px 5px 10px 10px;color:#FF8C00"}).text)
    
driver.quit()


# In[38]:


views = [int(v.split()[1].strip()) for v in views]
for v in views:
    print(v)


# In[14]:


len(urls)


# In[19]:


# 全画像取得

import urllib.request

# 画像ファイルのURLを開く
# （urlに画像ファイルのURLを指定）
for cnt,url in enumerate(urls):
    request = urllib.request.urlopen(url)

    # ファイルをバイナリモードで開き、URLの内容を書き込み
    # （file_nameに保存時のファイル名を指定）
    f = open('2ch/{}.jpg'.format(cnt), "wb")
    f.write(request.read())

    # ファイルを閉じる
    f.close()


# In[30]:


from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import glob
get_ipython().magic('matplotlib inline')

for i in glob.glob("2ch/*"):
    img = Image.open(i)
    img = img.resize((100,100))
    plt.figure()
    plt.imshow(img)


# In[39]:


import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator


# In[59]:


x_train = np.empty((0,100,100,3), float)
y_train = []

for i in glob.glob("2ch/*"):
    img = Image.open(i)
    img = img.resize((100,100))
    img_array = np.array(img, 'f')
    img_array /= 255.
    if len(img_array.shape) == 2:
        print(i);continue
        
    y_train.append(views[int(i.split(".")[0].split('/')[-1])])
        
#     x_train.append(img_array)

    x_train = np.append(x_train,img_array.reshape(-1,100,100,3),axis=0)
    
print(x_train.shape)
# x_train = np.array(x_train)
# print(x_train.shape)

