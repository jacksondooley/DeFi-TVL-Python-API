from calendar import EPOCH, month
from posixpath import split
from unicodedata import name
import requests
import json
from datetime import datetime


protocols_url = "https://api.llama.fi/protocols"

protocol_url = "https://api.llama.fi/protocol/"

response = requests.get(protocols_url)


datas = response.json()

ethProtocols = []

for data in datas:
    if "Ethereum" in data["chains"]:
        ethProtocol = {
            "name": data["name"]
        }
        ethProtocols.append(ethProtocol)


protocol_datas =  []

i = 0
while i < 100:
    if " " in ethProtocols[i]["name"]:
        split_name = ethProtocols[i]["name"].split(" ")
        join_name = "-".join([split_name[0], split_name[1]])
        name = join_name.lower()
    else:
        name = ethProtocols[i]["name"]

    print(name)
    if name == "xdai-stake" or name == "the-tokenized":
        i += 1
        continue

    protocol_response = requests.get(protocol_url + name)
    temp_data = protocol_response.json()
    object = {
        "name": name,
        "ethTvlHistory": temp_data["chainTvls"]["Ethereum"]["tvl"]
    }

    FirstOfMonth = []
    for hash in object["ethTvlHistory"]:
        epochtime = hash["date"]
        datetime = datetime.fromtimestamp(epochtime)
        date = datetime.strftime("%d-%b-%Y")
        
        if date[0] == '0' and date[1] == '1':
            HashyMcHasherson = {
                "date": datetime,
                "tvlUSD": hash["totalLiquidityUSD"]
            }
            FirstOfMonth.append(HashyMcHasherson)

    object["ethTvlHistory"] = FirstOfMonth
        

    protocol_datas.append(object)
    # breaks
    i += 1

# for protocol in protocol_datas:
#     for hash in protocol["ethTvlHistory"]:
#         epochtime = hash["date"]
#         datetime = datetime.fromtimestamp(epochtime)
#         protocol_datas[protocol][hash]["date"] = datetime

with open('data.json', 'w') as f:
    json.dump(protocol_datas, f, indent=4, default=str)

