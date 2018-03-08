# Spécifications fonctionnelles détaillées

## PLAN :

## 1. Scrapping et constitution du jeu de données

## 2. Classification

## SPECIFICATIONS :

## 1. Scrapping et constitution du jeu de données



07 /03 **Script de scrapping :**


Le scrapping des charts se base sur un script qui récupère les résultats de google
image pour une requête. Ce script est disponible sur le GitHub au nom de google-
scrapper_2.0.py.

Nous l’avons obtenu en faisant un tour d’horizon de l’existant, avec comme critère de
trouver un script qui permette de scrapper à la fois une image et un json avec des
descripteurs. Nous avons trouvé un premier script mais qui avais le défaut de
n’extraire qu’un nombre limité d’image. En cherchant plus avant, nous avons trouvé
un nouveau script qui a permis de surmonter ce bridage. Nous l’avons adapté et
modifié selon nos besoins, notamment en termes de nommage des fichiers sortants
et de facilitation du procédé de lancement de requête afin de permettre une
meilleure parallélisation des tâches au sein du groupe.

Le script prend en entrée le terme de la recherche google image à effectuer et renvoie
tous les résultats disponibles sur la page jusqu’à ce que plus aucun résultat ne
s’affiche. Par résultat, on entend une image et un fichier json dont le nommage
répond à la règle suivante : requête_numérotation.format
Exemple : line_chart_ 30 .jpg
bar_chart_ 5 .json

Le script utilise une méthode de scrolling avec un driver adapté pour chrome et des
paramètres de gestion du temps (afin de ne pas être repéré comme un bot.)

Nous avons dans un premier temps lancé trois requêtes distinctes correspondant au
trois types de graphiques sur lesquelles nous allons nous concentrer :
- Line Chart (requête : line_chart)
- Bar Chart (requête : bar_chart)
- Scatter Ploit (requête : scatter plot)

Les résultats se trouvent dans un dossier situé dans le répertoire du scrapper, dont le
nom est « dataset ». Chaque sous-dossier de « dataset » correspond au résultat
d’une requête.

07/03  **Nettoyage du jeu de donnée :**


Une fois les trois requêtes lancées et les dossiers de données brutes constituées, nous
avons effectué une première phase de tri manuel avec comme objectif d’obtenir 230
images propres et utilisables.

Voici les critères que nous avons utilisé pour exclure les images non conformes. Ils
sont issus de l’expérience. Cette liste n’est pas exhaustive mais correspond au cas qui
reviennent le plus souvent.

Pour les trois catégories (line chart, bar chart, scatter plot) :

- Fond hétérogène ne permettant pas un contraste clair
- Graphique en 3 dimensions :
- Légende représentant une part trop importante de l’image


- Graphique regroupant 2 catégories (ex : à la fois bar et line chart)
- Graphique trop simpliste (type icône ou vecteur)
- Image comportant plusieurs graphiques :
- Graphique tracé manuellement :

**Critères spécifiques aux line Charts :**

- Zone pleine colorée en dessous de la ligne :


- Nombre trop important de lignes :

Critères spécifiques aux Scatter Plot :

- Fond de cartes :

Critères spécifiques aux Bar Chart :

**2. Classification**
