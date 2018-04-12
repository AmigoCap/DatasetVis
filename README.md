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

#Prise en main

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

Afin d'installer l'ensemble des packages nécessaires au fonctionnement du script, installer le module pip ([Page officielle](https://pypi.python.org/pypi/pip))  et exécuter la commande suivante :  

```
pip3 install -r requirements-scraper.txt
```

Afin d'utiliser le script de scrapping, il faut:
- installer le driver chrome correpondant à la version du navigateur GoogleChrome présente sur l'ordi ([Page officielle](https://chromedriver.storage.googleapis.com/index.html))
- modifier la ligne 24 du script et renseigner l'emplacement du driver

```
browser = webdriver.Chrome(executable_path=r'C:/Users/Desktop/chromedriver.exe')
```

Après modification du script, il faut remplacer les espaces de la requêtes par des "\_", par exemple pour scrapper les images de "bar chart", on lancera la commande suivante:

```
python3 google-scrapper_2.0 bar_chart
```

Ce script nous permet de récupérer plusieurs centaines d'images exploitables par classe et d'avoir des images correctement nommées pour faire tourner nos algorithmes.

## Traitement d'image

Le fichier <b>loadData.py</b> permet d'effectuer un traitement préliminaire sur la base de données. Il contient la fonction "resize_dataset" qui prend en entrée trois arguments :
- La dossier contenant l'ensemble de la base de données, la taille d'image désirée ainsi que la largeur
- Il charge chaque image de la base de données et compare son ratio au ratio désiré : si le ratio ne convient pas, on ajoute du blanc à droite ou en bas de l'image afin de ne pas déformer l'image originale lors du changement d'échelle
- On effectue le changement d'échelle de l'image pour obtenir les dimensions voulues
- L'image est enregistrée au format ".jpg" dans le dossier data

Cela nous permet d'avoir un ensemble d'images au bon format en entrée de notre réseau de neurones.

## Paramètres de contrôle du fichier settings.py

Avant de lancetr le script, il est nécessaire de choisir les paramètres voulus dans le fichier <b>settings.py</b>.

Voici en détail les rôle de chaque paramètre :
- databasePath =: emplacement du fichier d'images sources
- size : choix de la résolution de l'image (Attention, au delà de 64x64, cela devient très couteux pour les machines habituelles)
- offset_test : pourcentage d'image prise pour tester le modèle (Par défaut à 0.1)
- offset_train_val : pourcentage d'image du dossier d'entraînement, prise pour l'apprentissage. Le reste sert à la validation (Par défaut à 0.8)
- nb_epoch nombre d'itérations, ie nombre de fois que chaque image va passer dans le réseau
- batch_size : nombre d'images qui passent en même temps dans le réseau
- learning_rate : taux d'apprentissage. Par défaut, fixé à 0.001
- strictness_class : ce paramètre permet de classifier plus sérieusement. En effet, il n'attribuera une image à une classe qu'uniquement si son score est supérieure à ce chiffre x score du hasard (i.e. supérieur à strictness_class * 1/classes_number)
- nb_filter nombre de filtre pour le réseau 1 dans la couche initiale (attention, ne fonctionne que si le réseau 1 est choisi. Pour les autres réseaux, ce paramètre est fixé à 32)
- filter_size : taille / résolution du filtre
- reseau : choix du réseau. Allant de 1 à 5, les structures des réseaux sont disponibles dans le fichier reseau.py


## Comment utiliser nos scripts ?

Le fichier <main.py> permet de lancer les scripts :
- <b>loadData.py</b> traite les images brutes et les redimensionnent à la taille voulue en JPG.
- <b>build_dataset.py</b> sérialise les images de train-validation et leurs labels correspondant dans un fichier Pickle.
- <b>reseau.py</b> définit les différents modèles de réseaux de neurones que l'on peut choisir dans le fichier <b>settings.py</b>
- <b>neuralnetwork.py</b> permet d'entraîner le modèle choisit à partir des données issues du fichier pkl et enregistre le modèle entraîné.
- <b>prediction.py</b> utilise le modèle entraîné sur un ensemble test créé au préalable et enregistre les métriques dans un fichier JSON.
- <b>result.py</b> permet d'initialiser la structure de notre fichier JSON, avec notamment tous les paramètres choisis pour le lancement des scripts.


# Pour une meilleure compréhension

## Construction de la base de données

### Scrapping

La première partie de notre travail consiste en la collecte de visualisations de données, par exemple des nuages de points ou des histogrammes, afin de constituer une base de données d’images suffisamment grande pour entraîner un modèle de réseaux de neurones convolutionnels et le tester.

Grâce au script Python <b>google-scrapper_2.0.py</b> inspiré du git image-scrapers, il est possible de récupérer des centaines d’images issues d’une requête sur Google Image.
En effet, ce script permet de lancer un driver de Google Chrome, de réaliser la requête souhaitée sur Google Image et de scroller automatiquement jusqu’en bas de la page afin de charger toutes les images possibles pour pouvoir ensuite les télécharger avec un JSON associé, contenant la provenance de l’image notamment. Ceci nous permet de garder une trace des sources utilisées. Nous avons apporté des modifications au script initial afin de renommer automatiquement les images téléchargées avec leur classe et un identifiant unique.


Ainsi, si on souhaite récupérer des centaines d’images de “bar chart”, on exécute le script Python comme suit, en prenant soin d’ajouter les “_ ” à la place des espaces :

```
python3 google-scrapper_2.0 bar_chart
```

On obtient alors des centaines d’images nommées suivant l’exemple suivant
“bar_chat_1.jpg”. Ceci nous sera très utile pour associer à chaque image sa classe. Nous avons utilisé ce script pour collecter des images des dix classes sélectionnées. Les résultats se trouvent dans un dossier situé dans le répertoire du script scrapper, dont le nom est dataset. Chaque sous-dossier de dataset correspond au résultat d’une requête.
Sur le git de notre projet DatasetVis, il est possible de suivre un tutoriel pour pouvoir utiliser ce script de scrapping.

Il faut ensuite nettoyer ce premier jeu de données pour obtenir une base de données propre et exploitable.


### Nettoyage du jeu de données

Une fois les images des dix classes téléchargées, il faut nettoyer ce jeu car il comporte des images illisibles, et des images qui ne correspondent pas à la requête réalisée, ou alors comportant trop de bruit. Voici les critères que nous avons utilisé pour exclure les images non conformes. Ils sont issus de l’expérience. Cette liste n’est pas exhaustive mais correspond aux cas qui reviennent le plus souvent.

Pour les dix catégories, les images que nous avons retirées, en plus de celles qui n’étaient pas lisibles, valident un ou plusieurs critères suivants :

-	Légende / bruit représentant une part trop importante de l’image
-	Graphique regroupant 2 catégories (ex : à la fois bar et line chart)
-	Graphique trop simpliste (type icône ou vecteur)
-	Graphique tracé manuellement

Nous avons volontairement laissé du bruit dans nos données, introduit par du texte par exemple, des fonds hétérogènes ou encore des graphiques en trois dimensions. On obtient après nettoyage manuel au moins 300 images exploitables par classe. Notre dossier contient finalement plus de 3500 images. Certaines classes regroupent plus de 500 photos, d’autres près de 400. Nous construisons alors un dossier comprenant un nombre semblable d’image pour chaque catégorie : trois catégories bien renseignées (1350 images), six catégories (2100 images) et 10 catégories (3200 images).

Il est nécessaire de noter que ce nombre reste faible pour obtenir de très bons résultats. En effet, si l’on prend l’exemple de la base de données MNIST faite pour essayer de classer les chiffres manuscrits, la base données comporte 70 000 images. On se rend bien compte qu’il est très compliqué de constituer une telle base de données dans le temps imparti, et avec les ressources à disposition. Les résultats obtenus seront donc à nuancer au regard de ce point.

### Préparation des données pour les phases d’entraînement et de test

Une fois la collecte réalisée et le jeu de données propre, l’étape suivante consiste à la préparation de nos images pour l’entraînement du réseau de neurones.

Dans un premier temps, il est nécessaire de redimensionner toutes les images au même format. Le fichier <b>loadData.py </b>le permet. Il suffit de modifier dans <b>settings.py</b> le chemin vers le dossier contenant les images, ainsi que la largeur et la hauteur souhaitées.

Le script contient la fonction "resize_dataset" qui prend en entrée ces trois arguments, puis procède comme suit :

- Il charge chaque image de la base de données et compare son ratio au ratio désiré : si le ratio ne convient pas, on ajoute du blanc à droite ou en bas de l'image afin de ne pas déformer l'image originale lors du changement d'échelle
- On effectue le changement d'échelle de l'image pour obtenir les dimensions voulues
- L'image est enregistrée au format <b>".jpg"</b> dans le dossier <b>data</b>
- On obtient alors un nouveau dossier <b>/data</b> dans le même répertoire, il contient les images redimensionnées au format JPG.

Dans un second temps, il faut préparer le jeu de données pour l’entraînement et le test. Grâce au script <b>build_dataset.py</b>, on sépare l’ensemble d’images contenu dans le répertoire data en :
- Un ensemble test qui sera utilisé plus tard pour tester le modèle et calculer des métriques, créé dans le répertoire /test.
- Et un ensemble d’entraînement-validation qui va être sérialisé dans un fichier Pickle <b>dataset.pkl</b>

Le pourcentage est à modifier dans le fichier settings.py, il est de 10% par défaut pour l’ensemble test, donc 90% pour l’ensemble d’entrainement. Dans cet ensemble d’entrainement, une partie est allouée à l’apprentissage, l’autre à la validation.

Il est à noter que dans le dossier parent les images sont mélangées avant de procéder à la séparation et nous nous assurons que la quantité d’image pour chaque classe dans les deux dossiers créés reste proche afin d’éviter la surreprésentation d’une classe.

Le fichier Pickle en sortie du script contient :

- Le tableau des images d’entraînement ainsi que le tableau des labels respectifs pour chaque image
- Le tableau des images de validation croisée ainsi que le tableau des labels respectifs pour chaque image

Une image correspond à un tableau de pixels et son label respectif à un tableau de 0 contenant un seul 1 suivant l’indice correspondant à la classe de l’image. Par exemple, [0,0,1] si notre BDD contient 3 classes et que l’image de l’exemple appartient à la 3ème classe.

Ces quatre objets sont sérialisés pour pouvoir être lus en entrée du réseau de neurones. Il est possible de modifier le pourcentage pour chacun des deux ensembles d’images. Par défaut, 20 % des images sont pour la validation et 80% pour l’entraînement.

## Choix des métriques de sortie

#### Valeurs de sortie
En sortie du réseau, nous obtenons un vecteur de probabilité d’appartenance à chaque classe. La probabilité la plus grande détermine la classe à laquelle est attribuée l’image.
Il faut alors analyser ces attributions.

#### Matrice de confusion
Cette matrice classe recoupent les prédictions avec les valeurs réelles. Sur la diagonale (True Positive) se situent les images bien classées. Cela permet d’avoir une vision de la précision du modèle.

#### Accuracy
Cette valeur calcule le nombre de d’instances bien classées. Elle permet de se rendre compte de la validité du modèle. Elle est égale à la somme des valeurs sur la diagonale divisée par la somme de tous les éléments de la table.

#### Recall ou rappel
Cette valeur calcule pour chaque classe le nombre d’instances bien classées sur le nombre d’instances de la classe (True Positive / Total d’instances la classe). Cela permet de se rendre compte de la faculté du modèle à trouver ou non les éléments d’une classe.
Le rappel total d’un modèle et la somme des rappels de chaque classe divisée par le nombre de classes.

#### Précision
Cette valeur calcule pour chaque classe le nombre d’instances bien classées sur le nombre d’instances attribuées à cette classe (True Positive / Total des prédictions de cette classe). Cela permet de se rendre compte de la pertinence du modèle dans la classification, i.e. à chaque fois qu’il prédit une classe, quelle est la chance pour que cette prédiction soit bonne.
La précision totale d’un modèle et la somme des précisions de chaque classe divisée par le nombre de classes.

#### Sévérité du modèle (strictness class)
Ce paramètre est un paramètre additionnel qui nous permet de classer mieux que le hasard. En effet, il n’attribue une instance à une classe que si cette dernière a une probabilité x fois supérieur au hasard (1/nombre de classes). Dans notre modèle nous avons pris 1,3. Ce choix est arbitraire mais marque la volonté de classer de plus sûrement que le hasard. Si tel n’est pas le cas, cette instance est attribuée à la classe ‘uncategorized’, qui regroupe toutes les instances pour lesquelles aucune classe ne se démarque.


## Construction de notre modèle final

### Choix des paramètres

#### Itérations

Nous avons fixé le nombre d’itérations à 125 pour les différents réseaux. Nous pouvons justifier ce choix en visualisant l’évolution de la perte (loss) et de la précision (accuracy) lors de la phase d’apprentissage. Les courbes représentatives (visualisable dans le rapport) ont bien atteint leurs asymptotes. On peut donc se satisfaire de ce nombre.

#### Taux d'apprentissage

Le taux d’apprentissage permet de définir la vitesse de convergence du modèle. Il est essentiel qu’il soit adapté puisque sinon le modèle ne peut converger, ou converge vers un résultat non optimal.

De la même manière que pour le nombre d'itération, nous avons comparé différents taux. Pour un taux faible (0.0001), cela ne converge pas rapidement, pour un taux trop haut (0.01) cela ne converge pas.

#### Taille du filtre

Le filtre permet de déterminer la taille de la tuile. Via un filtre de taille 1, le réseau traitera tous les pixels indépendamment les uns des autres.
A partir du réseau 1, nous avons comparé les résultats pour différentes tailles de filtre. Il faut noter que la puissance de nos machines ne nous permet pas d’utiliser des filtres de tailles trop importantes. En effet, pour un filtre de taille 5x5, et un nombre de filtres égal à 32 au sein d’une unique couche de convolution, il y a 5x5x32 paramètres à calculer, soit 800 paramètres. Sur le réseau tout entier, cela fait plus de 10 000 paramètres à calculer à chaque itération. Il devient presque donc impossible pour nos machines de les faire tourner sur des bases de données comprenant plus de 3 catégories (donc plus de 2000 images). D’autant plus que si l’on augmente la résolution de l’image, les calculs seront d’autant plus longs.

Nous constatons que les résultats des différentes simulations ne suivent pas de logique claire : selon le nombre de classe, des filtres de taille 3x3 peuvent être plus ou moins pertinents.
Nous choisirons par la suite le meilleur modèle selon que l’on veut trouver sur trois classes (taille : 7x7), six classes (taille 3x3) ou 10 classes (taille 3x3).

Les graphes sont visualisables dans le rapport.

#### Taille de l'image

La résolution de l’image va influencer les résultats attendus. On peut par exemple se convaincre qu’un modèle différenciera mieux des images de bonne qualité que des images de mauvaise qualité, où il un nuage de point et un diagramme en ligne peuvent être peu différenciables.

Le test effectué avec le premier réseau montre qu’une résolution de 64x64 donne de meilleurs résultats. Cela se retrouve pour tous les réseaux, et pour les filtres de taille 3x3 et 5x5. Cependant, il faut noter que, pour certains réseaux avec certains paramètres, on peut trouver  de plus mauvais résultats avec une résolution de 128x128 qu’avec une résolution de 64x64.


#### Influence du réseau

Nous avons construit plusieurs réseaux pour essayer de comprendre l’influence du réseau sur les résultats. L’architecture des différents réseaux est détaillée dans la partie précédente.

Nous constatons que les résultats dépendent encore une fois du nombre de classes.

Pour conclure, il est compliqué de prédire quel réseau et quels paramètres seront le mieux, avant de les tester sur les bases de données. De manière empirique, nous choisissons donc les modèles suivants :



|   Paramètres  |    3 classes    |    3 classes    |    10 classes   |
| ------------- | : ------------: | : ------------: | : -----------:  |
| reseau        |        1        |        3        |         1       |
| filter_size   |        7        |        3        |         3       |
| size (image)  |        64       |        64       |         64      |
| learning_rate |        0.001    |        0.001    |         0.001   |
| nb_epoch      |        125      |        125      |         125     |
| Accuracy      |        91,60%   |        81,60%   |         71,03%  |

|        | 3 classes | 6 classes | 10 classes |
|--------|----------:|----------:|------------|
| Réseau |       ayj |         k | j          |
| kd     |      hjdi |           | poj        |
|        |           |           |            |


Bien entendu, pour généraliser le modèle, nous pouvons garder que le modèle à 10 classes, mais la précision sera plus faible. Si l’on est certain d’avoir un visuel de datavisualization dans les modèles à six classes ou trois classes, nous pourrons utiliser les modèles restreints qui apportent de meilleures performances.

## Test d'une images

API ou unit test
Explication radar (cf rapport)


## Auteurs

Arnal Marc  
Brugière Arnaud  
Guery Luca  
Kraemer Louis  
Martin-Delahaye Alexis
