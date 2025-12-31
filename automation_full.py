from netmiko import ConnectHandler
from rich.console import Console
from rich.table import Table
import os
import time

# =========================
# INITIALISATION
# =========================
console = Console(record=True)

os.makedirs("backups", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# =========================
# INVENTAIRE ROUTEURS
# role:
#  - lan1 : R1 → R6
#  - border : R7, R8
#  - lan2 : R9 → R14
# =========================
routers = [
    # LAN 1
    {"name": "R1", "port": 5010, "ip": "10.10.10.1", "lan": "10.10.10.0", "rid": "1.1.1.1", "role": "lan1"},
    {"name": "R2", "port": 5017, "ip": "10.10.10.2", "lan": "10.10.10.0", "rid": "2.2.2.2", "role": "lan1"},
    {"name": "R3", "port": 5018, "ip": "10.10.10.3", "lan": "10.10.10.0", "rid": "3.3.3.3", "role": "lan1"},
    {"name": "R4", "port": 5019, "ip": "10.10.10.4", "lan": "10.10.10.0", "rid": "4.4.4.4", "role": "lan1"},
    {"name": "R5", "port": 5020, "ip": "10.10.10.5", "lan": "10.10.10.0", "rid": "5.5.5.5", "role": "lan1"},
    {"name": "R6", "port": 5021, "ip": "10.10.10.6", "lan": "10.10.10.0", "rid": "6.6.6.6", "role": "lan1"},

    # INTERCONNEXION
    {"name": "R7", "port": 5002, "ip": "10.10.10.7", "lan": "10.10.10.0", "rid": "7.7.7.7", "role": "border"},
    {"name": "R8", "port": 5001, "ip": "10.10.20.8", "lan": "10.10.20.0", "rid": "8.8.8.8", "role": "border"},

    # LAN 2
    {"name": "R9",  "port": 5022, "ip": "10.10.20.9",  "lan": "10.10.20.0", "rid": "9.9.9.9", "role": "lan2"},
    {"name": "R10", "port": 5023, "ip": "10.10.20.10", "lan": "10.10.20.0", "rid": "10.10.10.10", "role": "lan2"},
    {"name": "R11", "port": 5024, "ip": "10.10.20.11", "lan": "10.10.20.0", "rid": "11.11.11.11", "role": "lan2"},
    {"name": "R12", "port": 5014, "ip": "10.10.20.12", "lan": "10.10.20.0", "rid": "12.12.12.12", "role": "lan2"},
    {"name": "R13", "port": 5015, "ip": "10.10.20.13", "lan": "10.10.20.0", "rid": "13.13.13.13", "role": "lan2"},
    {"name": "R14", "port": 5016, "ip": "10.10.20.14", "lan": "10.10.20.0", "rid": "14.14.14.14", "role": "lan2"},
]

# =========================
# BOUCLE PRINCIPALE
# =========================
for r in routers:
    console.print(f"\n [bold cyan]Connexion à {r['name']}[/bold cyan]")

    device = {
        "device_type": "cisco_ios_telnet",
        "host": "127.0.0.1",
        "port": r["port"],
        "username": "admin",
        "password": "admin",
        "secret": "admin",
        "timeout": 15,
    }

    try:
        conn = ConnectHandler(**device)
        conn.enable()

        # =========================
        # CONFIG INTERFACE + OSPF
        # =========================
        cmds = [
            "conf t",
            "interface FastEthernet0/0",
            f"ip address {r['ip']} 255.255.255.0",
            "no shutdown",
            "exit",
            "router ospf 1",
            f"router-id {r['rid']}",
            f"network {r['lan']} 0.0.0.255 area 0",
        ]

        # Routeurs d'interconnexion (R7 & R8)
        if r["role"] == "border":
            cmds.append("network 10.10.30.0 0.0.0.3 area 0")

        cmds += ["end", "write memory"]

        conn.send_config_set(cmds)
        time.sleep(1)

        # =========================
        # BACKUP CONFIG
        # =========================
        running = conn.send_command("show running-config")
        with open(f"backups/{r['name']}.txt", "w") as f:
            f.write(running)

        # =========================
        # COLLECTE INFOS
        # =========================
        interfaces = conn.send_command("show ip interface brief")
        ospf_neighbors = conn.send_command("show ip ospf neighbor")
        routes = conn.send_command("show ip route ospf")

        # =========================
        # TEST DE PING AUTOMATIQUE
        # =========================
        if r["role"] == "lan1":
            ping = conn.send_command("ping 10.10.20.9 repeat 3")
        elif r["role"] == "lan2":
            ping = conn.send_command("ping 10.10.10.1 repeat 3")
        else:
            ping = conn.send_command("ping 10.10.30.2 repeat 3")

        # =========================
        # SAUVEGARDE OUTPUTS
        # =========================
        with open(f"outputs/{r['name']}.txt", "w") as f:
            f.write("=== INTERFACES ===\n" + interfaces)
            f.write("\n\n=== OSPF NEIGHBORS ===\n" + ospf_neighbors)
            f.write("\n\n=== OSPF ROUTES ===\n" + routes)
            f.write("\n\n=== PING TEST ===\n" + ping)

        # =========================
        # AFFICHAGE CONSOLE
        # =========================
        table = Table(title=f"{r['name']} – Interfaces")
        table.add_column("Interface")
        table.add_column("IP")
        table.add_column("Status")
        table.add_column("Protocol")

        for line in interfaces.splitlines()[1:]:
            p = line.split()
            if len(p) >= 6:
                table.add_row(p[0], p[1], p[-2], p[-1])

        console.print(table)
        console.print(" OSPF voisins :")
        console.print(ospf_neighbors if ospf_neighbors.strip() else "Aucun")
        console.print(" Résultat du ping :")
        console.print(ping)

        # =========================
        # LOG AFFICHAGE
        # =========================
        with open(f"logs/{r['name']}.log", "w", encoding="utf-8") as f:
            f.write(console.export_text())

        console.clear()
        conn.disconnect()
        console.print(f"[green]{r['name']} terminé[/green]")

    except Exception as e:
        console.print(f" [red]{r['name']} : {e}[/red]")

console.print("\n [bold cyan]AUTOMATISATION COMPLÈTE TERMINÉE[/bold cyan]")
