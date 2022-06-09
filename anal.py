import re
from googletrans import Translator #api de tradutor
import functools #higher order functions
#modulo de nlp em pt
import spacy
from spacy.lang.pt.examples import sentences
nlp = spacy.load("pt_core_news_sm")

#devolve o sinal de um numero
def sig(n):
    if n>=0:
        return 1
    return -1

#aplica a operacao de multiplicacao de sentimentos
#feita de forma a que o valor para mult <1 dinua, e para >1 aumente sem nunca passar de 1.
def mult(current,mult):
    if abs(mult)<=1:
        return current * mult
    else:
        m = abs(mult)
        mod_change = (1-abs(current) )
        return (abs(current) + mod_change*((m-1)/m)) * sig(current*mult)
#media
def mean(x,y):
    return (x+y)/2
#produto simples
def prod(x,y):
    return x*y


#lista de valores absolutos para palavras, entre -1 e 1
#lista = {"gosto":0.5,"desteto":-0.5,"passar":0.5,"reprovar":-0.5,"lido":0.5,"saboroso":0.5,"chumbei":-0.5}

def fill_lista():
    f= open("data/neg_pt.cat")
    for w in f.readlines():
        lista[w.strip("\n").lower()]=-0.5
    f.close()

    f= open("data/pos_pt.cat")
    for w in f.readlines():
        lista[w.strip("\n").lower()]=0.5
    f.close()
lista={}
fill_lista()

#palavras que alteral a intensidade do que foi dito. valores negativos passam de bom para mau e vice versa.
#valores em mod maiores que 1 aumentam a intensidade, menores diminuem
mpos = {"muito":2,"bastante":3,"tudo":3,"tanto":2,"todo":2,"mais":2,"tão":2,"provável":1.5,"suficiente":1.5}
mmenos = {"talvez":0.75,"alguns":0.5,"possível":0.75}
mneg = {"não":-1,"pouco":-2,"nenhum":-1,"nada":-1,"mal":-1}
multiplicadores = mpos | mneg | mmenos

#lista de strings para serem testadas
strings = [
 "passei no exame de condução.",
 "chumbei muito no exame de condução",
 "reprovei no exame de condução",
 "hoje choveu torrencialmente",
 "hoje está um lindo sol",
 "ontem comi uma pizza saborosa"
]

# divide uma string em oracoes ( de forma um bocado tosca )
def dividir(s):
    if re.search(r'\.\.\.', s):
        return list(map(lambda a: dividir(a) ,re.split(r'\.\.\.', s)))
    elif re.search('[,;?!.]', s):
        return list(map(lambda a: dividir(a) ,re.split('[,;?!.]', s)))
    return s
#
# tansforma listas (de listas)^n numa lista recursivamente
def flatten(l):
    if len(l)==0:
        return l
    if isinstance(l[0], list):
        return flatten(l[0])+flatten(l[1:])
    return l[:1]+flatten(l[1:])


#analisa uma string
def analise(s):
    s = flatten(dividir(s))
    print("a analisar a string:\n",s)
    sa_count = []
    if isinstance(s,list):
        sl = list(map(lambda c:functools.reduce(lambda a ,b :  a +" " + b.lemma_, nlp(c), ''),s ))
        print("lematized :")
        print(sl)
        for oracao in sl:
            if len(re.sub(r'\s','' , oracao))>0:
                sa_count.append(analisa_oracao(oracao)) 
            else:
                #string vasia
                pass
    else:
        sl = functools.reduce(lambda a ,b :  a +" " + b.lemma_, nlp(s), '')
        sa_count.append(analisa_oracao(sl)) 
    print("sa da string total")
    print(sum(sa_count)/(len(sa_count)))

def analisa_oracao(oracao):
    print("a analisar a ora¢ão lematizada:\n",oracao)
    sums =[]
    mults=[]
    #separamos sl por palavras
    for word in oracao.split():
        doc = nlp(word)
        lemma = doc[0].lemma_
        if lemma in list(lista):
            print("na lista palavras:", lemma,"; com valor: ",lista[lemma])
            sums.append(lemma)
        elif lemma in list(multiplicadores):
            print("na lista de multiplicadores: ", lemma,";com valor: ",multiplicadores[lemma])
            mults.append(lemma)
        # se estiver em multiplicadores chamamos mult
    m = list(map(lambda a: multiplicadores[a], mults))
    m = functools.reduce(lambda a,b: a*b, m ,1)

    a = list(map(lambda a: lista[a], sums))
    if len(a)>0:
        a = sum(a)/len(a)
    else:
        a = 0

    print("SA desta oracao:")
    sa = mult(a, m)
    print(sa)
    return sa

#supondo que temos um modelo alternativo que eu posso chamar com a funcao: altmodel(frase) que tbm devolve um nr entre -1 e 1
#oracao antes da lematizacao :s
def treina_oracao(s,oracao):
    print("a treinar o modelo com a ora¢ão lematizada:\n",oracao)
    sums =[]
    mults=[]
    #separamos sl por palavras
    for word in oracao.split():
        doc = nlp(word)
        lemma = doc[0].lemma_
        if lemma in list(lista):
            print("na lista palavras:", lemma,"; com valor: ",lista[lemma])
            sums.append(lemma)
        elif lemma in list(multiplicadores):
            print("na lista de multiplicadores: ", lemma,";com valor: ",multiplicadores[lemma])
            mults.append(lemma)
        # se estiver em multiplicadores chamamos mult
    m = list(map(lambda a: multiplicadores[a], mults))
    m = functools.reduce(lambda a,b: a*b, m ,1)

    a = list(map(lambda a: lista[a], sums))
    if len(a)>0:
        a = sum(a)/len(a)
    else:
        a = 0.5# estava como 0 mas acho que da melhores resultados com 0.5

    print("SA desta oracao:")
    sa = mult(a, m)
    altsa = altmodel(s)
    #diferenca entre as avaliacoes
    dif = altsa-sa
    for palavra in sums:
        lista[palavra]+=dif*0.1
        pass


s="a gata fugiu para o jardim"
analise(s)