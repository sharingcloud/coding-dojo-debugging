# Section 1 - Le logging

Avant de commencer à aborder le debugging, on va vite fait voir les autres façons classiques de faire.

## 1. La classique - le printf-debugging

Ce nom vient du langage C et de l'utilisation de `printf` (équivalent en gros de la fonction `print` de Python) qui permet facilement et rapidement d'afficher quelque chose sur la sortie standard.

```python
>>> print("Coucou, la sortie standard")
Coucou, la sortie standard
```

C'est simple, ça marche bien, et c'est complètement ingérable quand y'a 15.000 appels partout sur une centaine de fichiers.

Comme cette technique devrait être plutôt bien maîtrisée, on va directement monter d'un cran grâce au module Python `logging`.

## 2. La meilleure solution - les loggers

- Documentation officielle: [https://docs.python.org/3.6/library/logging.html](https://docs.python.org/3.6/library/logging.html)
- Logging HOWTO: [https://docs.python.org/3.6/howto/logging.html](https://docs.python.org/3.6/howto/logging.html)
- Logging cookbook: [https://docs.python.org/3/howto/logging-cookbook.html](https://docs.python.org/3/howto/logging-cookbook.html)

Voici un conseil: a moins qu'il y ait besoin de formatter du texte d'une certaine façon ou de faire un outil en ligne de commande avec interactions (donc scripts, apps CLI ou commandes custom Django), n'utilisez plus `print`, car il y a beaucoup mieux.

La technique est de passer par les loggers, configurable à l'aide du module `logging` de Python, qui permet de structurer les différentes entrées de log réparties dans toutes les sources d'un projet.

Il y a 5 niveaux de log standard, par ordre d'importance:

- **DEBUG** - Pour les messages verbose avec un maximum d'information
- **INFO** - Pour les infos ponctuelles mais utiles
- **WARNING** - Pour les warnings, avec par exemple des warnings de dépréciation
- **ERROR** - Pour les erreurs récupérables
- **CRITICAL** - Pour les erreurs irrécupérables

Pour écrire dans le logger standard, il suffit de faire:

```python
import logging

# Message d'info
logging.info("Je suis une info")
# Message d'erreur
logging.error("Je suis une erreur")
```

Un exemple complet est dans le dossier `examples/1-logging`. Pour lancer le script, il faut exécuter:

```bash
python examples/1-logging/main.py
```

La sortie devrait donner ça:

```text
[__main__] INFO 2019-02-07 22:16:50,779 Je démarre le script...
[counter] INFO 2019-02-07 22:16:50,779 Je vais compter de 1 à 2
[counter] DEBUG 2019-02-07 22:16:50,780 Je dis 0...
[counter] DEBUG 2019-02-07 22:16:50,780 Je dis 1...
[counter] DEBUG 2019-02-07 22:16:50,780 J'ai fini de compter !
[spammer] DEBUG 2019-02-07 22:16:50,780 Je spam le debug !
[spammer] INFO 2019-02-07 22:16:50,780 Je spam l'info !
[counter] ERROR 2019-02-07 22:16:50,780 Je ne sais pas compter les nombres inférieurs à 1
[spammer] ERROR 2019-02-07 22:16:50,781 Je spam l'erreur !
[counter] INFO 2019-02-07 22:16:50,781 Je vais compter de 1 à 10
[counter] DEBUG 2019-02-07 22:16:50,781 Je dis 0...
[counter] DEBUG 2019-02-07 22:16:50,781 Je dis 1...
[counter] DEBUG 2019-02-07 22:16:50,781 Je dis 2...
[counter] DEBUG 2019-02-07 22:16:50,781 Je dis 3...
[counter] DEBUG 2019-02-07 22:16:50,782 Je dis 4...
[counter] DEBUG 2019-02-07 22:16:50,782 Je dis 5...
[counter] DEBUG 2019-02-07 22:16:50,783 Je dis 6...
[counter] DEBUG 2019-02-07 22:16:50,783 Je dis 7...
[counter] DEBUG 2019-02-07 22:16:50,784 Je dis 8...
[counter] DEBUG 2019-02-07 22:16:50,785 Je dis 9...
[counter] DEBUG 2019-02-07 22:16:50,785 J'ai fini de compter !
[__main__] INFO 2019-02-07 22:16:50,786 J'ai fini le script...
```

C'est plutôt bien structuré, avec *le module en cours*, *le niveau de message*, *la date*, et enfin *le contenu du message*. C'est quand même plus pratique qu'un appel à `print`.

Pour que tous ces messages soient affichés, il faut au préalable configurer le système de logging, soit avec la fonction `basicConfig`, soit la fonction `config.dictConfig`. C'est cette deuxième fonction qui est utilisé dans Django.

Pour mieux comprendre, regardez le fichier `config.py` du projet:

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "[%(name)s] %(levelname)s %(asctime)s %(message)s"},
        "simple": {"format": "[%(name)s] %(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "DEBUG"},
        "__main__": {"handlers": ["console"], "level": "INFO"},
    },
}
```

Prenez le temps de comprendre ce dictionnaire à l'aide du [logging cookbook](https://docs.python.org/3/howto/logging-cookbook.html), mais en gros la section la plus importante est la section `loggers`.

## Petit exercice pratique

Pour voir si vous avez compris, voici quelques petites tâches à réaliser:

- Ajoutez un log `INFO` à l'entrée et la sortie de la fonction `count_and_spam` du fichier `counter.py`.
- Sans toucher aux entrées de log, seulement en changeant la configuration:
    - Cachez tous les messages du module `spammer`.
    - Cachez les messages de plus basse importance qu'`INFO` sur le module `counter`.
    - Ne laissez passer que les messages `ERROR` sur tous les modules.

Si vous êtes OK sur ces exercices, on passe à la suite !

<p style="float: left">
    <a href="./0-INTRODUCTION.html">< Introduction</a>
</p>

<p style="float: right">
    <a href="./2-DEBUGGING-CLI.html">Debugging d'une application CLI ></a>
</p>