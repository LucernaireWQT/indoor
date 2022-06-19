from __future__ import annotations
from dataclasses import dataclass
import subprocess
from sortedcontainers import SortedSet
from os.path import exists

@dataclass
class RSSIReading:
    zone: int
    _id: int
    rssis: dict[str, str]

class RssiCsvWriter:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.known_macs: SortedSet = SortedSet()
        self.readings: list[RSSIReading] = []


    def load_from_file(self, filename):
        with open(filename, 'r') as fp:
            lines = fp.readlines()

        if len(lines) == 0:
            return
        
        striped_lines = []
        for striped_line in lines:
            striped_lines.append([r.strip() for r in striped_line.split(',')])

        self.known_macs.update(striped_lines[0][2:])
        
        for striped_line in striped_lines[1:]:
            zone, _id, *rssi_list = striped_line
            zone = int(zone)
            _id = int(_id)

            rssis: dict[str, str] = dict()
            for i in range(len(self.known_macs)):
                mac = self.known_macs[i]
                rssi = rssi_list[i]
                rssis[mac] = rssi


            self.readings.append(RSSIReading(zone, _id, rssis))


    def add_reading(self, zone: int, rssis: dict[str, str]):
        reading = RSSIReading(zone, len(self.readings), rssis)
        self.readings.append(reading)
        
        reading_macs = set(rssis.keys())
        new_macs = reading_macs.difference(self.known_macs)

        if len(new_macs) > 0:
            self.known_macs.update(new_macs)
            print(f"{len(reading_macs)}/{len(self.known_macs)} of known APs")
            print(f"-> found {len(new_macs)} new APs")

            self.write_from_scratch()
        else:
            print(f"{len(reading_macs)}/{len(self.known_macs)} of known APs")
            self.append_reading_to_file(reading)
        

    def write_from_scratch(self):
        with open(self.filename, 'w') as fp:
            fp.write(', '.join(["zone", "mesure"] + list(self.known_macs)) + '\n')
            for n, reading in enumerate(self.readings):
                zone = reading.zone
                rssis = reading.rssis
                
                line = ', '.join([str(zone).rjust(4), str(n).rjust(6)] + [rssis.get(mac, "NaN").rjust(17) for mac in self.known_macs]) + '\n'
                fp.write(line)

    def append_reading_to_file(self, reading: RSSIReading):
        zone = reading.zone
        rssis = reading.rssis

        with open(self.filename, 'a') as fp:
            n = len(self.readings) - 1
            line = ', '.join([str(zone).rjust(4), str(n).rjust(6)] + [rssis.get(mac, "NaN").rjust(17) for mac in self.known_macs]) + '\n'
            fp.write(line)


def get_rssis() -> dict[str, str]:
    values: dict[str, str] = {}

    output = subprocess.getoutput('.\\WifiInfoView.exe /stab "" | .\\GetNir.exe "MAC Address,RSSI" "1=1"')
    
    for line in output.split("\n"):
        mac, rssi = line.split("\t")
        values[mac] = rssi

    return values


def capture_values_to_file(filename):
    rssiwriter = RssiCsvWriter(filename)
    if exists(filename):
        rssiwriter.load_from_file(filename)

    while True:
        zone = int(input("Zone: "))
        if zone == -1:
            return

        print(f"Capturing zone {zone}: ")

        total_to_do = len(rssiwriter.readings)

        nb_values = int(input("Aquisitions(-1 pour changer de zone): "))
        while nb_values != -1:
            if nb_values == -1:
                return

            total_to_do += nb_values

            for _ in range(nb_values):
                rssiwriter.add_reading(zone, get_rssis())

                print(f"reading : {len(rssiwriter.readings)}/{total_to_do}")
                print()

            nb_values = int(input("Aquisitions(-1 pour changer de zone): "))


if __name__ == "__main__":
    capture_values_to_file("new_captures.csv")
