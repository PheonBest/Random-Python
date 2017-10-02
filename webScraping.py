from bs4 import BeautifulSoup
import requests

page = requests.get('http://www.jeuxvideo.com/forums/42-51-53326975-259-0-1-0-m6-dossier-tabou-harcelement-sexuel-les-femmes-n-en-peuvent-plus.htm')
contents = page.content
soup = BeautifulSoup(contents, 'html.parser')
 
#msgList = soup.findAll("div"); 
msgList = soup.findAll("div", { "class" : "txt-msg  text-enrichi-forum "}) # <-- UN EPSACE POURQUOI JVC
print(len(msgList))