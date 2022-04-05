from calendar import EPOCH, month
from posixpath import split
from unicodedata import category, name
import requests
import json
from datetime import datetime



protocol_url = "https://api.llama.fi/chain/"

response = requests.get(protocol_url + "Gnosis")
datas = response.json()
print(datas)