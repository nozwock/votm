import os
import shutil
from sys import argv
from pathlib import Path
from spec._data import BASE_DIR
from votm import __version__

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
command = ["pyinstaller {0} --noconfirm {1}".format(i, argv) for i in TEMP_FILE]
for i in command:
    os.system(i)  # for now can't check if command executes successfully

dist_dir = BASE_DIR.joinpath("dist")
source = dist_dir.joinpath(f"votm_dist_{__version__}_vote")
target = dist_dir.joinpath(f"votm_dist_{__version__}_manage")

counter = 0

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
# cleaning up
shutil.rmtree(str(source), ignore_errors=True)
for i in TEMP_FILE:
    Path(i).unlink()
