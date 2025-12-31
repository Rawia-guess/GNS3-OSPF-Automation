# Exemple — Configuration rapide pour tester `automation_full.py`

But: Ce document explique comment exposer les routeurs GNS3 en telnet sur `127.0.0.1` afin que le script `automation_full.py` puisse s'y connecter.

Ports et mappage (défini dans `automation_full.py`):

- R1 : 5010
- R2 : 5017
- R3 : 5018
- R4 : 5019
- R5 : 5020
- R6 : 5021
- R7 : 5002
- R8 : 5001
- R9 : 5022
- R10: 5023
- R11: 5024
- R12: 5014
- R13: 5015
- R14: 5016

Instructions générales

- Assurez-vous que chaque routeur dans votre projet GNS3 accepte des connexions Telnet TCP et que le port local correspondant ci‑dessus est routable depuis la machine exécutant le script (localhost/127.0.0.1).
- Dans GNS3 Desktop vous pouvez :
  - Pour chaque routeur, ouvrir les préférences de la console et configurer l'accès via `Telnet` sur le port souhaité (ou laisser GNS3 assigner un port et rediriger vers celui-ci).
  - Alternativement, utilisez un forwarder TCP (socat sur Linux/macOS) pour exposer le port local si nécessaire.

Exemple (Linux / macOS) — rediriger une console série locale vers un port TCP :

```bash
# Exemple socat : /dev/pts/X → 127.0.0.1:5010
socat -d -d TCP-LISTEN:5010,reuseaddr,fork FILE:/dev/pts/5,raw,echo=0
```

Remarques Windows
- Sous Windows, vous pouvez utiliser des outils tiers (par ex. ncat, ser2net pour WSL, ou configurer la console GNS3 pour exposer un port TCP). L'important : `automation_full.py` doit atteindre `127.0.0.1:<port>` en telnet.

Vérification
- Une fois la topologie démarrée, testez la connexion telnet depuis la machine hôte :

```bash
telnet 127.0.0.1 5010
```

- Si la connexion s'établit et que vous voyez l'invite Cisco, le script pourra se connecter.

Si vous voulez, je peux générer un petit export GNS3 (.gns3project) basé sur cette table de ports — dites-moi si vous utilisez GNS3 Desktop ou GNS3 Server (remote) et je le prépare.
