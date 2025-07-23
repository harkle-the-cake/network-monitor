# \# 🖧 Netzwerk-Monitor (Flask + nmap + Docker)

# 

# Ein einfaches webbasiertes Tool zur Anzeige aller aktiven Geräte im lokalen Netzwerk. Das Tool nutzt `nmap` zur Erkennung und `ping`, um den Online-Status und die Antwortzeit zu bestimmen.

# 

# \## 🔧 Features

# 

# \- Scannt automatisch \*\*alle physikalischen Interfaces\*\* (z. B. `eth0`, `wlan0`) des Hosts

# \- Nutzt `nmap -sL` zur Namensauflösung im Subnetz

# \- Führt `ping` durch, um Online-Status und Latenz zu ermitteln

# \- Zeigt Daten im Web-Frontend als Tabelle

# \- Farbige Anzeige: 🟢 online, 🔴 offline

# \- Filter: Alle, Nur Online, Nur Offline

# \- Docker-basiert mit Host-Netzwerkzugriff

# 

# ---

# 

# \## 📸 Beispielansicht

# 

# | Name       | IP              | Status   | Ping (ms) | Netz            |

# |------------|------------------|----------|------------|-----------------|

# | slavepi1   | 192.168.180.20   | 🟢 online | 4 ms       | 192.168.180.0/24 |

# | slavepi2   | 192.168.180.21   | 🔴 offline| –          | 192.168.180.0/24 |

# 

# ---

# 

# \## 🚀 Setup

# 

# \### 1. Repository klonen

# 

# ```bash

# git clone https://github.com/DEIN-BENUTZERNAME/network-monitor.git

# cd network-monitor





# \### 2. Container bauen



``` bash

docker build -t network-monitor .



# \### 3. Container starten



``` bash

docker run --rm --net=host --name network-monitor network-monitor







