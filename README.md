[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/hzCHf1-n)
# RoboArmSimulator 

## Beskrivning
Ett huvud Desktop GUI för att kontrollera ett riktigt robot arm. GUI
kommunicerar med ett server. Server håller "True state" av arm segment
positioner. När första GUI klient ansluter till server blir den automatiskt
till "Kontroller" alltså den som får styra robot armen. Andra GUI klienter får
ansluta men de får ett "Viewer" roll dvs dem kan se armens nuläges position.

Projektet är indelat i olika projekt mappar samt en libs/commonlib mapp (där json schema och
logging är definerad). Under mappen projects finns det 3 färdiga projekt:
robo_arm_sim (Pyside6 GUI), server (WS) och esp32_client (skriven i arduino).

## Installation och användning
För att installera de bibliotek som behövs och köra programmet, öppna en
terminal och kör följande kommandon. OBS dessa bash scripts fungerar endast på Linux
för Windows kan man pipa requirments.txt och köra main.py filerna själv:
*LMAO WHO USES WINDOWS*

```bash
source scripts/setup.sh
install-app <app-name>
start-app <app-name>
```
<app-name>: [server, robo_arm_sim]

## Teknologier
Till projektets GUI program användes PySide6. 
För server användes websocket bibliotek tillsammans med asyncio


## Bidra
Detta är ett projekt i kursen Programmering 2 på NTI Gymnasiet Nacka VT24. Då projektet kommer att bedömas och användas som betygsunderlag tillåts inga pull-requests eller kommentarer kring projektet. Var vänlig respektera detta.

## Licens

Projektet är släppt under MIT:s licens.

## Författare

Eduards Abisevs [GitHub](https://github.com/Abishevs)

## Donations
[BuyMeACoffe](hah_sike_swisha_mig)
