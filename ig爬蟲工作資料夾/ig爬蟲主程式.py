import requests
from bs4 import BeautifulSoup
import os
import time
import random
from selenium import webdriver
import openpyxl
tStart = time.time()#計時開始
#keyword = input("輸入想搜尋的：")
keyword = "桃園景點"
url = ("https://www.instagram.com/explore/tags/"+keyword)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
     'cookie': 'mid=W4VyZwALAAHeINz8GOIBiG_jFK5l; mcd=3; csrftoken=KFLY0ovWwChYoayK3OBZLvSuD1MUL04e; ds_user_id=8492674110; sessionid=IGSCee8a4ca969a6825088e207468e4cd6a8ca3941c48d10d4ac59713f257114e74b%3Acwt7nSRdUWOh00B4kIEo4ZVb4ddaZDgs%3A%7B%22_auth_user_id%22%3A8492674110%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_platform%22%3A4%2C%22_token_ver%22%3A2%2C%22_token%22%3A%228492674110%3Avsy7NZ3ZPcKWXfPz356F6eXuSUYAePW8%3Ae8135a385c423477f4cc8642107dec4ecf3211270bb63eec0a99da5b47d7a5b7%22%2C%22last_refreshed%22%3A1535472763.3352122307%7D; csrftoken=KFLY0ovWwChYoayK3OBZLvSuD1MUL04e; rur=FRC; urlgen="{\"103.102.7.202\": 57695}:1furLR:EZ6OcQaIegf5GSdIydkTdaml6QU"'
}
#遊覽器模擬登入(暫時用不到)
'''driver = webdriver.Chrome('D:/python/chromedriver.exe')
driver.get('https://www.instagram.com/accounts/login/')
time.sleep(3)
search_elem = driver.find_element_by_xpath('//input[@aria-label="電話號碼、用戶名稱或電子郵件"]')
search_elem.send_keys('wed_workday')
search_elem = driver.find_element_by_xpath('//input[@aria-label="密碼"]')
search_elem.send_keys('hope0208')
submit_elem = driver.find_element_by_xpath('//button[@class="sqdOP  L3NKy   y3zKF     "]')
submit_elem.click()
cookie = driver.get_cookies()'''


def get_urls(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('请求错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        return None


html = get_urls(url)


import json
from pyquery import PyQuery as pq

urls = []
shortcodes =[]
doc = pq(html)
items = doc('script[type="text/javascript"]').items()
#輸出結果<generator object PyQuery.items at 0x0000020B2F63CCF0>

p = 0
x = 0
for item in items:
    x = +1
    if item.text().strip().startswith('window._sharedData'):
        js_data = json.loads(item.text()[21:-1], encoding='utf-8')
        edges = js_data["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
        #抓取最新文章
        for edge in edges:
            url = edge['node']['display_url'] #抓出圖片url
            shortcode = edge['node']['shortcode'] #抓出新文章編碼
            p =+1

            urls.append(url)
            shortcodes.append(shortcode)

address_ids = []
p=0
for new_shortcode in shortcodes:
    new_url = ('https://www.instagram.com/p/'+new_shortcode)
    new_html = get_urls(new_url)
    doc = pq(new_html)
    item = doc('script[type="text/javascript"]').items()
    for items in item:
        if items.text().strip().startswith('window._sharedData'):
            js_data = json.loads(items.text()[21:-1], encoding='utf-8')
            edges = js_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]['location']#['id']
            if edges == None:
                edges = "/"
            else:
                edges = edges['id']
            address_ids.append(edges)

yes_id = []
for nonone in address_ids:
    if nonone =="/":
        continue
    yes_id.append(nonone)
time.sleep(2)
print(yes_id)
p=0
x=0
y=0
names =[]
for run_id in yes_id:
    url = ('https://www.instagram.com/explore/locations/'+run_id)
    location = get_urls(url)
    docx = pq(location)
    location = docx('script[type="text/javascript"]').items()
    p = p+1
    for locations in location :
        if locations.text().strip().startswith('window._sharedData'):
            js_data = json.loads(locations.text()[21:-1], encoding='utf-8')
            name = js_data["entry_data"]["LocationsPage"][0]["graphql"]["location"]["name"]
            names.append(name)
            y=y+1
        x = x+1
print("p="+str(p))
print("x="+str(x))
print("y="+str(y))
print(names)
q=0
#寫入excel
wb =openpyxl.Workbook()
sheet = wb["Sheet"]
sheet["A1"] = "數量"
sheet["B1"] = "地標"
x = 2
w = 0
for i in names:
    w=w+1
    sheet["A"+str(x)] = w
    sheet["B"+str(x)] = i
    x += 1

wb.save("測試寫數據.xlsx")



'''
for run_id in yes_id:
    url = ('https://www.instagram.com/explore/locations/'+run_id)
    location = get_urls(url)
print(location)'''
tEnd = time.time()#計時結束
print("It cost %f sec" % (tEnd - tStart))#會自動做近位
print('***')
input("結束")