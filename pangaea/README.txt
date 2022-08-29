- La directory input_converter contiene due script

  - input_converter.py parte dalla rappresentazione JSON per generare delle
    annotazione che Pangaea e' in grado di analizzare (usato con il JSON di
    Tutored per controllare il corretto funzionamento del convertitore).

  - cromlech-sc2pangaea_input_converter.py parte dagli input di cromlech e di
    pangaea per costruire le annotazioni che Pangaea e' in grado di
    analizzare.

- La directory parser/annotations-parser contiene un file run.js che permette
  di leggere le annotazioni e trasformarle in input per il problema di
  programmazione lineare.

  - Creare una directory dentro repository con e la stessa struttura delle
    directory di esempio e inserire le annotazione (le annotazioni vanno
    dentro una directory src e devono avere estensione .ts)

- Lanciare il problema di ottimizzazione con il file dat ottenuto
  dall'annotation-parser

- A questo punto, denominare il file dei risultati 'result.csv' e rilanciare
  il programma run.js. Questo popolera' i file json all'interno della
  directory visualization

- Dentro la directory visualization, invocare il file
  create_microservices-data.py, che copia il contenuto dei file json e crea il
  file microservices-data.js.  Questo file puo' essere invocato per conoscere
  i costi della decomposizione, inoltre il file view.html permette di
  visualizzare la decomposizione ottenuta.

- Per convertire l'output di Pangaea in output (e costi) di Cromlech, copiare
  il file 'microservices.json' dentro alla directory 'output_converter'.
  Questo legge il file di descrizione yaml di cromlech e i risultati json di
  Pangaea e produce i risultati.

*** TODO ***

- L'output converter non funziona ancora correttamente perche' non considera i
  microservizi senza operazioni
