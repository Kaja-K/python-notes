# ── WRITE ────────────────────────────────────────────────────
with open("file.txt", "w", encoding="utf-8") as f:
    f.write("some content\n")   # writes a string, \n = new line
    f.write("second line\n")    # overwrites file if it already exists

# ── APPEND ───────────────────────────────────────────────────
with open("file.txt", "a", encoding="utf-8") as f:
    f.write("third line\n")     # adds to end, does not overwrite

# ── READ ─────────────────────────────────────────────────────
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()          # entire file as one string
    
with open("file.txt", "r") as f:
    lines = f.readlines()       # list of lines, each ending with \n
    
with open("file.txt", "r") as f:
    line = f.readline()         # reads one line at a time

# most memory-efficient — iterate line by line (no full load)
with open("file.txt", "r") as f:
    for line in f:
        print(line.strip())     # strip() removes the trailing \n

# ── FILE MODES ───────────────────────────────────────────────
# "r"   read only (default) — error if file doesn't exist
# "w"   write — creates file if missing, OVERWRITES if exists
# "a"   append — creates if missing, adds to end if exists
# "x"   exclusive create — error if file already exists
# "r+"  read and write — file must exist
# "rb"  read binary (images, PDFs, etc.)
# "wb"  write binary

# ── PATHS ────────────────────────────────────────────────────
open("file.txt")                # current working directory
open("data/file.txt")           # relative path
open("/home/user/file.txt")     # absolute path

from pathlib import Path        # modern way to handle paths
p = Path("data") / "file.txt"  # builds path safely across OS
p.exists()                      # True / False
p.read_text(encoding="utf-8")   # read entire file in one line
p.write_text("hello\n")         # write in one line
p.parent                        # "data" directory
p.stem                          # "file" (name without extension)
p.suffix                        # ".txt"

# ── CHECK BEFORE OPENING ─────────────────────────────────────
import os
os.path.exists("file.txt")      # True / False
os.path.isfile("file.txt")      # True only if it's a file (not dir)
os.path.getsize("file.txt")     # file size in bytes

# ── SAFE OPEN WITH ERROR HANDLING ────────────────────────────
try:
    with open("file.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("File doesn't exist!")
except PermissionError:
    print("No permission to read this file!")

# ── WORKING WITH LINES ───────────────────────────────────────
with open("file.txt", "r") as f:
    lines = [line.strip() for line in f]        # clean list, no \n
    lines = [line.strip() for line in f if line.strip()]  # skip empty lines

# ── WRITE MULTIPLE LINES ─────────────────────────────────────
lines = ["Warsaw", "Krakow", "Gdansk"]
with open("cities.txt", "w") as f:
    f.writelines(line + "\n" for line in lines) # write all at once
    # or: f.write("\n".join(lines))

# ── CSV ──────────────────────────────────────────────────────
import csv

with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])            # header
    writer.writerow(["Anna", 25])

with open("data.csv", "r") as f:
    reader = csv.DictReader(f)                  # each row as a dict
    for row in reader:
        print(row["name"], row["age"])

# ── JSON ─────────────────────────────────────────────────────
import json

data = {"name": "Anna", "scores": [10, 20, 30]}

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)                # write dict → JSON file

with open("data.json", "r") as f:
    loaded = json.load(f)                       # read JSON file → dict

json.dumps(data)                                # dict → JSON string (no file)
json.loads('{"a": 1}')                          # JSON string → dict