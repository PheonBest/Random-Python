from bs4 import BeautifulSoup
import requests
def getAllPost(jvc_topic_url):
	page = requests.get(jvc_topic_url)
	contents = page.content
	soup = BeautifulSoup(contents, 'html.parser')
	postList = soup.findAll("div", { "class" : "inner-head-content" });
	return postList
 


allPost = getAllPost("http://www.jeuxvideo.com/forums/42-51-53428771-1-0-1-0-les-punaises-de-lit-cet-enfer.htm")

for i in range(0, len(allPost)): 
	#print("------- Post N°" + str(i) + "-------")
	textFixed = allPost[i].text
	textFixed = textFixed.replace("MP", " ")
	textToInsert = "Post N°" + str(i)
	textFixed = list(textFixed)
	for a in range(0, len(textToInsert)):
		 textFixed[a] = textToInsert[a]

	print("".join(textFixed));
	
	for d in range(0, 2):
		print("\n")
