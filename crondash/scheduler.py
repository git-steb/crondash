#!/usr/bin/env python3
"""
Minimal cron-style scheduler for macOS.

* Reads crontab file from config.
* Uses croniter to decide which jobs run at the current time.
* Logs all output to artifacts directory.
* Sets CRONDASH_ARTIFACTS_DIR for each task.
"""

import subprocess, shlex, pathlib, sys, os
from datetime import datetime

# Try to import optional dependencies
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    from croniter import croniter
    CRONITER_AVAILABLE = True
except ImportError:
    CRONITER_AVAILABLE = False

def load_config():
    """Load configuration from config.yaml"""
    config_path = pathlib.Path(__file__).resolve().parent.parent / "config.yaml"
    if config_path.exists():
        if YAML_AVAILABLE:
            with open(config_path) as f:
                return yaml.safe_load(f)
        else:
            # Basic config parser without yaml dependency
            config = {}
            with open(config_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and ':' in line:
                        key, value = line.split(':', 1)
                        config[key.strip()] = value.strip()
            return config
    return {
        "artifacts_dir": "./artifacts",
        "crontab": "./crontab/mycrontab.txt",
        "log_level": "INFO"
    }

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
config = load_config()
CRONTAB_FILE = BASE_DIR / config["crontab"]
LOG_DIR = BASE_DIR / config["artifacts_dir"]
LOG_DIR.mkdir(exist_ok=True)

now = datetime.now().replace(second=0, microsecond=0)

def should_run(expr, ts):
    if not CRONITER_AVAILABLE:
        print("❌ croniter not available. Install with: pip install croniter", file=sys.stderr)
        return False
    try:
        return croniter.match(expr, ts)
    except Exception:
        return False

def run_job(line):
    cmd = line.split(None, 5)[5:]
    if not cmd:
        print(f"Malformed job line: {line}", file=sys.stderr)
        return
    task_name = pathlib.Path(cmd[0]).stem
    env = os.environ.copy()
    env["CRONDASH_ARTIFACTS_DIR"] = str(LOG_DIR / task_name)
    
    try:
        os.makedirs(env["CRONDASH_ARTIFACTS_DIR"], exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_path = LOG_DIR / f"{ts}_{task_name}.log"
        with open(log_path, "w") as lf:
            lf.write(f"=== {ts} ===\n$ {' '.join(cmd)}\n\n")
            subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT, text=True, shell=False, env=env)
    except (OSError, IOError) as e:
        # Fallback to stderr if artifact logging fails
        print(f"Failed to write to artifact log: {e}", file=sys.stderr)
        print(f"=== {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')} ===", file=sys.stderr)
        print(f"$ {' '.join(cmd)}", file=sys.stderr)
        subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, text=True, shell=False, env=env)

def main():
    if not CRONTAB_FILE.exists():
        sys.exit(f"Crontab file not found: {CRONTAB_FILE}")

    for raw in CRONTAB_FILE.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split(maxsplit=5)
        if len(fields) < 6:
            print(f"Skipping malformed crontab line: {line}", file=sys.stderr)
            continue
        cron_expr = " ".join(fields[:5])
        if should_run(cron_expr, now):
            run_job(line)

if __name__ == "__main__":
    main() 