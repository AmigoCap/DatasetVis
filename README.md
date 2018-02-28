# DatasetVis

## Lancement

Pour lancer le script, tapez 
```
python3 main.py <chemin/vers/la/base/de/données>
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
