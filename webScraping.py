from bs4 import BeautifulSoup
import requests

 
page_number = 1; 
url = "############################################################################################################"; #"http://www.jeuxvideo.com/forums/42-51-53306780-"+str(page_number)+"-0-1-0-risibank-solution-finale-contre-les-stickers-pirates.htm"
url_topic_list = "http://www.jeuxvideo.com/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm"
page = requests.get(url_topic_list)
contents = page.content
soup = BeautifulSoup(contents, 'html.parser')
topicList = soup.findAll("a", { "class" : "lien-jv topic-title" });
 
def refreshUrl():
	global page_number, url, page, contents, soup
#url = "http://www.jeuxvideo.com/forums/42-51-53306780-"+str(page_number)+"-0-1-0-risibank-solution-finale-contre-les-stickers-pirates.htm"
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


def getCommand():
	global page_number, topicList, url
	command = input();
	print("cmd : " + command)
	if command[0] == "g" and command[1] == "o":
		nbr = None;
		if len(command) == 5:
			nbr = command[3]+command[4]
		elif len(command) == 4:
			nbr = command[3]
		if nbr != None:
			print(nbr)
			url = "http://www.jeuxvideo.com" + topicList[int(nbr)]["href"]
			print(url)
			refreshUrl();
			printAllPost();
	if url[48] == '-':
		page_number = int(url[47])
 	elif url[49] == '-':
		page_number = int(url[47]+url[48])
	elif url[50] == '-':
		page_number = int(url[47]+url[48]+url[49])
	if command == "np": # next page
		if nbr < 10:

		refreshUrl();
		printAllPost();
	if command == "bp":
		refreshUrl();
		printAllPost();
	elif command == "bp":
		print("Vous avez atteint la page minimum")
 
	getCommand();


for i in range(0, len(topicList)):
	print("["+str(i)+"] "+topicList[i].text)

getCommand();
print("choose topic")

'''  
printAllPost();
getCommand();'''