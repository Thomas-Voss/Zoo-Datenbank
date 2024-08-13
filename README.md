# Datenbank für einen fiktiven Zoo
 ## Kurzbeschreibung des Projekts
Dieses Projekt ist ein im Rahmen einer Fortbildung erstelltes Übungsprojekt von [Michael Heinrich](https://github.com/JimmyKnox2058) und [Thomas Voss](https://github.com/Thomas-Voss), das sich mit dem Prozess der Datenbankmodellierung und -erstellung beschäftigt. Der Kunde für das Projekt ist ein fiktiver Zoo, der seinen Papierbetrieb digitalisieren will. Das Ziel des Projekts ist, dafür eine Datenbank zu erstellen und ein Data-Warehouse- sowie ein Data-Quality-Konzept zu erarbeiten.

Das Projekt beinhaltet die folgenden Schritte:
 - Anforderungsmanagement
 - Erstellung eines ERM für die Datenbank, Star für Data Mart
 - Umsetzung der Datenbank in SQL
 - Schreiben eines Data Dictionary
 - Erstellung eines Data Quality Konzepts

## Anforderungsmanagement
 Der fiktive Kunde (Dozent des Kurses) hat zunächst ein Dokument mit seinen Vorstellungen und Wünschen für die Datenbank bereitgestellt. Da dieses Dokument in Teilen unpräzise und unvollständig war, haben wir die Anforderungen in einem weiteren Gespräch mit dem Kunden präzisiert und dokumentiert.

## Modellierung
 Auf Basis der Anforderungen haben wir ein ERM erstellt, das die Grundlage für die Datenbank bildet. Für ein genaueres und inhaltliches Verständnis der Datenbank haben wir ein Data Dictionary geschrieben. Ein weiteres exemplarisches ERM im Star-Schema haben wir für einen potenziellen Data Mart erstellt.

## Erstellung der Datenbank
 Das ERM haben wir in eine in SQL geschriebene Datenbank umgesetzt. Dabei haben wir auch Referenzwerte sowie Testdaten eingefügt. Mithilfe von Python-Skripten wurde überprüft, ob die erstellte Datenbank mit dem Data Dictionary und dem ERM übereinstimmt.

## Data Quality
 Um die Anforderungen an eine hohe Datenqualität sicherzustellen, haben wir ein Datenqualitätskonzept für den operativen Betrieb des Kunden ausgearbeitet.
