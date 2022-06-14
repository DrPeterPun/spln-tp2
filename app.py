from tkinter import filedialog
from insta import get_info
from anal import analise
import sys, os
import matplotlib.pyplot as plt

############################ Funções Auxiliares ############################

# bloquear a impressão para o stdout
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# permitir a impressão para p stdout
def enablePrint():
    sys.stdout = sys.__stdout__

# cria um gráfico circular, tendo como base os valores presentes num dicionário
def pie_chart(dic):

    labels = []
    sizes = []
    #add colors
    colors = ['#034630','#a0503c','#d49d48']

    for key, value in dic.items():
        if value > 0:
            sizes.append(value)
            labels.append(key)

    fig, ax1 = plt.subplots()
    _, _, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85, colors=colors)

    for ins in autotexts:
        ins.set_color('white')

    #draw circle
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    ax1.axis('equal')
    plt.tight_layout()
    plt.savefig('out/pie_chart.png')

def html(likes, comments,tabela):

    file = open("out/output.html", "w+")

    # conteúdo inicial
    content = [ '<!DOCTYPE html>\n',
                '<html>\n'
                '\t<head>\n',
                '\t\t<meta charset="UTF-8">\n',
                '\t\t<title>Instagram Analysis</title>\n',
                '\t\t<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">\n',
                '\t</head>\n',
                '\t<style>\n',
                '\t\t.w3-igreen {color: #FFFFFF !important;background-color:#034630 !important}\n',
                '\t\t.w3-ired {color:#FFFFFF !important;background-color:#a0503c !important}\n',
                '\t\t.w3-iyellow {color:#FFFFFF !important;background-color:#d49d48 !important}\n',
                '\t\t.w3-ipink {color:#FFFFFF !important;background-color:#d19998 !important}\n',
                '\t</style>\n',
                '\t<body>\n']

    content.extend(['\t<div class="w3-container w3-igreen">\n',
                    '\t\t<h1>Instagram Analysis</h1>\n',
                    '\t</div>\n'])

    photo = ''
    dFile = ''
    profile_path = 'out/' + ACCOUNT

    # descobrir o nome da imagem e do ficheiro com a descrição
    filelist=os.listdir(profile_path)
    for f in filelist[:]:
        if f.endswith(".jpg"):
            photo = f
        elif f.endswith(".txt"):
            dFile = f

    # recolher a descrição do ficheiro .txt
    description = open(profile_path + '/' + dFile, 'r').read()

    content.extend(['\t<div class="w3-row">\n',
                    '\t\t<div class="w3-container w3-third" style="padding:0.20cm">\n',
                    '\t\t\t<div class="w3-card" style="width:100%">\n',
                    '\t\t\t\t<img src="' + ACCOUNT + '/' + photo + '"; style="width:100%">\n',
                    '\t\t\t\t<div class="w3-container w3-iyellow">\n',
                    '\t\t\t\t\t<h4><b>@' + ACCOUNT + '</b></h4>\n',
                    '\t\t\t\t\t<p><i>' + description + '</i></p>\n',
                    '\t\t\t\t</div>\n',
                    '\t\t\t</div>\n',
                    '\t\t</div>\n',
                    '\t\t<div class="w3-container w3-twothird">\n',
                    '\t\t<div class="w3-row">\n',
                    '\t\t\t<div class="w3-half w3-container" style="padding:0.20cm">\n',
                    '\t\t\t\t<img src="pie_chart.png"; style="width:100%">\n',
                    '\t\t\t</div>\n',
                    '\t\t\t<div class="w3-half w3-container" style="padding:0.20cm">\n',
                    '\t\t\t\t<div class="w3-container w3-round w3-ired">\n',
                    '\t\t\t\t\t<p>Número de likes:&nbsp;' + str(likes) + '</p>\n',
                    '\t\t\t\t\t<p>Número de comentários:&nbsp;' + str(comments) + '</p>\n',
                    '\t\t\t\t</div>\n',
                    '\t\t\t</div>\n',
                    '\t\t</div>\n',
                    '\t\t</div>\n',
                    '\t</div>\n'])

    #add tabela
    content.extend(['<table>\n',
                    '\t<tr>\n',
                    '\t\t<th>\n'
                    '\t\t<th>Likes</th>\n',
                    '\t\t<th>Comments</th>\n',
                    '\t\t<th>Sentiment</th>\n','\t</tr>\n'])
    (l,c,s) = tabela[1]
    content.extend( ['\t<tr>\n',
                        '\t\t<th>Valores médios </th>\n',
                        '\t\t<th>'+str(l)+'</th>\n',
                        '\t\t<th>'+str(c)+'</th>\n',
                        '\t\t<th>'+str(s)+'</th>\n',
                        '\t</tr>\n'])

    i=0

    for l,c,s in tabela[1:]:
        content.extend(['\t<tr>\n',
                        '\t\t<th>Comentário ' + i +'</th>\n',
                        '\t\t<th>'+str("{:.2%}".format(l))+'</th>\n',
                        '\t\t<th>'+str("{:.2%}".format(c))+'</th>\n',
                        '\t\t<th>'+str("{:.2%}".format(s))+'</th>\n',
                        '\t</tr>\n'])
        i+=1

    content.extend(['\t</table>\n'])

    # adicionar conteúdo final
    content.extend(['\t</body>\n',
                    '</html>\n'])

    file.writelines(content)
    file.close()

############################ Função Principal ############################

# como o instaloader, módulo de Python utilizado para recolher os comentários de um post de Instagram,
# exige que se esteja logged in para aceder ao comentários, criou-se uma conta de teste com as seguintes
# credênciais:
USER = "helloworld.ipynb"
PASSWORD = "SPLN2022"

# username da conta à qual queremos ir buscar os comentários do último post
ACCOUNT = "radiocomercial"

# flag que indica se queremos coletar os comentários do Instagram ou se queremos utilizar um documento já existente
COLLECT = True

# número dos post que queremos consultar
# considera-se que a numeração começa no 0
N = 2

# escreve os comentário presentes no último post de Instgram do user ACCOUNT

posts = []
#alaniza os ultimos N posts da conta
for i in range(N):
    # dicionário que armazena o número de comentários positivos, neutros e negativos
    dic = {"Positivos": 0, "Negativos": 0, "Neutros": 0}
    if COLLECT:
        likes, comments = get_info(USER, PASSWORD, ACCOUNT, N)
    else:
        likes = 'undefined'
        comments = 'undefined'

    # realiza a análise de sentimento dos comentários
    avg_sa=0
    for comment in open("out/comments.txt", "r").readlines():
        blockPrint()
        sa = analise(comment)
        avg_sa+=sa
        enablePrint()
        print(sa, ">", comment)
        if sa<0:
            dic["Negativos"] += 1
        elif sa>0:
            dic["Positivos"] += 1
        else:
            dic["Neutros"] += 1

    posts.append(likes,comments,dic,avg_sa/len(dic))

avg_likes = sum(map(lambda  l,c,d,s : l,posts))/len(posts)
avg_comments = sum(map(lambda l,c,d,s: c,posts))/len(posts)
avg_sentv = sum(map(lambda l,c,d,s: s,posts))/len(posts)

tabela = [(avg_likes,avg_comments,avg_sent)]
print("analise dos ultimos ",N," posts")
print("valores médios:")
print("Likes\tComentários\tSentimento")
print(avg_likes,"\t",avg_comments,"\t",avg_sent)
#nr likes, comentarios, SA do 
for l,c,d,s in posts:
    #calcula a diferenca percentual de likes, comentarios e sentimento em relacao a media
    pdlikes = l/avg_likes
    pdcoms = c/avg_comments
    pdsent = s/avg_sent
    tabela.append(pdlikes,pdcoms,pdsent)
    print(pdlikes,"\t",pdcoms,"\t",pdsent)


print(dic)
pie_chart(dic)
html(likes, comments, tabela)
