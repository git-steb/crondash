#!/usr/bin/env python3
import subprocess, pathlib, datetime, os

target_dir = os.environ.get("CRONDASH_ARTIFACTS_DIR")
if not target_dir:
    raise RuntimeError("CRONDASH_ARTIFACTS_DIR is not set")

ART = pathlib.Path(target_dir)
ART.mkdir(parents=True, exist_ok=True)

ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
outfile = ART / f"diskwatch_{ts}.log"

with open(outfile, "w") as f:
    f.write(f"=== Disk snapshot {ts} ===\n\n")
    subprocess.run(["df", "-h", "/System/Volumes/Data"], stdout=f)
    f.write("\n")
    subprocess.run(["sudo", "du", "-sh", "/System/Library/AssetsV2"],
                   stdout=f, stderr=subprocess.DEVNULL)
    f.write("\n")
    docker_raw = os.path.expanduser("~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw")
    subprocess.run(["du", "-sh", docker_raw], stdout=f, stderr=subprocess.DEVNULL) 

# This is a placeholder for the disk_watch functionality.
# The actual implementation will be added here.

# Example function
def disk_watch():
    pass 