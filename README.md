# Automatisation GNS3 — Configuration OSPF et sauvegardes

Description
- Script Python pour automatiser la configuration d'une maquette GNS3 (routeurs Cisco), activer OSPF, réaliser des sauvegardes de configuration, collecter des informations et exécuter des tests de connectivité.

Fonctionnalités principales
- Configure les interfaces et OSPF sur une liste de routeurs définie.
- Sauvegarde le `running-config` dans `backups/`.
- Récupère et sauvegarde les sorties (interfaces, voisins OSPF, routes, ping) dans `outputs/`.
- Enregistre un log d'affichage enrichi dans `logs/`.

Prérequis
- Python 3.8+
- Accès au réseau local / à GNS3 où chaque routeur est exposé en `telnet` sur `127.0.0.1` et un port unique.
- Bibliothèques Python : `netmiko`, `rich`.

Installation
1. Créez et activez un environnement virtuel (recommandé) :

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows PowerShell
```

2. Installez les dépendances :

```bash
pip install netmiko rich
```

Configuration
- Le fichier principal est `automation_full.py` (définit l'inventaire `routers` avec `name`, `port`, `ip`, `lan`, `rid`, `role`).
- Les identifiants utilisés par défaut sont `admin/admin` (utilisateur/secret). Adaptez selon votre maquette.
- Les dossiers `backups`, `outputs` et `logs` sont créés automatiquement par le script.

Usage

```bash
python automation_full.py
```

- Le script parcourt chaque routeur défini dans la liste `routers`, se connecte via Netmiko (telnet vers `127.0.0.1:<port>`), applique la configuration, sauvegarde et collecte les sorties.

Structure des fichiers (exemples)
- `automation_full.py` : script principal ([voir fichier](GNS3_automatisation/automation_full.py#L1)).
- `backups/` : sauvegardes des configurations (fichiers `R1.txt`, `R2.txt`, ...).
- `outputs/` : sorties collectées par routeur.
- `logs/` : logs d'affichage générés par `rich`.

Personnalisation
- Pour ajouter/supprimer des routeurs, modifiez la liste `routers` dans `automation_full.py`.
- Adaptez les commandes de configuration ou les tests de ping selon votre topologie.

Dépannage
- Erreurs de connexion : vérifiez que GNS3 expose bien les routeurs en telnet sur `127.0.0.1` et les ports indiqués.
- Timeout ou commandes non reconnues : augmentez `timeout` dans la définition `device` ou adaptez `device_type` si nécessaire.

Contribuer
- Suggestions et corrections bienvenues — ouvrez une issue ou proposez une PR.

Licence
- À préciser (par défaut : projet privé). Si vous souhaitez une licence permissive, je peux ajouter un `LICENSE` (MIT).

Contact
- Si vous voulez que j'ajoute un `requirements.txt`, des exemples de configuration GNS3 ou un script de démarrage, dites-le et je l'ajouterai.
