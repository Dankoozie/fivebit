#Fivebit version 0.2g [27/01/2016] by Dankoozie
# ---official site--- http://fivebit.download

#5bit encoding / compression
#0-25 - abcdefghijklmnopqrstuvwxyz
#26 - Spás
#27 - Change to UCase / end of message
#   - 27,31 Caps lock on
#   - 27,30 Num lock on
#   - 27,31...31 release

#28 - Numeric/Punc.  
#29 - Reserved
#30 - Dict1024
#31 - UTF-8 escape

from math import ceil

std_chars = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ')
std_ucase = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[',chr(92),']','^')
std_num = ('!',"\"" ,'#','$','%','&',"'",'(',')','*','+',',','-','.','/','0','1','2','3','4','5','6','7','8','9',':', ';', "<",  "=",  ">",  "?",  "@")

#7 = num  lock, 6 = caps lock
std_decode =[(0,k) for k in std_chars] + [(1,None),(2,None),(3,None),(4,None),(5,None)]
std_ucase_decode =  [(0,k) for k in std_ucase] + [(7,None),(6,None)]
lock_ucase_decode = [(6,k) for k in std_ucase] + [(6," "),(0,None)] # Space is (30) here - ^ ommited, 31 = release
lock_num_decode = [(7,k) for k in std_num][:-1] + [(0,None)] # 31 = release

#dict_reverse = dict((w,d) for d,w in dic1024.items())

dic1024 = {}
f = open('english-1.txt','r')
for a in range(1024):
	dic1024[a] = f.readline().strip()
f.close()

dict_reverse = dict((w,d) for d,w in dic1024.items())


def load_dict(filename):
    dic1024 = {}
    f = open(filename,'r')
    for i in range(0,1024):
        cw = f.readline()
        if(len(cw.rstrip()) > 2): dic1024[i] = cw.rstrip()
	
    dict_reverse = dict((w,d) for d,w in dic1024.items())      

def shift(val,amt):
    if(amt >= 0):
        return(val << amt)
    elif(amt < 0):
        return(val >> abs(amt))

class Substitute:
    
    def __init__(self):
        self.dict_last = False
        self.dict_fchar = 0
        self.unicode_len = 0
        self.unicode_buffer = []

    #Desub functions
    def __desub_lcase(self,a):
        #Character greater than 26 = Mode switch
        return(std_decode[a])
                   
    def __desub_ucase(self,a):
        return(std_ucase_decode[a])
    
    def __desub_capslock(self,a):
        return(lock_ucase_decode[a])

    def __desub_numlock(self,a):
        return(lock_num_decode[a])
        
    def __desub_num(self,a):
        return((0,std_num[a]))

    def __desub_dic1024(self,a):
        if(not self.dict_last):
            self.dict_fchar = a
            self.dict_last = True
            return((4,None))
        else:
            self.dict_last = False
            return(0,dic1024[((self.dict_fchar << 5) | a)] + " ")

    def __desub_twentynine(self,a):
        return((0,None))

    def __desub_unicode(self,a):
        if(self.unicode_len == 0):
            self.unicode_len = a
            if(a == 0): return((0,chr(0))) #Handle null character
            return((5,None))
        elif(self.unicode_len > 0):
            self.unicode_buffer.append(a)
            
            if(self.unicode_len == len(self.unicode_buffer)):
                char = self.__get_unicode(self.unicode_buffer)
                self.unicode_len = 0
                self.unicode_buffer = []
                return((0,char))
            return((5,None))

    #Unicode gen/get
    def __gen_unicode(self,char):
        ordn = ord(char)
        bl = ordn.bit_length()
        li = [31,ceil((bl) / 5)]

        for i in range(0,li[1]):
            li.append(((ordn >> 5*i) & 31))

        return li

    def __get_unicode(self,clist):
        ccode = 0
        for i in range(0,len(clist)):
            ccode = (ccode << 5) + (clist[len(clist) - i - 1] & 31)
        return chr(ccode)

    def desub(self,charlist,usedict = True):
        self.unicode_len = 0 # Reset unicode len
        self.unicode_buffer = [] # and buffer
        
        mos = {0:self.__desub_lcase,1:self.__desub_ucase,2:self.__desub_num,3:self.__desub_twentynine,4:self.__desub_dic1024,5:self.__desub_unicode,6:self.__desub_capslock,7:self.__desub_numlock}
        cl = []
        mode = 0

        for a in charlist:
            (mode,st) = mos[mode](a)
            if(st != None): cl.append(st)

        #Cut off trailing space if last mode was a dictionary word
        if(len(cl) > 0):
            if(cl[-1].strip() in dic1024.values()): cl[-1] = cl[-1].strip()

        return "".join(cl)


	#Experimental new first pass
    def sub(self,strin,usedict = True):
        op = []
        ld = False
        ke = 0

        dr = dict_reverse
        if(usedict == False): dr = dict()
        
        spl = strin.split(" ")
        for x in spl:
            try:
                ke = dr[x]
                op.extend((30,ke >> 5,ke & 31))
                ld = False
                ed = True
            except KeyError:
                if(len(x)>0): 
                    op.extend(s.subbe(x))
                    op.append(26)
                    ld = True
                    ed = False
                elif(len(x) == 0):
                    op.append(26)
                    ld = True
    
        if(ld and (not ed)): op.pop()
        #Throw in blank character if more than 5 bits free
        BitsFree = 8 - (len(op) * 5) % 8
        if( (BitsFree > 4) and (BitsFree != 8)): op.append(27)
        return op

    def __subpass_uppercase_strings(self,strin):
        pass


    def subbe(self,str_in):
        #Zero length string
        if(str_in == ""): return []
        cl = []

        for a in str_in:
            #c_num = ord(a)
            try:
                cl.append(std_chars.index(a))
                #return cl
            except ValueError: 

#            if(a in std_chars): cl.append(std_chars.index(a))
                try:
                    cl.extend([27,std_ucase.index(a)])
                #return cl 
                except ValueError: 


#            if(a in std_ucase): #Upper case (formerly and [\]^_`)
#                cl.extend([27,std_ucase.index(a)])

                   try:
                       cl.extend([28,std_num.index(a)])
                   except: cl.extend(self.__gen_unicode(a))

#            elif(a in std_num.values()): cl.extend(num_chars[c_num])

            #else:
                #UTF-8
           #     cl.extend(self.__gen_unicode(a))

        return cl

def encode(charlist):
    #Converts a list of 5-bit values (0-31) into byte string
    nexstep = {0:(5,3), 1:(6,2), 2:(7,1), 3:(0,0), 4:(1,-1,1,7), 5:(2,-2,3,6), 6:(3,-3,7,5), 7:(4,-4,15,4) }
    curbyte = 0
    bstr = []
    lastbit = []
    step = 0
        
    ByteLeft = False
    
    bistro = []

    #as_num = (a[0] << 35) + (a[1] << 30) + (a[2] << 25) + (a[3] << 20) + (a[4] << 15) + (a[5] << 10) + (a[6] << 5) + a[7] 
    #For speed we encode 8 characters at a time (40b)
    for f in range(int(len(charlist) / 8)):
        thisbit = charlist[f*8:(f*8)+8]
        as_num = (thisbit[0] << 35) + (thisbit[1] << 30) + (thisbit[2] << 25) + (thisbit[3] << 20) + (thisbit[4] << 15) + (thisbit[5] << 10) + (thisbit[6] << 5) + thisbit[7]
        bistro.append(as_num.to_bytes(5,'big'))             


    if(len(charlist) % 8 > 0): #Catch remaining characters
        lastbit = charlist[0-(len(charlist)%8):]

    for a in lastbit:
        curbyte = curbyte | shift(a,nexstep[step][1])
        ByteLeft = True
        if(step > 2):
            bstr.append(curbyte)
            curbyte = 0
            ByteLeft = False
            if(step > 3):
                curbyte = (a & nexstep[step][2]) << nexstep[step][3]
                ByteLeft = True
        step = nexstep[step][0]
        
    if ByteLeft:
        bstr.append(curbyte)
    
    #return bytes(bstr)
    return b''.join(bistro) + bytes(bstr)

def drawchars(byte,nbits,nbitsl):
    tot = 8 + nbitsl
    itot = (nbits << 8) | byte
    if(tot < 10):
        c1 = itot >> (tot - 5) & 31
        newnbits = itot & (2**(tot -5) -1)
        newnbitsl = tot - 5
        return(([c1],newnbits,newnbitsl))
    elif(tot > 9):
         c1 = itot >> (tot - 5) & 31
         c2 = itot >> (tot - 10) & 31
         newnbits = itot & (2**(tot - 10)-1)
         newnbitsl = tot - 10
         return(([c1,c2],newnbits,newnbitsl))
    
def decode(string):
    bs = bytes(string)
    nbl = 0
    nbs = 0
    ls = []
    ns = None
    as_num = 0
    lastbit = b''
    #Try to get 5 bytes at a time first for a while
    for b in range(int(len(bs)/5)):
        as_num = as_num.from_bytes(bs[b*5:(b*5)+5],'big')                
        ls.extend([as_num >> 35, (as_num >> 30) & 31, (as_num >> 25) & 31, (as_num >> 20) & 31, (as_num >> 15) & 31, (as_num >> 10) & 31, (as_num >> 5) & 31, as_num & 31])

    if(len(bs) % 5 > 0): #Catch remaining characters
        lastbit = bs[0-(len(bs)%5):]

        for a in lastbit:
            rs = drawchars(a,nbs,nbl)
            nbs = rs[1]
            nbl = rs[2]
            ls.extend(rs[0])
    return ls

s = Substitute()



def compress(string,usedict = True):
    return(encode(s.sub(string,usedict)))

def decompress(string):
   return(s.desub(decode(string)))

