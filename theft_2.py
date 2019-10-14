import json
import requests
import sys
import time

url = "https://sf-dkt-gates-store-api-s.herokuapp.com/alerts/theft"

payload = "{\n    \"api_key\": \"u7dcdj52df45y7a0avcba8idu56g17d4\",\n    \"id_gate\": 2\n}"

headers = {
    'Content-Type': "application/json",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "sf-dkt-gates-store-api-s.herokuapp.com",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "72",
    'Referer': "https://sf-dkt-gates-store-api-s.herokuapp.com/alerts/theft",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }


def get_pic():
    '''
    returning a list, containing a sorted data to display a restroom data
    '''
    response = requests.request("GET", url, data=payload, headers=headers)
    obj = response.json()
    info_list = []
    data = obj["data"]["results_data"]
    for i in data:
        dic = {}
        name = i["product_name"]
        pic = i["product_picture"]
        brand = i["product_brand"]
        size = i["product_size"]
        time = i["created"]
        dic.update({"name": name})
        dic.update({"pic": pic})
        dic.update({"brand": brand})
        dic.update({"size": size})
        dic.update({"time": time})
        info_list.append(dic)
    return(info_list)
