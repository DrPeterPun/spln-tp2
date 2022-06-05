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
multiplicadores = {"nao":-1,"muito":2,"pouco":-2}

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

# divide uma frase em palavras e/ou expressões
def expressoes(frase):
    output = []
    for phrase in nlp(frase).sents:
        state = 0
        for word in phrase:
            
            if state==0:
                if word.pos_ == 'ADV' or word.pos_ == 'ADJ' or word.lemma_.lower() == 'tudo':
                    exp = word.lemma_
                    state = 1
                else:
                    output.append(word.lemma_)

            elif state==1:
                if word.pos_ == 'ADV' or word.pos_ == 'ADJ' or word.lemma_.lower() == 'tudo':
                    exp += " " + word.lemma_
                else:
                    output.append(exp)
                    output.append(word.lemma_)
                    state = 0

        if state==1:
            output.append(exp)

    print("Depois de partir por expressões e/ou palavras:",str(output),"\n")

    return output

#analisa uma string
def analise(s):
    s = flatten(dividir(s))
    print("\nA analisar a string:",s)
    sa_count = []
    if isinstance(s,list):
        for oracao in s:
            if len(re.sub(r'\s','' , oracao))>0:
                sa_count.append(analisa_oracao(oracao)) 
            else:
                #string vazia
                pass
    else:
        sa_count.append(analisa_oracao(s)) 
    sa = sum(sa_count)/(len(sa_count))
    print("--------------------------------------------------------------")
    print("SA da string total:",sa,"\n")

def analisa_oracao(oracao):
    print("--------------------------------------------------------------")
    print("A analisar a oração:",oracao,"\n")
    sums =[]
    mults=[]
    #separamos sl por palavras e/ou expressões
    for exp in expressoes(oracao):

        # verificamos se a expressão ou palavra está na lista ou nos multiplicadores
        if exp in list(lista):
            print("Na lista palavras:", exp,"| com valor:",lista[exp],"\n")
            sums.append(exp)
        elif exp in list(multiplicadores):
            print("Na lista de multiplicadores:", exp,"| com valor:",multiplicadores[exp],"\n")
            mults.append(exp)

        # se estamos perante uma expressão que não estava na lista nem nos multiplicadores
        elif len(exp.split())>1:
            print("Partimos a expressão em ",exp.split(),"\n")
            # partimos a expressão em palavras e verificamos se estas estão na lista ou nos multiplicadores
            for word in oracao.split():
                if word in list(lista):
                    print("Na lista palavras:", word,"| com valor:",lista[word],"\n")
                    sums.append(word)
                elif word in list(multiplicadores):
                    print("Na lista de multiplicadores:", word,"| com valor:",multiplicadores[word],"\n")
                    mults.append(word)

        # se estiver em multiplicadores chamamos mult
    m = list(map(lambda a: multiplicadores[a], mults))
    m = functools.reduce(lambda a,b: a*b, m ,1)

    a = list(map(lambda a: lista[a], sums))
    if len(a)>0:
        a = sum(a)/len(a)
    else:
        a = 0

    sa = mult(a, m)
    print(">>>> SA desta oracao:", sa, "<<<<")
    return sa

#s="a gata fugiu para o jardim, porque precisava de fazer coco"
s = "A gata sabia muito bem o que estava a fazer. Muito horrível. Queria que ficasse tudo bem."
analise(s)