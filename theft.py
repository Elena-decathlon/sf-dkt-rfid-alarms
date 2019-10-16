import json
import requests
import sys
import time

import decoder 

url = "https://sf-dkt-gates-store-api-s.herokuapp.com/alerts/theft"

payload = "{\n    \"api_key\": \"u7dcdj52df45y7a0avcba8idu56g17d4\",\n    \"id_gate\": 1\n}"

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
    returning a list, containing a sorted data to display an entrance data
    '''
    response = requests.request("GET", url, data=payload, headers=headers)
    obj = response.json()
    info_list = []
    data = obj["data"]["results_data"]
    ln = len(data)
    for i in data:
        dic = {}
        if i["product_name"] == None:
            name = ""
            brand = ""
            size = ""
            pic = "../static/images/not_found.png"
        else:
            name = i["product_name"]
            pic = i["product_picture"]
            brand = i["product_brand"]
            size = i["product_size"]
        time = i["created"]
        epc = i["product_epc"]
        ean13 = decoder.EPC_decoder_EAN13(epc)
        serial = decoder.EPC_decoder_serial(epc)
        dic.update({"name": name, "pic": pic, "brand": brand, "size": size, "time": time, "epc": epc, "ean13": ean13, "serial": serial})
#        dic.update({"pic": pic})
#        dic.update({"brand": brand})
#        dic.update({"size": size})
#        dic.update({"time": time})
#        dic.update({"ean13": ean13})
#        dic.update({"serial": serial})
        info_list.append(dic)
    print(info_list)
    return(info_list)

get_pic()