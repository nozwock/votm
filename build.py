import os
import shutil
from spec_data import BASE_DIR
from sys import argv
from votm import __version__

argv = " ".join(argv[1:])

SPEC_FILE = [
    "manage_dist.spec",
    "vote_dist.spec",
    "manage_bundled_bin.spec",
    "vote_bundled_bin.spec",
]

os.chdir(BASE_DIR)
command = ["pyinstaller {0} --noconfirm {1}".format(i, argv) for i in SPEC_FILE]
for i in command:
    os.system(i)

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
target.rename(target.parent.joinpath(f"votm_dist_{__version__}"))
# cleaning up
shutil.rmtree(str(source), ignore_errors=True)
