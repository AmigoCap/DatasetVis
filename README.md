# DatasetVis

## Le projet

Ce répertoire permet à partir d'une base de données d'images contenant n classes différentes d'entraîner un modèle de réseaux de neurones convolutionnels et de le tester sur une base test.

À partir d'une base de données contenant n classes d'images de tailles et de formats quelconques, on redimensionne chaque image à la taille sizexsize et on convertit en JPG. Il est primordial que le nom de la classe de l'image soit dans son nom, et notre script pour scrapper Google Image le fait automatiquement, en renommant avec la requête réalisée.

On crée deux dossiers :
- /data contient x% des images pour entraîner le réseau de neurones convolutionnels
- /test contient (1-x)% des images pour tester le modèle finale enregistrée

À partir du dossier /data, on sérialise nos images de 'train' & 'validation' ainsi que leur labels respectifs dans un fichier pkl. Celui-ci sera lu pour entraîner le réseau de neurones. 
À la fin de l'entraînement, qui peut être plus ou moins long suivant les paramètres que vous avez choisi, le modèle est enregistré.

Il est ensuite utilisé automatiquement sur le dossier /test créé ultérieurement et en ressort une matrice de confusion.

Comme chaque variable intermédiaire est enregistrée (modèle CNN entraînée, dataset dans le fichier pkl, dossiers /data et /test) il est possible de les réutiliser sans réaliser toutes les étapes.

Dans le fichier <b>settings.py</b> il vous est possible de <b>modifier les différents paramètres</b> clés utilisés dans nos scripts Python, comme la taille des images, le part de l'ensemble test, etc.
 
## Lancement

Afin d'installer l'ensemble des packages nécessaires au fonctionnement du script, installer le module pip ([Page officielle](https://pypi.python.org/pypi/pip))  et exécuter la commande suivante :  

```
pip3 install -r requirements.txt
```

Dans le terminal, placez vous dans le dossier que vous venez de clôner.
Pour lancer le script, tapez :
```
python3 main.py
```
Après l'exécution du script, un fichier "results_<date_de_creation>.json" est créé. Celui-ci contient la date d'exécution, les paramètres utilisés ainsi, les différentes probabilités de label pour chaque image et des métriques sur chaque classe (précision et recall).

Ce fichier sera utilisé pour la visualisation des résultats à l'aide du framework d3.js.

## Scrapping

Nous utiliserons le script <b>google-scrapper_2.0.py</b> issu du git image-scrapers afin de peupler notre base de données. Celui-ci permet de récupérer des images issues de google et fournit un JSON associé.

Afin d'utiliser le script de scrapping, il faut:
- installer les différents modules importés en début de script
- installer le driver chrome correpondant à la version du navigateur GoogleChrome présente sur l'ordi ([Page officielle](https://chromedriver.storage.googleapis.com/index.html))
- modifier la ligne 24 du script et renseigner l'emplacement du driver 

```
browser = webdriver.Chrome(executable_path=r'C:/Users/ACER/Desktop/Projet_Info/chromedriver.exe')
```

Après modification du script, il faut remplacer les espaces de la requêtes par des "_", par exemple pour scrapper les images de "bar chart", on lancera la commande suivante:

```
python3 google-scrapper_2.0 bar_chart
```
Ce script nous permet de récupérer environ 400 images exploitables par classe et d'avoir des images correctement nommées pour faire tourner nos algorithmes.

## Traitement d'image

Le fichier <b>loadData.py</b> permet d'effectuer un traitement préliminaire sur la base de données. Il contient la fonction "resize_dataset" qui prend en entrée trois arguments :
- La dossier contenant l'ensemble de la base de données, la taille d'image désirée ainsi que la largeur
- Il charge chaque image de la base de données et compare son ratio au ratio désiré : si le ratio ne convient pas, on ajoute du blanc à droite ou en bas de l'image afin de ne pas déformer l'image originale lors du changement d'échelle
- On effectue le changement d'échelle de l'image pour obtenir les dimensions voulues
- L'image est enregistrée au format ".jpg" dans le dossier data

Cela nous permet d'avoir un ensemble d'images au bon format en entrée de notre réseau de neurones.

## Comment utiliser nos scripts ?

Le fichier <main.py> permet de lancer les scripts : 
- <b>loadData.py</b> traite les images brutes et les redimensionnent à la taille voulue en JPG.
- <b>build_dataset.py</b> sérialise les images de train-validation et leurs labels correspondant dans un fichier Pickle.
- <b>reseau.py</b> définit les différents modèles de réseaux de neurones que l'on peut choisir dans le fichier <b>settings.py</b>
- <b>neuralnetwork.py</b> permet d'entraîner le modèle choisit à partir des données issues du fichier pkl et enregistre le modèle entraîné.
- <b>prediction.py</b> utilise le modèle entraîné sur un ensemble test créé au préalable et enregistre les métriques dans un fichier JSON. 
- <b>result.py</b> permet d'initialiser la structure de notre fichier JSON, avec notamment tous les paramètres choisis pour le lancement des scripts.

## Auteurs

Arnal Marc  
Brugière Arnaud  
Guery Luca  
Kraemer Louis  
Martin-Delahaye Alexis
