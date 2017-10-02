from bs4 import BeautifulSoup
import requests
#http://www.skstream.ws/series/rick-et-morty/saison-1/episode-10/version-francaise
def printA(url):
	page = requests.get(url)
	contents = page.content
	soup = BeautifulSoup(contents, 'html.parser')

	a = soup.findAll("a")
	for i in range(0, len(a)):
		print(a[i].text)

printA(input())