import fivebit
fc = open('tioer.txt.5b','rb').read()
ds = fivebit.decode(fc)

ks = []
ls = []
for a in range(len(ds)-2):
	ls.append(ds[a:a+3])

print(ls)



