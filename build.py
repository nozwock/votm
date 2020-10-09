import os
import time
import shutil
import subprocess
from sys import argv
from pathlib import Path
from spec._data import BASE_DIR
from votm import __version__


start = time.time()
argv = " ".join(argv[1:])

SPEC_FILE = [
    "manageDist.spec",
    "voteDist.spec",
    "manageBundledBin.spec",
    "voteBundledBin.spec",
]

TEMP_FILE = [f"TEMP_{i}.spec" for i, _ in enumerate(SPEC_FILE)]

for i, j in enumerate(SPEC_FILE):
    try:
        shutil.copy(BASE_DIR.joinpath(f"spec/{j}"), BASE_DIR.joinpath(TEMP_FILE[i]))
    except:
        for i in TEMP_FILE:
            try:
                Path(i).unlink()
            except:
                pass

os.chdir(BASE_DIR)
command = [["pyinstaller", i, "--noconfirm", argv] for i in TEMP_FILE]
if argv.strip() == "":
    command = [i[:-1] for i in command]
for i, j in enumerate(command):
    try:
        print(
            f"• Generating Build [{i+1}/{len(command)}]...",
            end="",
        )
        proc = subprocess.run(
            j,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        print("ok", end=" ")
        print(f"ReturnCode: {proc.returncode}")
    except subprocess.CalledProcessError as e:
        print(f" Error: {e.returncode}")
        raise

dist_dir = BASE_DIR.joinpath("dist")
source = dist_dir.joinpath(f"votm_dist_{__version__}_vote")
target = dist_dir.joinpath(f"votm_dist_{__version__}_manage")

counter = 0

print("• Collecting...")
# collecting
for obj in source.iterdir():
    if obj.is_file():
        try:
            obj.rename(target / obj.name)
        except:
            pass
        counter += 1
    if counter > 1000:
        break

# renaming
try:
    target.rename(target.parent.joinpath(f"votm_dist_{__version__}"))
except FileExistsError:
    shutil.rmtree(
        target.parent.joinpath(f"votm_dist_{__version__}"), ignore_errors=True
    )
    target.rename(target.parent.joinpath(f"votm_dist_{__version__}"))

print("• Cleaning up...")
# cleaning up
shutil.rmtree(str(source), ignore_errors=True)
for i in TEMP_FILE:
    Path(i).unlink()

end = time.time()
print(f"Build compeletion in {end-start} seconds")
