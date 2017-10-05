from bs4 import BeautifulSoup
import requests

page_number = 1; 
url = "http://www.jeuxvideo.com/forums/42-51-49873942-" + str(page_number) + "-0-1-0-les-depressifs-on-se-regroupe-ici.htm"
page = requests.get(url)
contents = page.content
soup = BeautifulSoup(contents, 'html.parser')


def refreshUrl():
	global url
	global page
	global contents
	global soup
	url = "http://www.jeuxvideo.com/forums/42-51-49873942-" + str(page_number) + "-0-1-0-les-depressifs-on-se-regroupe-ici.htm"
	page = requests.get(url)
	contents = page.content
	soup = BeautifulSoup(contents, 'html.parser')

def getAllPost():
	postList = soup.findAll("div", { "class" : "inner-head-content" });
	return postList
 

def printAllPost():
	allPost = getAllPost()
	for i in range(0, len(allPost)): 
		currentPage = soup.findAll("span", { "class" : "page-active" })[0].text;
		textFixed = allPost[i].text
		textFixed = textFixed.replace("MP", " ")
		textToInsert = "Page " + str(currentPage) +" "+ "Post N°" + str(i)
		textFixed = list(textFixed)
		for a in range(0, len(textToInsert)):
			 textFixed[a] = textToInsert[a]

		print("".join(textFixed));
		
		for d in range(0, 2):
			print("\n")


printAllPost();

'''
while page_number < 5:
 	page_number += 1;
 	refreshUrl();
 	printAllPost();
'''

command = input();
print(command)

if command == "np": # next page
	page_number += 1;
	refreshUrl();
	printAllPost();