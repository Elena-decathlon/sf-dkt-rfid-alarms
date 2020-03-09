import app.decoder
import json
import os
import requests
import sys
import time

from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

POTRERO_API_KEY = os.getenv("POTRERO_API_KEY")
EMERYVILLE_API_KEY = os.getenv("EMERYVILLE_API_KEY")

url_potrero = "https://sf-dkt-gates-store-api-2214.herokuapp.com/alerts/theft"

payload_entrance_potrero = {
    "api_key": POTRERO_API_KEY, 
    "id_gate": 1
    }

payload_restroom_potrero = {
    "api_key": POTRERO_API_KEY,
    "id_gate": 2
    }

url_emrvl = "https://sf-dkt-gates-store-api-2213.herokuapp.com/alerts/theft"

payload_entrance_emrvl = {
    "api_key": EMERYVILLE_API_KEY,
    "id_gate": 1
    }

payload_restroom_emrvl = {
    "api_key": EMERYVILLE_API_KEY,
    "id_gate": 2
    }


headers = {
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    }


def get_pic(store, gates):
    '''
    returning a list, containing sorted data to display an entrance/exit detected alarms
    '''
    if store == "potrero" and gates == "entrance":
        response = requests.request("GET", url=url_potrero, json = payload_entrance_potrero, headers=headers)
    elif store == "potrero" and gates == "restroom":
        response = requests.request("GET", url=url_potrero, json = payload_restroom_potrero, headers=headers)
    elif store == "emeryville" and gates == "entrance":
        response = requests.request("GET", url=url_emrvl, json = payload_entrance_emrvl, headers=headers)
    elif store == "emeryville" and gates == "restroom":
        response = requests.request("GET", url=url_emrvl, json = payload_restroom_emrvl, headers=headers)
    obj = response.json()
    gates = "entrance"
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
                pic = "https" + pic_check[4:]
            else:                                                          #handle the case, when product picture missing
                pic = "../static/images/not_found.png"
            brand = i["product_brand"]
            size = i["product_size"]
        t_str = i["created"]
        t_str_rep = t_str.replace(" GMT", "")                             #deleting the timezone name form the string
        t_time = datetime.strptime(t_str_rep, '%a, %d %b %Y %H:%M:%S')
        time = t_time - timedelta(hours=8, minutes = 0)                   #converting time to a PTZ    #converting str to datetime object
        epc = i["product_epc"]
        ean13 = app.decoder.EPC_decoder_EAN13(epc)
        serial = app.decoder.EPC_decoder_serial(epc)
        dic.update({"name": name, "pic": pic, "brand": brand, "size": size, "time": time, "epc": epc, "ean13": ean13, "serial": serial})
        info_list.append(dic)
#        print(info_list)
    return(info_list)

#get_pic()
