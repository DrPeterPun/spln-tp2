#pip install googletrans==3.1.0a0
# a versao 3.0.0 da erro
import googletrans

trans = googletrans.Translator()

def gettrans(name):
    print("opening file: ",name)
    f = open(name,"r")
    print("reading file: ",name)
    lines = f.readlines()

    pos=[]
    for s in lines:
        print("translating word:\t", s.strip("\n"))
        t = trans.translate(s,dest='pt',src='en')
        print("got word:\t\t",t.text,"\n")

        if s==t.text:
            #a traducao é igual o que significa que nao reconheceu a palavra 
            print("No translation found")
        else:
            pos.append(t.text)
    f.close()
    return pos

badlist = gettrans("neg_en.cat")
f = open("neg_pt.cat","w")
for w in badlist:
    f.write(w)
    f.write("\n")
f.close()

goodlist = gettrans("pos_en.cat")
f = open("pos_pt.cat","w")
for w in goodlist:
    f.write(w)
    f.write("\n")
f.close()
