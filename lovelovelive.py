import requests
import lxml
import re
from bs4 import BeautifulSoup as PrettySoup

def getUrls(url):
	raw_html = requests.get(url)
	html = PrettySoup(raw_html.text, "lxml")
	urlList = html.find_all("a", "category-page__member-link")
	songNames = []	
	songUrls = []

	for i in urlList:
		raw_html = requests.get("http://love-live.wikia.com" + i["href"])
		html = PrettySoup(raw_html.text, "lxml")

		theDiv = str(html.find(id = "ogg_player_1")).split(';')
		if(theDiv[0] != "None"):
			songNames.append(html.title.text.split('|')[0][:-1])

		for i in range(len(theDiv)):
			if(theDiv[i] == "videoUrl&quot"):
				songUrls.append((theDiv[i + 2])[:-5])
				break

	return(songNames, songUrls)

def getData(name, url):
	for i in range(len(name)):
		print(str(i + 1) + " of " + str(len(name)))
		bites = requests.get(url[i]).content

		f = open(re.sub("/|\\\\|\?|%|\*|:|\"|<|>|\.", "", name[i]) + ".oga", "wb")
		f.write(bites)
		f.close()


museUrl = "http://love-live.wikia.com/wiki/Category:Discography"
aqoursUrl = "http://love-live.wikia.com/wiki/Category:Discography:Aqours"

museData = getUrls(museUrl)
aqoursData = getUrls(aqoursUrl)

getData(museData[0], museData[1])
getData(aqoursData[0], aqoursData[1])