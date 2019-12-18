
from datetime import datetime, timedelta
import json
import requests
import sys
import time

import app.decoder

url = "https://sf-dkt-gates-store-api-s.herokuapp.com/alerts/theft"

payload = "{\n    \"api_key\": \"u7dcdj52df45y7a0avcba8idu56g17d4\",\n    \"id_gate\": 2\n}"

headers = {
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    }


def get_pic():
    '''
    returning a list, containing a sorted data to display a restroom detected alarms
    '''
    response = requests.request("GET", url, data=payload, headers=headers)
    obj = response.json()
    info_list = []
    data = obj["data"]["results_data"]
    ln = len(data)
    for i in data:
        dic = {}
        if i["product_name"] == None:
            name = "Picture is not found"
            brand = ""
            size = ""
            pic = "../static/images/not_found.png"
        else:
            name = i["product_name"]
            pic_check = str(i["product_picture"])
            if pic_check[0:4] == "http":
                pic = "https" + pic_check[4:]                               #hardcoded to change http to https manually, needs to be fixed
            brand = i["product_brand"]
            size = i["product_size"]
        t_str = i["created"]
        t_str_rep = t_str.replace(" GMT", "")                             #deleting the timezone name form the string
        t_time = datetime.strptime(t_str_rep, '%a, %d %b %Y %H:%M:%S')    #converting str to datetime object
        time = t_time - timedelta(hours=8, minutes = 0)                   #converting time to a PTZ
        epc = i["product_epc"]
        ean13 = app.decoder.EPC_decoder_EAN13(epc)
        serial = app.decoder.EPC_decoder_serial(epc)
        dic.update({"name": name, "pic": pic, "brand": brand, "size": size, "time": time, "epc": epc, "ean13": ean13, "serial": serial})
        info_list.append(dic)
    return(info_list)

get_pic()
