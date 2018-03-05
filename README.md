# DatasetVis

## Le projet

Ce répertoire permet à partir d'une base de données d'images contenant 3 classes différentes d'entraîner un modèle de réseaux de neurones convolutionnels et de le tester sur une base test.

À partir d'une base de données contenant 3 classes d'images de tailles et de formats quelconques, on redimensionne chaque image à la taille sizexsize et on convertit en JPG. 

On crée deux dossiers :
- /data contient x% des images pour entraîner le réseau de neurones convolutionnels
- /test contient (1-x)% des images pour tester le modèle finale enregistrée

À partir du dossier /data, on sérialise nos images de 'train' & 'validation' ainsi que leur labels respectifs dans un fichier pkl. Celui-ci sera lu pour entraîner le réseau de neurones. 
À la fin de l'entraînement, qui peut être plus ou moins long suivant les paramètres que vous avez choisi, le modèle est enregistré.

Il est ensuite utilisé automatiquement sur le dossier /test crée ultérieurement et en ressort une matrice de confusion.

Comme chaque variable intermédiaire est enregistrée (modèle CNN entraînée, dataset dans le fichier pkl, dossiers /data et /test) il est possible de les réutiliser sans réaliser toutes les étapes.

Dans le fichier <b>settings.py</b> il vous est possible de <b>modifier les différents paramètres</b> clés utilisés dans nos scripts Python, comme la taille des images, le part de l'ensemble test, etc.
 
## Lancement

Dans le terminal, placez vous dans le dossier que vous venez de clôner.
Pour lancer le script, tapez :
```
python3 main.py
```

## Scrapping

Nous utiliserons le script issu du git image-scrapers afin de peupler notre 
base de données. Celui-ci permet de récupérer des images issues de google et
fournit un JSON associé.

## Traitement d'image

Le fichier loadData.py permet d'effectuer un traitement préliminaire sur la base de données. Il contient la fonction "resize_dataset" qui prend en entrée trois arguments :
- La dossier contenant l'ensmble de la base de données, la taille d'image désirée ainsi que la largeur
- Il charge chaque image de la base de données et compare son ratio au ratio désiré : si le ratio ne convient pas, on ajoute du blanc à droite ou en bas de l'image afin de ne pas déformer l'image originale lors du changement d'échelle
- On effectue le changement d'échelle de l'image pour obtenir les dimensions voulues
- L'image est enregistrée au format ".jpg" dans le dossier data

Cela nous permet d'avoir un ensemble d'images au bon format pour notre réseau de neurones.

## Auteurs

Arnal Marc  
Brugière Arnaud  
Guery Luca  
Kraemer Louis  
Martin-Delahaye Alexis
