import time
import fivebit as fivebit
import entropy
import random


#Test routines
def teststr(lent=65536,low=26,high=128):
	a = ""	
	for i in range(lent): a = a + chr(random.randrange(low,high))
	return a


print("Compressing random string 65536 characters, range 26-128 Dictionary on...")
tstr = teststr()
starttime = time.time()
h = (fivebit.s.sub(tstr))


for y in h:
	if(y > 31): print(y,h.index(y))



for u in range(256):
	print(u, ": ", h.count(u))	

d = fivebit.compress(tstr)
print("Execution time: " + str(time.time() - starttime) + " compressed length: " +str(len(d))  )

print("Decompressing random string 65536 characters, range 26-128 Dictionary on...")
starttime = time.time()
dec = fivebit.decompress(d)
print("Execution time: " + str(time.time() - starttime))
print( dec==tstr)

if(dec != tstr):
	print(tstr)
	print(dec)


print("Compressing random string 65536 characters, range 26-128 Dictionary off...")
starttime = time.time()
nd = fivebit.compress(tstr,False)
print("Execution time: " + str(time.time() - starttime))


#Random lowercase words
print("\n\n\nGenerating 50000 lowercase random words..")
lst = []
for i in range(50000):	
	lst.append(teststr(random.randrange(1,15),97,122) + " ")

wordlist = "".join(lst)
print("Testing compression time with dictionary enabled")
starttime = time.time()
d = fivebit.compress(wordlist,True)
print("Execution time: " + str(time.time() - starttime))
print("Testing compression time with dictionary disabled")
starttime = time.time()
nd = fivebit.compress(wordlist,False)
print("Execution time: " + str(time.time() - starttime))
print("Testing decompression time..")
print("Uncompressed length: " + str(len(wordlist)) + " Dict compressed length: " + str(len(d)) + " Nodict compressed length: " + str(len(nd)) )

#Random dictionary words
lst = []
print("\n\n\nGenerating 50000 lowercase random dictionary words..")
fl = fivebit.d.from_file('english-1.5b')[0]

for i in range(50000):	
	lst.append(fl[random.randrange(1024)] + " ")

starttime = time.time()
fivebit.decompress(fivebit.compress("".join(lst)))
print("Execution time: " + str(time.time() - starttime))



#Random gobbledegook words
print("\n\n\nGenerating 50000 gobbledegook random words..")
lst = []
for i in range(50000):	
	lst.append(teststr(random.randrange(1,15),1,255) + " ")

wordlist = "".join(lst)

print("Shannon entropy: " + str(entropy.shannon_entropy(wordlist)))

print("Testing compression time with dictionary enabled")
starttime = time.time()
d = fivebit.compress(wordlist,True)
print("Shannon entropy: " + str(entropy.shannon_entropy(d)))
print("Execution time: " + str(time.time() - starttime))
print("Testing compression time with dictionary disabled")
starttime = time.time()
nd = fivebit.compress(wordlist,False)
print("Execution time: " + str(time.time() - starttime))
print("Testing decompression time..")
starttime = time.time()
dec = fivebit.decompress(d)
print("Execution time: " + str(time.time() - starttime))
print("Uncompressed length: " + str(len(wordlist)) + " Dict compressed length: " + str(len(d)) + " Nodict compressed length: " + str(len(nd)) )
print( dec==wordlist)
