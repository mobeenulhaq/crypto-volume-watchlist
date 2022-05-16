import requests
import csv

headers = {
  'X-CMC_PRO_API_KEY' : '',
  'Accepts' : 'application/json'
}

limit = str(input("Search limit: "))
convert = str(input("Currency: "))
print('')

params = {
  'start' : '1',
  'limit' : limit,
  'convert' : convert
}

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

json = requests.get(url, params=params, headers=headers).json()

#print(json)

coins = json['data']

def ratio(mcap, vol):
  ratio = vol/mcap
  return ratio

ratiolist = []
for coin in coins:
  ratiolist.append([coin['cmc_rank'], coin['symbol'], ratio(coin['quote'][convert]['market_cap'], coin['quote'][convert]['volume_24h']), coin['quote'][convert]['volume_24h'], coin['quote'][convert]['market_cap']])

ratiolist_sorted = sorted(ratiolist, key=lambda x: x[2], reverse=True)

print("{:>4} {:>6} {:>9} {:>20} {:>20}".format("Rank", "Symbol", "Ratio", "Volume", "Market Cap"))
for coin in ratiolist_sorted:
  print(format(coin[0], '4'), format(coin[1], '6'), format(coin[2], '10.2f'), format(coin[3], '20,.2f'), format(coin[4], '20,.2f'))

head = ["Rank", "Symbol", "Ratio", "Volume", "Market Cap"]

file_name = ""

if convert == "USD":
  file_name = "maketdata_usd.csv"
elif convert == "BTC":
  file_name = "marketdata_btc.csv"

with open(file_name, 'w') as f:
  writer = csv.writer(f)
  writer.writerow(head)
  for coin in ratiolist_sorted:
      writer.writerow(coin)

search = input("Search coin by symbol: ")
found = False
while search != "-":
  for coin in ratiolist_sorted:
    if coin[1] == search:
      print("{:>4} {:>6} {:>9} {:>20} {:>20}".format("Rank", "Symbol", "Ratio", "Volume", "Market Cap"))
      print(format(coin[0], '4'), format(coin[1], '6'), format(coin[2], '10.2f'), format(coin[3], '20,.2f'), format(coin[4], '20,.2f'))
      found = True
      break
  search = input("Search coin by symbol: ")
  continue
 
if found == False:
  print("Token not found.")

# for coin in coins:
#   print(format(coin['symbol'], '5'), format(coin['quote']['USD']['price'],'20.2f'), format(coin['quote']['USD']['volume_24h'], '20.2f'), format(coin['quote']['USD']['market_cap'], '20.2f'))
