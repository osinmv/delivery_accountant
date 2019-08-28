import requests
import json
CUSTOMER = "Customers"
VENDOR = "Vendor"
CUSTOMER_DB = "customers"
VENDOR_DB = "vendors"
URL = "http://127.0.0.1:5000"


def request_by_docket(docket):
    return requests.get(URL+"/docket/"+str(docket)).json()


def request_recent():
    return requests.get(URL+"/recent/10").json()


def request_partners(info):
    return requests.get(URL+"/partners/"+info).json()


def request_partner_info(info, partner):
    return requests.get(URL+"/partners/"+info+"/"+partner).json()

