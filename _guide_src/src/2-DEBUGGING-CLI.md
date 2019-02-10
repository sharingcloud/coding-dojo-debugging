# Section 2 - Le debugging d'une application CLI

Pour afficher certaines informations rapidement, on a vu que le printf-debugging ou le logging peuvent être très utiles.

Malheureusement, il peut arriver qu'on veuille regarder le contenu d'une certaine variable à un instant *t* sans changer le code, exécuter un bout de fonction, réaliser un import ou supprimer le cache en plein milieu d'une fonction dans changer le code (pour tester un certain chemin par exemple).

Il est possible de faire ça et encore plus à l'aide d'un outil fort pratique: le **debugger**.
Dans l'univers Python, le debugger s'appelle **pdb**. Mais je vais vous présenter un outil plus propre et plus puissant basé dessus: **ipdb** (la plupart des commandes sont les mêmes).

## 1. Découverte de l'app de tâches

Dans le dossier `examples/2-debugging-cli` vous trouverez une petite appli de gestion de TODO.
Prenez le temps de regarder le code, il est pas trop complexe et facile à comprendre.

Pour l'exécuter (s'assurer qu'on a bien chargé le virtualenv):

```bash
> python examples/2-debugging-cli/main.py
```

```text
[tasks.cli] INFO 2019-02-08 12:14:54,301 Running task client...

Welcome to the task manager!


ID | Title                        | Date            | Done
---|------------------------------|-----------------|-------
---|------------------------------|-----------------|-------

? What do you want to do?  (Use arrow keys)
   show task list
   show task
   add task
   toggle task
   rename task
   remove task
   export tasks
   import tasks
 » exit
```

Vous pouvez ajouter une tâche, supprimer, renommer, changer le status, exporter et importer dans des fichiers.

Après avoir un peu joué avec l'app, on va entrer dans le debugger !

## 2. L'entrée du debugger

Documentation officielle: [https://docs.python.org/3.6/library/pdb.html](https://docs.python.org/3.6/library/pdb.html)

Pour entrer, tapez ça (juste ajouter `-m ipdb` avant):

```bash
> python -m ipdb examples/2-debugging-cli/main.py
```

```text
> c:\...\coding-dojo\cd1-debugging\examples\2-debugging-cli\main.py(1)<module>()
----> 1 """Main."""
      2
      3 from tasks.cli import TaskClient

ipdb> _
```

Bienvenue sur le *prompt* d'ipdb ! Avant de paniquer, vous pouvez afficher la liste des commandes avec `help` ou regarder la [documentation officielle](https://docs.python.org/3.6/library/pdb.html).

```text
ipdb> help

Documented commands (type help <topic>):
========================================
EOF    cl         disable  interact  next    psource  rv         unt
a      clear      display  j         p       q        s          until
alias  commands   down     jump      pdef    quit     source     up
args   condition  enable   l         pdoc    r        step       w
b      cont       exit     list      pfile   restart  tbreak     whatis
break  continue   h        ll        pinfo   return   u          where
bt     d          help     longlist  pinfo2  retval   unalias
c      debug      ignore   n         pp      run      undisplay

Miscellaneous help topics:
==========================
exec  pdb

ipdb> _
```

Voici une liste des commandes principales avec des petites explications:

- **w**/where - Voir où on est dans la stack complète, fonctions parent y compris.
- **l**/list - Afficher la ligne courante et les 5 lignes suivantes.
- **ll**/longlist - Afficher le code de la fonction courante.
- **p**/print *var_name* - Affiche le contenu d'une variable. Utiliser **pp** pour pretty-print.
- **s**/step - Exécute la ligne suivante, et entre dans les appels de fonction
- **n**/next - Exécute la ligne suivante, sans entrer dans les appels de fonction
- **c**/continue - Continue l'exécution jusqu'au prochain breakpoint
- **r**/return - Continue l'exécution jusqu'au retour de la fonction courante
- **u**/up - Remonte le contexte sur la fonction parent (utile pour les vars dessus)
- **d**/down - Descend le contexte sur la fonction enfant (utile pour les vars dessous)
- **b**/break *location* - Ajouter un breakpoint sur un fichier. Le paramètre peut être:
  - Juste une ligne (ex. *86* pour mettre un bp à la ligne *86* du fichier courant)
  - Un nom de fonction (ex. *toto* pour mettre un bp sur l'entrée de la fonction *toto* du fichier courant)
  - Un chemin avec une ligne ou une fonction (ex. *c:\users\...\toto.py:42* pour mettre un bp à la ligne *42* sur le fichier *toto.py*)
- **tb**/tbreak - Ajouter un breakpoint temporaire: une fois passé, il disparaît
- **disable** *id* - Désactive un breakpoint par son ID
- **restart** - Recommence le debugger depuis le début
- **q**/quit - Quitter le debugger

C'est une grosse liste de commandes, et on apprend pas ça juste en lisant, pour commencer à maîtriser le debugger il faut pratiquer !

> Attention: si vous allez trop vite et passez une fonction au lieu d'entrer dedans, pas de panique, vous pouvez recommencer
> avec la commande **restart**, ou en sortant de pdb avec **q** et en relançant la commande. Je pense que ça va vous arriver assez souvent au début.

## 3. Exploration dans la hiérarchie

On peut commencer avec **w**(here) pour savoir où on se trouve:

```text
ipdb> w
  c:\...\python\current\lib\bdb.py(585)run()
    584         try:
--> 585             exec(cmd, globals, locals)
    586         except BdbQuit:

  <string>(1)<module>()

> c:\...\coding-dojo\cd1-debugging\examples\2-debugging-cli\main.py(1)<module>()
----> 1 """Main."""
      2
      3 from tasks.cli import TaskClient

ipdb> _
```

On se rend compte qu'on est dans le fichier `main.py` et qu'on a deux fonctions parentes:

- une éxécution dans le module courant (`<string>(1)<module>()`)
- une fonction parente dans `bdb.py` (`run`)

On peut remonter dans le contexte parent avec la commande **u**(p). Il faut le faire 2 fois pour remonter dans `bdb.py`.
Si on fait **l**(ist) ou **ll**, on voit le code courant de `bdb.py`:

```text
ipdb> l
    580         self.reset()
    581         if isinstance(cmd, str):
    582             cmd = compile(cmd, "<string>", "exec")
    583         sys.settrace(self.trace_dispatch)
    584         try:
--> 585             exec(cmd, globals, locals)
    586         except BdbQuit:
    587             pass
    588         finally:
    589             self.quitting = True
    590             sys.settrace(None)

ipdb> _
```

On peut ensuite redescendre dans notre `main.py` en appelant 2 fois **d**(own).

## 4. Step-by-step

On va avancer dans le code en faisant 4 fois **n**(ext), jusqu'a ce que la ligne courante soit la ligne 12, avec l'appel à `main()`.

> Conseil: si on ne tape pas de commande et qu'on valide, la commande précédente est utilisée.

Une fois sur la ligne, on entre dans la fonction avec **s**(tep), et hop, on se retrouve à la ligne 6 sur l'en-tête de la fonction `main`.

```text
ipdb> s
--Call--
> c:\...\coding-dojo\cd1-debugging\examples\2-debugging-cli\main.py(6)main()
      5
----> 6 def main():
      7     client = TaskClient()

ipdb> _
```

> Exercice: à l'aide de **s** et **n**, essayez d'atterir dans le constructeur du `TaskManager` et d'afficher la valeur de `self.task_index` avec la commande **p**.

On exécute la création du client avec **n**, et on peut afficher le client avec **p**:

```text
ipdb> p client
<tasks.cli.TaskClient object at 0x000001D4D87B8588>
```

On apprend pas grand chose. On va regarder ce qui existe dans l'objet client avec le code `p client.__dict__`.

```text
ipdb> p client.__dict__
{'mgr': <tasks.models.TaskManager object at 0x000001D4D89265C0>}
```

On voit donc qu'il y a un champ `mgr` qui contient un `TaskManager`.
Un des intérêts à utiliser `ipdb` plutot que le `pdb` standard c'est que vous pouvez taper `p client.`, faire *TAB*, et bim: autosuggestions, ce qui peut être plus pratique que de passer par `__dict__`.

On continue notre exploration en entrant dans la fonction `run`:

```text
ipdb> s
--Call--
> c:\...\coding-dojo\cd1-debugging\examples\2-debugging-cli\tasks\cli.py(38)run()
     37
---> 38     def run(self):
     39         logger.info("Running task client...")

ipdb> _
```

On va tenter de placer un breakpoint sur l'appel de la fonction `prompt_action`. En listant le code (**ll**), on voit que l'appel est sur la ligne *47*.
On peut donc taper `b 47`.

```text
ipdb> b 47
Breakpoint 1 at c:\...\coding-dojo\cd1-debugging\examples\2-debugging-cli\tasks\cli.py:47
ipdb> _
```

Ok, on a placé notre breakpoint, on peut maintenant continuer l'exécution du code jusqu'au bp en utilisant la commande **c**(ontinue).

```text
ipdb> c
[tasks.cli] INFO 2019-02-08 15:10:24,796 Running task client...

Welcome to the task manager!


ID | Title                        | Date            | Done
---|------------------------------|-----------------|-------
---|------------------------------|-----------------|-------

> c:\...\coding-dojo\cd1-debugging\examples\2-debugging-cli\tasks\cli.py(47)run()
     46             try:
1--> 47                 running = self.prompt_action()
     48             except KeyboardInterrupt:

ipdb> _
```

On est directement allé jusqu'au breakpoint (indiqué par un *1*). D'ici on peut afficher l'état des variables locales comme `running`, `self.mgr`, `WELCOME_MESSAGE` ou encore `ACTION_HANDLER` en utilisant **p** ou **pp**.

```text
ipdb> pp running
True
ipdb> pp ACTION_HANDLERS
OrderedDict([('show task list', '_show_task_list'),
             ('show task', '_show_task'),
             ('add task', '_add_task'),
             ('toggle task', '_toggle_task'),
             ('rename task', '_rename_task'),
             ('remove task', '_remove_task'),
             ('export tasks', '_export_tasks'),
             ('import tasks', '_import_tasks'),
             ('stats (buggy)', '_show_stats'),
             ('exit', '_exit')])
ipdb> _
```

D'ici, vous pouvez continuer l'exploration en utilisant tout ce que vous avez vu jusque là.

## 5. Exercices

### Exercice 1: trouve le code caché

Le code contient un morceau de texte secret qu'il vous faut trouver sans lire ou modifier les sources depuis un éditeur et seulement en utilisant **ipdb**.
Voici les indices:

- La variable s'appelle `secret` et se trouve dans une des fonctions du `TaskManager`, accessible par l'une des actions disponibles sur l'app. Promenez vous sur les actions.
- Mettez un breakpoint sur l'appel à la fonction de résolution des actions (cli.py, ligne 58) et faites un pas. Et regardez du côté de `_show_task`.
- Le code est stocké en base64. Vous pouvez décoder en utilisant la fonction `b64decode` de la lib standard `base64`.
- Il est possible d'exécuter du code arbitraire dans la session ipdb, en évitant d'écraser les commandes avec des noms de variables courts (donc il est également possible de faire des imports).

### Exercice 2: crée une tâche avant le démarrage du client

C'est pas très compliqué, mais ça demande de se mettre au bon endroit au bon moment.
Vous pouvez utiliser la fonction `add_task(title)` de l'objet `TaskManager`.

### Exercice 3: fixer le bug de la fonction stats

Visez la fonction `show_stats` de la classe `TaskManager`.

- Il est possible de changer les valeurs des variables à la volée

<hr />

C'est tout pour le debugger et les applications CLI, il est temps de voir comment ça marche dans un environnement web.

<p style="float: left">
  <a href="./1-LOGGING.html">< Logging</a>
</p>

<p style="float: right">
  <a href="./3-DEBUGGING-WEB.html">Debugging d'une application web ></a>
</p>
