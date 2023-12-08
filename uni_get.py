# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json

f = open('data.json', 'w',errors='ignore')

base_json_string = '{"range": "スポットデータ","majorDimension": "ROWS","values": []}'
base_json_dict = json.loads(base_json_string)

values = []
value = ["タイムスタンプ","カテゴリ","画像","緯度","経度","スポット名","紹介文","Instagram","Twitter","公式サイト","Facebook"]
values.append(value)

url = 'https://location.am-all.net/alm/location?gm=109&ct=1000&at='

for i in range(47):
    print(i)
    print(url+str(i))
    res = requests.get(url+str(i))
    soup = BeautifulSoup(res.text, "html.parser")
    find = soup.find_all("li")
    for tempo in find:
        name = tempo.find(class_="store_name").text
        address = tempo.find(class_="store_address").text
        pattern = '''(...??[都道府県])'''
        todofuken = re.match(pattern , address)[0]
        address2 = address.replace(todofuken,'')
        location = str(tempo.find(class_="store_map")).replace('\n', '')
        detail = re.search('sid=\d+',str(tempo.find(class_="store_bt")).replace('\n', ''))[0]
        detailurl = "https://location.am-all.net/alm/shop?gm=109&astep=0&" + detail
        
        pattern = '@.*&'
        result = re.findall(pattern, location)[0].replace('@','').replace('&','')
        ido = result.split(',')[0]
        keido = result.split(',')[1]

        value = ["",todofuken,"",ido,keido,name,address2,"","",detailurl,""]
        values.append(value)

        
base_json_dict["values"] = values
final_json_string = json.dumps(base_json_dict, indent=4, ensure_ascii=False)
print(final_json_string)
f.writelines(final_json_string)
f.close()