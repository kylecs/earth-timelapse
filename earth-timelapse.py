import requests
import json
import shutil
import os
from datetime import datetime, timedelta
from subprocess import call
import time
import sys
import argparse

#Make API call, return response body in JSON format
def call_api(lat, lon, date):
    data = {"lat" : str(lat), "lon" : str(lon), "date" : date, "api_key" : api_key, "cloud_score" : "True"}
    response = requests.get("https://api.nasa.gov/planetary/earth/imagery", params=data)
    if response.status_code is not 200:
        print("API call failed!")
        return None
    return response.json()

def get_image(url, filename):
    path = "./data/" +  filename + ".png"
    response = requests.get(url, stream=True)
    if response.status_code is not 200:
        print("Image download failed!")
        return None
    out = open(path, "wb")
    shutil.copyfileobj(response.raw, out)
    return out.name

#Get all the suitable images from between 2 dates
def create_timelapse(lat, lon, start_date, end_date, clouds, cloudscore):
    cur_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    delta = timedelta(days=16)
    while end_date > cur_date:
        response = call_api(lat, lon, cur_date.strftime("%Y-%m-%d"))
        print("Api Call")
        print(response)
        if not clouds:
            if response is None or "cloud_score" not in response or response["cloud_score"] is None or response["cloud_score"] > cloudscore:
                 print("Request does not match threshold")
            else:
                get_image(response["url"], cur_date.strftime("%Y-%m-%d"))
        else:
            get_image(response["url"], cur_date.strftime("%Y-%m-%d"))

        cur_date = cur_date + delta
    call(["convert", "-delay", "50", "-loop", "0", "./data/*.png", "output.gif"])
    call(["rm", "-rf", "./data"])

parser = argparse.ArgumentParser(description="Create timelapse from nasa earth image api")
parser.add_argument("--latitude")
parser.add_argument("--longitude")
parser.add_argument("--start", help="Starting date in form YYYY-MM-DD, defaults to 2015-01-01")
parser.add_argument("--end", help="Ending date in form YYYY-MM-DD, defaults to current date")
parser.add_argument("--apikey", help="NASA API Key, Defaults to key in api-key file or DEMO_KEY")
parser.add_argument("--clouds", help = "Incude clouds in timelapse? Defaults to false")
parser.add_argument("--cloudscore", help="Maximum value for cloudscore to include in timelapse, default = 0.1, maximum = 1.0")
args = parser.parse_args()

#Validate arguments
if args.latitude is None or args.longitude is None:
    print("Please supply coordinate arguments")
    exit()

end = datetime.today()
if args.end:
    try:
        end = datetime.strptime(args.end, "%Y-%m-%d")
    except:
        print("Please supply end date in form: YYYY-MM-DD")
        exit()

start = datetime.strptime("2015-01-01", "%Y-%m-%d")
if args.start:
    try:
        start = datetime.strptime(args.start, "%Y-%m-%d")
    except:
        print("Please supply start date in form: YYYY-MM-DD")

clouds = False
if args.clouds is not None and (args.clouds == "True" or args.clouds == "true" or args.clouds == "yes" or args.clouds == "Yes"):
    clouds = True

cloudscore = 0.1
if args.cloudscore is not None:
    cloudscore = float(args.cloudscore)

#Try getting api key from file, or else use DEMO_KEY
if args.apikey is None:
    try:
        api_file = open("api-key", "r")
        api_key = api_file.read().strip()
    except:
        api_key = "DEMO_KEY"
        print("No API key, using DEMO_KEY")

#Prepare data directory to store images
if os.path.exists("./data"):
    call(["rm", "-rf", "./data"])
os.makedirs("./data")

#Call main function
create_timelapse(args.latitude, args.longitude, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), clouds, cloudscore)
