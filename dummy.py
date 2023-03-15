from calendar import EPOCH, month
from posixpath import split
from unicodedata import category, name
import requests
import asyncio
import aiohttp
import json
from datetime import datetime
import math


PROTOCOLS_URL = "https://api.llama.fi/protocols"
PROTOCOL_URL = "https://api.llama.fi/protocol/"

def get_eth_protocols():

    response = requests.get(PROTOCOLS_URL)
    datas = response.json()

    eth_protocols = []

    for data in datas:
        if "Ethereum" in data["chains"] and data["category"] != "CEX":
            ethProtocol = {
                "name": data["name"],
                "category": data["category"]
            }
            eth_protocols.append(ethProtocol)

    return eth_protocols


async def iterate_protocols(protocols):
    protocol_datas =  []
    tasks = []
    async with aiohttp.ClientSession() as session:
        for protocol in protocols[1:250]:
            if " " in protocol["name"]:
                split_name = protocol["name"].split(" ")
                join_name = "-".join([split_name[0], split_name[1]])
                name = join_name.lower()
            else:
                name = protocol["name"]

            if name == "xdai-stake" or name == "the-tokenized" or name == "perpetual-protocol" or name == "gnosis-protocol":
                continue

            try:
                task = asyncio.create_task(async_fetch_protocol_history(session, name, protocol))
                tasks.append(task)
            except Exception as err:
                print(f"async error {err}")
            # protocol_data = fetch_protocol_history(name, protocol)
            # protocol_datas.append(protocol_data)


        protocol_datas = await asyncio.gather(*tasks)
        
    return protocol_datas
    
def fetch_protocol_history(protocol_name, protocol):
    protocol_response = requests.get(PROTOCOL_URL+ protocol_name)
    temp_data = protocol_response.json()
    protocol_data = []
    try:
        object = {
            "name": protocol_name,
            "category": protocol["category"],
            "ethTvlHistory": temp_data["chainTvls"]["Ethereum"]["tvl"]
        }
        for hash in object["ethTvlHistory"]:
            epochtime = hash["date"]
            datetim = datetime.fromtimestamp(epochtime)
            date = datetim.strftime("%Y-%m-%d")
            
            if date[8] == '0' and date[9] == '1' and date[2] == "2":
                HashyMcHasherson = {
                    "date": date,
                    "name": protocol["name"],
                    "category": protocol["category"],
                    "tvlUSD": math.floor(hash["totalLiquidityUSD"])
                }
                protocol_data.append(HashyMcHasherson)
    except:
        print("------")
        print(protocol_name)
        # print(temp_data)
        print("-------")

    return {protocol_name: protocol_data}

async def async_fetch_protocol_history(session, protocol_name, protocol):

    async with session.get(PROTOCOL_URL + protocol_name) as protocol_response:
        temp_data = await protocol_response.json()
        protocol_data = []
        try:
            object = {
                "name": protocol_name,
                "category": protocol["category"],
                "ethTvlHistory": temp_data["chainTvls"]["Ethereum"]["tvl"]
            }
            for hash in object["ethTvlHistory"]:
                epochtime = hash["date"]
                datetim = datetime.fromtimestamp(epochtime)
                date = datetim.strftime("%Y-%m-%d")
                
                if date[8] == '0' and date[9] == '1' and date[2] == "2":
                    HashyMcHasherson = {
                        "date": date,
                        "name": protocol["name"],
                        "category": protocol["category"],
                        "tvlUSD": math.floor(hash["totalLiquidityUSD"])
                    }
                    protocol_data.append(HashyMcHasherson)
        except:
            print("------")
            print(protocol_name)
            # print(temp_data)
            print("-------")

    return {protocol_name: protocol_data}

eth_protocols = get_eth_protocols()
protocol_datas = asyncio.run(iterate_protocols(eth_protocols))

with open('data2.json', 'w') as f:
    json.dump(protocol_datas, f, indent=4, default=str)

