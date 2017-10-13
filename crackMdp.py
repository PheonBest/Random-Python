import time
alphabet = ['a','b','c','d','e','f','g','h','j','i','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0'];

mdp = str(input("Choisissez un mdp"));


tempMdp = []
for i in range (0, len(alphabet)):
	tempMdp.append("")
e = 0
def decrypt(nbr):
	global mdp, tempMdp,e 
	for j in range(0, len(alphabet)):
		for i in range(0, len(alphabet)):
			#time.sleep(0.1)
			e += 1
			print(e)
			for c in range(0, len(alphabet)):
				tempMdp[0] = alphabet[i]
				tempMdp[1] = alphabet[i-1]
				tempMdp[2] = alphabet[i-2]

				tempMdp[j] = alphabet[c]
				tempMdpJoin  = "".join(tempMdp)			
				print("-- test --- ! " + tempMdpJoin + " !")
				if str(tempMdpJoin) == mdp:
					print("trouvé !")
					return								 
 
 
decrypt(2)