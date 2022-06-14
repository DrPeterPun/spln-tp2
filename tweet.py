import io
import re

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


def load_t():

    f = open("data/t10000","r")

    l=f.readlines()

    eval_dict = {}

    for line in l:
        s=line.split(",")
        tam = len(s)
        sent = 0.7 if s[-2] == "Positivo" else -0.7
        text = ",".join(s[1:-3])
        oracoes = flatten(dividir(text))
        if isinstance(s,list):
            for oracao in oracoes:
                if len(re.sub(r'\s','' , oracao))>0:
                    eval_dict[oracao] = sent
                else:
                    #string vazia
                    pass
        else:
            eval_dict[oracao] = sent

        #print(sent)
        #print(text)
        eval_dict[text] = sent

    test_dict={}
    f = open("data/t13000","r")

    l=f.readlines()
    for line in l:
        s=line.split(",")
        tam = len(s)
        sent = 0.7 if s[-2] == "Positivo" else -0.7
        text = ",".join(s[1:-3])
        test_dict[text]=sent

    return (eval_dict,test_dict)

print(load_t())

