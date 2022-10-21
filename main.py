import requests
import json

def lambda_handler(req):
  since_id = None


  # get data for bitcoin price in that fiat
  URL = 'https://min-api.cryptocompare.com/data/histoday?fsym=BTC&tsym=USD&allData=true' 
  res = requests.get(URL)
  res_json = res.json()
  data= res_json['Data']

  # Reformat Twitter's response into nice, flat tables
  cryptoData = []
  for t in data:
    # Remember the first id we encounter, which is the most recent
    if (since_id == None) :
      since_id = t["time"]

    # Add all tflLineStatus
    cryptoData.append({
      "timestamp": t["time"],
      "high": t["high"],
      "low": t["low"],
      "open": t["open"],
      "volumefrom":t["volumefrom"],
      "volumeto":t["volumeto"],
      "close":t["close"],
      "ticker": "btc"
      })


    
  # Send JSON response back to Fivetran

  if(since_id==None):
    since_id = req.state.since_id
  ans = {
    # // Remember the most recent id, so our requests are incremental
    "state": {
      since_id: since_id
    },
    "schema" : {
      "cryptoData" : {
        "primary_key" : ["timestamp"]
      }
    },
    "insert": {
      "cryptoData": cryptoData
      },
    "hasMore" : False
  }
  return ans;
