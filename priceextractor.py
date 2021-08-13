import requests
from requests.structures import CaseInsensitiveDict
import json
import csv
f =open("prices.csv","w")
writer = csv.writer(f)

def tokengenerator():
  url = "<insert url here>"
  headers = CaseInsensitiveDict()
  headers["Authorization"] = "Basic <insert token here>"
  headers["Content-Type"] = "application/x-www-form-urlencoded"
  resp = requests.post(url, headers=headers)
  return (resp.json()["access_token"])
inquirytoken = tokengenerator()

def priceextractor(data):
  url = "<insert inquiry url here >"
  headers = CaseInsensitiveDict()
  headers["Authorization"] = "Bearer "+inquirytoken
  headers["Content-Type"] = "application/json"
  resp = requests.post(url, headers=headers, data=data)
  jsonresponse = resp.json()
  regularprice = resp.json()["items"][0]["totalRegularPrice"]
  discountedprice = resp.json()["items"][0]["discountPrice"]
  prices = {"regularprice":regularprice,"discountedprice":discountedprice}
  return prices

inputfile=""
try:
  inputfile = open("inquiry.txt","r")
except:
  print("could not locate file, so, i am creating a file for you, and you can edit that.")
  inputfile=open("inquiry.txt","a")
  inputfile.write("<add barcode here>,<add quantity>")
inputfile = open("inquiry.txt","r")
lines = inputfile.readlines()
for line in lines:
  try:
    splittedline = line.split(",")
    barcode = splittedline[0]
    quantity = splittedline[1].rstrip("\n")
    data = {
    "division": "<add sensitive data here>",
    "facilityId": "<add facilityid here>",
    "items": [
    {
      "consumerUpc": barcode,
      "quantity": quantity
    }
    ],
    "loyaltyId": 44510383810,
    "store": "00353"
    }
    strdata = json.dumps(data)
    itemprices=priceextractor(strdata)
    row=[barcode,quantity,itemprices["regularprice"],itemprices["discountedprice"]]
    writer.writerow(row)
  except:
    pass