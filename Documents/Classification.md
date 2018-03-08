# Etat de l’art : méthode de classification

## DEFINITION :

**Classification :** Dans une classification, la variable cible est qualitative. Il s’agit de créer des catégories. Elle s’oppose en cela à la régression dont la variable cible est quantitative.

## DETAIL DE L’ETAT DE L’ART


Methode de classification 
Apprentissage supervisé ou non supervisé? 
Classification binomiale ou multiclasses?

**CLASSIFICATION NAIVE BAYESIENNE** 
Supervisé Multiclasse

**_Principe :_** La méthode considère le vecteur x des valeurs des variables prédictives comme une variable aléatoire dont la distribution dépend de la classe. La classification est réalisée à partir d’un classifieur bayésien qui est soumis à l’apprentissage. Le but de l’apprentissage pour le classifieur bayésien est d'estimer la
probabilité a priori des classes et d'estimer la densité de probabilités des classes.

**_Avantages :_** L’efficacité et la simplicité de l’algorithme, et le peu de données nécessaires pour l’entrainer.

**_Inconvénients :_** On est obligé de supposer que les variables prédictives ont des probabilités conditionnelles indépendantes.
Exemple d’application : La classification naïve Bayésienne permet par exemple de déterminer si une personne est un homme ou une femme à partir de son poids et de ses mensurations à partir de données d’entraînement.

**_Exemple d’application :_** Pour déterminer a partir d'un jeu de données de taille et de poids si une personne a davatange d'être un homme ou une femme

**LES MACHINES A VECTEURS SUPPORTS** Non supervisé Binomial
**_Principe :_** La méthode consiste à trouver un hyperplan optimal qui sépare les deux catégories. Cet hyperplan doit avoir la distance la plus faible possible avec chacune
des catégories. Dans chaque catégorie, les points les plus proches de l’hyperplan sont appelés les vecteurs supports. L’espace entre les deux catégories est appelé la
marge.

**_Avantages :_** Ces algorithmes fonctionnent sur des problème complexes, ie non-linéaire et/ou avec beaucoup de dimension
**_Inconvénients :_** L’algorithme est souvent moins performant que les forêts aléatoires et passe difficilement à l’échelle


**_Exemple d’application :_** En médecine, la détection du cancer du sein par les machines à vecteurs supports conduit à un taux d’erreur de seulement 3%.

**LES ARBES DE DECISIONS** Supervisé Multiclasse
**_Principe :_**
La méthode consiste à classer une observation au moyen d’une succession de tests concernant les valeurs des variables prédictives. Chaque test est représenté par
un nœud de l’arbre. Chaque branche correspond à une réponse possible à la question posée. La classe de la variable est déterminée par la feuille à laquelle parvient
l’observation à l’issue de la suite de tests.
La phase d’apprentissage consiste donc à trouver les bons tests pour classer correctement les observations par rapport à leur valeur pour la variable cible.
L’objectif est le suivant : les feuilles doivent être homogènes en ne contenant que les observations appartenant à une seule et même classe
**_Avantages :_** Fonctionne sur des problèmes complexe (non-linéaire, multiclasse). Peu de préparation de données nécessaires.
**_Inconvénients :_** Risque important de surapprentissage. Le critère du premier nœud influe énormément l’ensemble du modèle de prédiction
**_Exemple d’application :_** Les arbres de décisions sont utilisés pour programmer les robots intelligents du jeu d’échec.


**LES FORÊTS ALEATOIRES** Supervisé Multiclasse
**_Principe :_** A partir d’un échantillon initial de N observations dont chacune est décrite par p variables prédictives, on crée artificiellement B nouveaux échantillons de
même taille N par tirage avec remise. On entraine alors B arbres de décisions différents
Parmi les p variables prédictives, on n’en utilise qu’un nombre m<p choisies au hasard. Elles sont alors utilisées pour faire la meilleure segmentation possible.
L’algorithme combine plusieurs algorithmes faibles (les B arbres de décision) pour en constituer un plus puissant en procédant par vote : pour classer une nouvelle
observation, on la fait passer par les B arbres et on sélectionne la classe majoritaires parmi les B prédictions.
**_Avantages :_** Possède les avantages des arbres de décision
**_Inconvénients :_** Peu intelligible, complexe à comprendre et à implémenter.
**_Exemple d’application :_** Ce sont les mêmes applications que les decisions tree. Les forêts aléatoire sont particulièrement plus performantes dans certains domaines
de pointes. Par exemple, la squelettisation numérique de personne.

**LES RESEAUX DE NEURONES** Non supervisé Multiclasse
**_Principe :_** Les réseaux de neurones consistent en un réseau orienté composé de neurones artificiels organisés en couches.
Les neurones d’une couche donnée sont liés à tous les neurones de la couche précédente et de la couche suivante par des relations pondérées. De ces poids dépend
le comportement du réseau, et leur adaptation au problème considéré et l’objectif de la phase d’apprentissage. Chaque neurone a une sortie qui est obtenue par
l’application d’une fonction non linéaire de la somme pondérée des entrées, qui sont elles mêmes les sorties des neurones de la couche précédente. Afin de calculer
le vecteur poids pour chaque neurone, des algorithmes de rétropropagation ont été développés
**_Avantages :_** Les réseaux de neurones permettent de traiter des problèmes de classification non linéaires complexes.
**_Inconvénients :_** Le choix de la structure du réseau de neurone est compliqué. Il existe un risque de tomber dans un minimum local lors de l’apprentissage.
**_Exemple d'application :_** Les réseaux de neurones sont par exemple utilisé dans la bourse pour identifier les tendances. Une explication est donnée par dans le papier
suivant : https://dumas.ccsd.cnrs.fr/dumas-01064660/document
```
## BIBLIOGRAPHIE :

[http://r.gmum.net/samples/svm.basic.html](http://r.gmum.net/samples/svm.basic.html)

[http://dspace.univ-tlemcen.dz/bitstream/112/4013/1/classification%20des%20tumeurs%20du%20cancer%20du%20sein%20par%20approche%20SVM](http://dspace.univ-tlemcen.dz/bitstream/112/4013/1/classification%20des%20tumeurs%20du%20cancer%20du%20sein%20par%20approche%20SVM)

https://www.math.univ-toulouse.fr/~besse/Wikistat/pdf/st-m-app-svm-old.pdf

[http://georges.gardarin.free.fr/Surveys_DM/Survey_SVM.pdf](http://georges.gardarin.free.fr/Surveys_DM/Survey_SVM.pdf)

[http://dpt-info.u-strasbg.fr/~nicolas.lachiche/CNAM_NFE212/arbresDecision.pdf](http://dpt-info.u-strasbg.fr/~nicolas.lachiche/CNAM_NFE212/arbresDecision.pdf)

[http://www.grappa.univ-lille3.fr/polys/apprentissage/sortie004.html](http://www.grappa.univ-lille3.fr/polys/apprentissage/sortie004.html)


https://www.lri.fr/~antoine/Courses/ENSTA/Tr.%20Cours%20ID3x9.pdf

https://kevinbinz.com/2015/02/26/decision-trees-in-chess/

[http://www.univ-orleans.fr/log/Doc-Rech/Textes-PDF/1997-1.pdf](http://www.univ-orleans.fr/log/Doc-Rech/Textes-PDF/1997-1.pdf)

https://www.math.ens.fr/enseignement/telecharger_fichier.php?fichier=

https://cran.r-project.org/doc/Rnews/

https://dumas.ccsd.cnrs.fr/dumas-01064660/document
