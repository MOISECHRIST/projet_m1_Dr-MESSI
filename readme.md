# Service Utilisateur 

## Membre du groupe

| N | Nom et prenom | Role |
|---|---------------|------|
| 1 |   Dr MESSI Thomas	            |  Encadreur    |
| 2 |     EPADIE EBOUANGUE Cédric          |   Étudiant   |
| 3 |     NDOMBOU KAMDEM Jerry          |    Étudiant  |
| 4 |     MEKA Moise Christian Junior          |   Étudiant   |


## Description du service 

Le service utilisateur est chargé de la création des utilisateurs (informations détaillées sur les utilisateurs), il sera aussi chargé de la connexion\
au système et de la gestion des utilisateurs (suppression de compte, modification du compte et des informations).\
Une fois qu'un utilisateur ait créé un compte, ce service informera les autres services sur la creation du compte. Il envera ainsi les données\
suivantes :
- Person.pk,
- Si l'utilisateur est un prestataire, il ajoutera les informations sur les services qu'il propose,

De plus il partagera avec les autres services la liste de tous les services proposés par les prestataires. Il mettra a jour cette liste en :
- Ajoutant un nouvel element,
- En suppriment un element supprimé

Pour eviter la duplication des données, seul les pk seront partagé. 

Retrouvez ci joint le diagramme de classe de ce service :

<img height="600" src="Diagramme Classe Service Utilisateur.drawio.png" title="Diagramme_classe" width="1000"/>