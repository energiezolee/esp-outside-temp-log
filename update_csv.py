import csv
import requests
from datetime import datetime

URL = "http://SAJAT_DDNS/cgi-bin/github_daily.cgi"
FILE = "outside_history.csv"

# 1. adat lekérése a routerről
r = requests.get(URL, timeout=10)
line = r.text.strip()

date, tmin, tmax = line.split(",")

# 2. meglévő CSV beolvasása
rows = []

try:
    with open(FILE, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
except FileNotFoundError:
    rows = [["Date", "OutsideMin", "OutsideMax"]]

header = rows[0]
data = rows[1:]

# 3. frissítés logika (egy nap = 1 sor)
updated = False

for i, row in enumerate(data):
    if row[0] == date:
        data[i] = [date, tmin, tmax]
        updated = True
        break

if not updated:
    data.append([date, tmin, tmax])

# 4. visszaírás
with open(FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)

print("Done:", date, tmin, tmax)
