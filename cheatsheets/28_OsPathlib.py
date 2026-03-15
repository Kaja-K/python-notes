from pathlib import Path
import os
import pandas as pd

# ── CURRENT LOCATION ─────────────────────────────────────────
os.getcwd()                                     # current working directory
os.listdir('.')                                 # list files in directory
os.listdir('/some/path')

# ── PATH OPERATIONS (old way — os.path) ──────────────────────
os.path.exists('file.txt')                      # True / False
os.path.isfile('file.txt')                      # True only if file
os.path.isdir('data/')                          # True only if directory
os.path.join('data', 'reports', 'file.csv')    # safe path join (cross-OS)
os.path.basename('/data/file.csv')             # 'file.csv'
os.path.dirname('/data/file.csv')              # '/data'
os.path.splitext('file.csv')                   # ('file', '.csv')
os.path.getsize('file.csv')                    # size in bytes

# ── PATHLIB — modern, recommended ────────────────────────────
p = Path('data/reports/file.csv')

p.exists()                  # True / False
p.is_file()                 # True if file
p.is_dir()                  # True if directory
p.name                      # 'file.csv'
p.stem                      # 'file'
p.suffix                    # '.csv'
p.parent                    # Path('data/reports')
p.parts                     # ('data', 'reports', 'file.csv')

# building paths — / operator is cleaner than os.path.join
base = Path('data')
full = base / 'reports' / 'file.csv'           # Path('data/reports/file.csv')

# read / write directly
p.read_text(encoding='utf-8')
p.write_text('hello\n', encoding='utf-8')
p.read_bytes()

# ── CREATING & DELETING ──────────────────────────────────────
Path('new_folder').mkdir()                      # create directory
Path('a/b/c').mkdir(parents=True, exist_ok=True)  # create all intermediate dirs

os.remove('file.txt')                           # delete a file
os.rmdir('empty_folder')                        # delete empty directory
import shutil
shutil.rmtree('folder')                         # delete folder and all contents
shutil.copy('src.csv', 'dst.csv')              # copy a file
shutil.move('old.csv', 'new_folder/old.csv')   # move a file

# ── LISTING & SEARCHING ──────────────────────────────────────
p = Path('data')
list(p.iterdir())                               # all files and folders
list(p.glob('*.csv'))                           # all CSVs in this folder
list(p.rglob('*.csv'))                          # all CSVs recursively

# load all CSVs in a folder into one DataFrame
import glob
files = glob.glob('data/**/*.csv', recursive=True)
df_all = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# same with pathlib
dfs = [pd.read_csv(f) for f in Path('data').rglob('*.csv')]
df_all = pd.concat(dfs, ignore_index=True)

# ── ENVIRONMENT VARIABLES ────────────────────────────────────
os.environ.get('HOME')                          # get env variable (safe — returns None)
os.environ['PATH']                              # raises KeyError if missing
os.environ.get('DB_PASSWORD', 'default')        # with fallback

# ── USEFUL OS EXTRAS ─────────────────────────────────────────
os.cpu_count()                                  # number of CPU cores
os.getenv('USER')                               # current username
os.sep                                          # '/' on Linux, '\\' on Windows
Path.home()                                     # home directory: Path('/home/user')
Path.cwd()                                      # current working dir as Path