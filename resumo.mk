# Resumo do trabalho feito

Neste trabalho construimos um SA (Sentiment Analizer) baseado em regras, Tentamos melhorar a precisao do mesmo com a ajuda do dataset de tweets em portugues utilizado nas aulas, e por fim posemos em pratico o nosso SA a avaliar os comentários de posts de Instagram

Primeiro de tudo foi analisado um dataset que contianha uma lista de palavras positivas e negativas de forma a ter uma base sobre a qual trabalhar, primeiro tornado mais facil de ler o ficheiro removendo toda a informação desnecessária e depois traduzindo para portugues utilizando o tradutor da google.

A cada uma destas palavras foi atribuido um valor de **±** 0.5. Foi tambem criada manualmente uma lista de palavras que servem como multiplicadores. Para calcular o Sentimento de uma dada oração ḿultiplicado o valor de cada multiplicador pela soma dos valores absolutos. Ex. Para "não gosto disto" sera detetado a palavra "gosto" que tem valor posivito, que será negado pela presenca de um "não" dando assim um valor negativo para o sentimento. Como cada palávra pode aparecer em várias formas utilizamos um lematizador para as conseguir emparelhar à forma "normal" (Ex.: "corremos" -> "correr").

Depois de utilizar o dataset de tweets para reavaliar os valores associados a cada palavra, a *accuracy* subiu de 75% para 98%. Este valor é obviamente suspeito dado ser tão alto e o dataset em si não é o melhor dado que todos os tweets têm um ":)" ou ":(" o que só por si pode caracterizar o sentimento do mesmo, mas o contributo que cada um destes têm não é alterado com o treino por isso não é a sua presenca que justifica mudanca de 75% para 98%.

Depois para por o trabalho em prática decidimos por em prática o nosso SA em comentários de instagram. Para expor os dados obtidos foi criada uma página html para uma dada conta analiza os ultimos N posts mostrando os valores médios de SA dos comentarios de cada post e tambem o valor médio de likes e de comentários. Mostra tambem uma analise mais detalhada do post numero N.
