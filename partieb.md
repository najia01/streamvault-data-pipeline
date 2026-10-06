PARTIE B ONTOLOGIE

Q28 Observer les données réelles

Les champs communs présents dans les 2 types sont : \_id, title, year, genre, directors, type.
Les champs spécifiques à chacun sont :

- pour les films: cast, imdb
- pour les livres: pagesNumber, note

Le champ year peut poser des problèmes d'incohérence car il peut parfois être stocké sous forme de string mais aussi sous forme d'integer ce qui peut poser des problèmes lors du mapping OWL.

Les champs imdb ou cast peuvent eux être en valeurs manquantes .
