# Introduction

Bienvenue sur cette première session de Coding Dojo à propos du debugging !

## Prérequis

- Python 3 et pip (au moins 3.6)
- Un terminal

## 1. Préparation

Pour commencer, on va installer tout ce qu'il faut.

Pour utiliser des paquets Python sans écraser l'environnement système, on va utiliser un **virtualenv**.
Un *virtualenv* est une sorte d'installation Python *indépendante*, avec ses propres paquets.

Voici ce qu'il faut taper:

```bash
pip install virtualenv
```

Ensuite, la création de ce virtualenv:

```bash
virtualenv -p python3 ./venv
```

Une fois le virtualenv crée, il faut l'activer:

```bash
# Pour Windows, sous Powershell
./venv/Scripts/activate.ps1
# Pour Windows, sous cmd
./venv/Scripts/activate.bat
# Pour Linux
source ./venv/bin/activate
```

Une fois dans le virtualenv, le *prompt* de la console va changer avec le texte `(venv)` devant.

```bash
# Exemple avec Powershell
(venv) PS C:\.....> _
```

D'ici, on peut installer les paquets nécessaires:

```bash
pip install -r requirements.txt
```

Pour être sûr que tout est bon, on peut essayer d'ouvrir une session `ipython`:

```bash
ipython
```

S'il s'ouvre et qu'un `In [1]` apparaît, c'est good !

<div style="float: right">
    <a href="./1-LOGGING.html">Prochaine étape: le logging ></a>
</div>