import requests
import json
from flask import Flask
app= Flask(__name__)
cors= CORS(app)
poe_api='http://api.pathofexile.com/public-stash-tabs'
poe_items= 'https://www.pathofexile.com/api/trade/data/items'

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
#r=requests('https://www.pathofexile.com/api/trade/data/items', headers=headers)
#unique_data = {}

unique_data={}

def test():
    r=requests.get(poe_items, headers=headers)
    #print(r)
    item_results= r.json()['result']
    for types in item_results:
        for items in types['entries']:
            if 'flags' in items:
                if 'unique' in items['flags']:
                    unique_data[items['name']]=0
                    # flags.append(items['flags'])
test()

#turn key into "name" = key name
#turn into "number" = dict number

    




@app.route("/")
def compiled_data():
    # Create dictionary for compiled uniques list
    uniques=[]
    # fetch stash info from poe api

    i=0
    next_id='0'
    while i <3:
        print(next_id)
        r = requests.get('http://api.pathofexile.com/public-stash-tabs', headers=headers, params={'id': next_id})
        print(r)
        stash_data= r.json()
        stashes = stash_data['stashes']
        next_id = stash_data['next_change_id']
        for user_stash in stashes:
            for item in user_stash['items']:
                if item['name'] and item['frameType']==3:                
                    uniques.append(item['name'])
        i+=1
    for name in uniques:
        unique_data[name]+=1
        
    
    return convert_to_json(unique_data)

if __name__== "__main__":
    app.run()

def convert_to_json(dataset):
    name=dataset.keys()
    combined={'items': []}
    #return name
    for item in name:
        combined['items'].append({
            "name": item,
            "number": dataset[item] 
        })
    return json.dumps(combined)