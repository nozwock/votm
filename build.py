import os
import time
import shutil
import subprocess
from sys import argv
from pathlib import Path
from spec._data import BASE_DIR
from rich.console import Console
from rich.traceback import install
from votm import __version__

install()

start = time.time()
console = Console()

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
for i, j in enumerate(command):
    try:
        console.print(
            f"[orange1]•[/orange1] [green3]"
            f"Generating Build [deep_sky_blue1][{i+1}/{len(command)}][/deep_sky_blue1][/green3]...",
            end="",
        )
        proc = subprocess.run(
            j,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        console.print("ok", end=" ")
        console.print(f"[u]ReturnCode:[/u] {proc.returncode}")
    except subprocess.CalledProcessError as e:
        console.print(f" [bold red1]Error:[/bold red1] {e.returncode}")
        raise

dist_dir = BASE_DIR.joinpath("dist")
source = dist_dir.joinpath(f"votm_dist_{__version__}_vote")
target = dist_dir.joinpath(f"votm_dist_{__version__}_manage")

counter = 0

console.print("[orange1]•[/orange1] [green3]Collecting...")
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

console.print("[orange1]•[/orange1] [green3]Cleaning up...")
# cleaning up
shutil.rmtree(str(source), ignore_errors=True)
for i in TEMP_FILE:
    Path(i).unlink()

end = time.time()
console.print(
    f"[orange1]Build compeletion in[/orange1] [u]{end-start}[/u] [green3]seconds[/green3]"
)
