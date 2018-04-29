import requests, json 


key = "$2a$10$4kqrutykvO.8dW6Ux5740exk/tz5cQHA5UnCaF/v12IwpYB6AhDfC"
addressURL = "https://api.jsonbin.io/b/5ae5fa237a973f4ce577de65"

def getAddresses():
    resp = requests.get(addressURL, headers={'secret-key':key})
    return resp.json()['pages']

def getCards(addr):
    addresses = getAddresses()
    resp = requests.get(addresses[addr], headers={'secret-key':key})
    return resp.json()

print(getAddresses())