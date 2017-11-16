import urllib2
import xml.etree.ElementTree
import json
import sys
from openalpr import Alpr

config = "path to the openalpr.conf file" #change
runtimeData = "path to the openalpr runtime_data folder" #change
alpr = Alpr("aus", config, runtimeData)
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

alpr.set_top_n(1)

image = "path to image to get license plate" #change
results = alpr.recognize_file(image)
plates = []

for plate in results['results']:
    for candidate in plate['candidates']:
        plates.append(candidate['plate'])
        break

# Call when completely done to release memory
alpr.unload()

#this is username of the fake email
username = "kek"

for plate in plates:

    #get the webpage
    page = urllib2.urlopen("http://www.regcheck.org.uk/api/reg.asmx/CheckAustralia?RegistrationNumber=" + plate + "&State=NSW&username=" +username)

    #get the root of the file of the xml response
    root = e = xml.etree.ElementTree.parse(page).getroot()

    #get the json text concerning the details of the vehicle
    j = root[0].text
    d = json.loads(j)

    #if the colour is unable to be obtained
    string = d["Colour"]
    if string == "":
        string = "N/A"

    #print details
    print "The car is a", d["Description"]
    print "The state the car is licensed under is", d["State"]
    print "The year is was registered was", d["RegistrationYear"]
    print "The colour of the car is", string
    print "The vehicle identification number is", d["VechileIdentificationNumber"]

    #can change that so the user can download the image etc
    print "An image of the car is obtainable by this url", d["ImageUrl"]



