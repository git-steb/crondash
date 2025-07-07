#!/usr/bin/env python3
"""
crondash CLI - Task registry and disk-aware cron dashboard
"""

import sys
import pathlib
from datetime import datetime
import subprocess
import os

VERSION = "0.1.0"

# --- Minimal logging ---
def log(msg):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}")

def load_config():
    config_path = pathlib.Path(__file__).resolve().parent.parent / "config.yaml"
    if not config_path.exists():
        log("No config.yaml found. Creating default config.yaml.")
        config_path.write_text("artifacts_dir: ./artifacts\ncrontab: ./crontab/mycrontab.txt\nlog_level: INFO\n")
    config = {}
    with open(config_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and ':' in line:
                key, value = line.split(':', 1)
                config[key.strip()] = value.strip()
    return config

def ensure_crontab():
    crontab_path = pathlib.Path(__file__).resolve().parent.parent / "crontab/mycrontab.txt"
    if not crontab_path.exists():
        crontab_path.parent.mkdir(parents=True, exist_ok=True)
        log("No crontab/mycrontab.txt found. Creating default crontab.")
        crontab_path.write_text("# crondash crontab\n# Add your tasks here. Examples:\n# 0 9 * * * /usr/bin/python3 tools/disk_watch.py\n")
    return crontab_path

def parse_crontab(crontab_path):
    tasks = []
    if not crontab_path.exists():
        return tasks
    for line in crontab_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split(maxsplit=5)
        if len(fields) < 6:
            continue
        cron_expr = " ".join(fields[:5])
        cmd = fields[5]
        task_name = pathlib.Path(cmd.split()[0]).stem
        tasks.append({
            "schedule": cron_expr,
            "command": cmd,
            "name": task_name
        })
    return tasks

def list_tasks():
    config = load_config()
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    crontab_path = ensure_crontab()
    tasks = parse_crontab(crontab_path)
    if not tasks:
        log("No tasks found in crontab.")
        sys.exit(1)
    print(f"{'Task':<20} {'Schedule':<20}")
    print("-" * 40)
    for task in tasks:
        print(f"{task['name']:<20} {task['schedule']:<20}")

def doctor():
    # Check if LaunchAgent is installed
    # Use launchctl list and launchctl print to inspect current state
    # Report status and provide fix command if not hooked up
    pass

def next_runs():
    """Show next scheduled run times - requires croniter"""
    try:
        from croniter import croniter
    except ImportError:
        log("croniter not available. Install with: pip install croniter")
        sys.exit(1)
    
    config = load_config()
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    crontab_path = ensure_crontab()
    tasks = parse_crontab(crontab_path)
    now = datetime.now()
    
    if not tasks:
        log("No tasks found in crontab.")
        sys.exit(1)
    
    print(f"{'Task':<20} {'Next Run':<20} {'Schedule':<20}")
    print("-" * 60)
    
    for task in tasks:
        try:
            cron = croniter(task["schedule"], now)
            next_run = cron.get_next(datetime)
            next_str = next_run.strftime("%Y-%m-%d %H:%M")
            print(f"{task['name']:<20} {next_str:<20} {task['schedule']:<20}")
        except Exception as e:
            print(f"{task['name']:<20} {'ERROR':<20} {task['schedule']:<20}")

def brew_install():
    import subprocess
    formula_path = pathlib.Path(__file__).resolve().parent.parent / "crondash.rb"
    if not formula_path.exists():
        log("crondash.rb formula not found in repo root.")
        sys.exit(1)
    log("Invoking: brew install --HEAD --build-from-source ./crondash.rb")
    try:
        subprocess.run(["brew", "install", "--HEAD", "--build-from-source", str(formula_path)], check=True)
    except Exception as e:
        log(f"brew install failed: {e}")
        sys.exit(1)

def pip_install():
    import subprocess
    log("Invoking: pip install .")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "."], check=True)
    except Exception as e:
        log(f"pip install failed: {e}")
        sys.exit(1)

def show_help():
    print('''
crondash - A lightweight cron-style task registry and disk dashboard

Usage:
  crondash list            Show all tasks
  crondash doctor          System health check
  crondash init            Initialize crondash environment
  crondash add-task        Add a new task
  crondash enable <task>   Enable a task
  crondash disable <task>  Disable a task
  crondash next            Show next scheduled runs (requires croniter)
  crondash tools           List available optional tools
  crondash install-pip     Install crondash with pip
  crondash install-brew    Install crondash with Homebrew
  crondash version         Show version
  crondash help, --help    Show this help message

If running from repo:
  ./crondash.cli <command>
''')

def show_version():
    # Try to read from pyproject.toml if available
    pyproject = pathlib.Path(__file__).resolve().parent.parent / "pyproject.toml"
    if pyproject.exists():
        for line in pyproject.read_text().splitlines():
            if line.strip().startswith("version"):
                print(line.strip())
                return
    print(f"crondash version {VERSION}")

def list_tools():
    """List available optional tools"""
    tools_dir = pathlib.Path(__file__).resolve().parent.parent / "tools"
    if not tools_dir.exists():
        print("No tools directory found.")
        return

    print("Available optional tools:")
    print("=" * 40)
    
    for yaml_file in tools_dir.glob("*.yaml"):
        try:
            # Basic YAML parsing without dependency
            config = {}
            with open(yaml_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and ':' in line:
                        key, value = line.split(':', 1)
                        config[key.strip()] = value.strip().strip('"')
            
            name = config.get('name', yaml_file.stem)
            description = config.get('description', 'No description')
            default_schedule = config.get('default_schedule', 'Not specified')
            
            print(f"📦 {name}")
            print(f"   {description}")
            print(f"   Default schedule: {default_schedule}")
            print(f"   Config: {yaml_file.name}")
            print()
        except Exception as e:
            print(f"📦 {yaml_file.stem} (config error: {e})")
            print()

def add_task():
    # Guide user through task setup
    # Scaffold tasks/<task>/task.yaml
    pass

def handle_missed_runs(task):
    # Implement logic to handle missed runs based on task YAML configuration
    pass

def enable_task(task_name):
    # Enable the specified task
    pass

def disable_task(task_name):
    # Disable the specified task
    pass

def init():
    # Create ~/.crondash directory and symlink dot-crontab
    pass

# Add command handling in the main function
if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        list_tasks()
    elif command == "doctor":
        doctor()
    elif command == "init":
        init()
    elif command == "add-task":
        add_task()
    elif command == "enable":
        if len(sys.argv) < 3:
            log("Please specify a task to enable.")
            sys.exit(1)
        enable_task(sys.argv[2])
    elif command == "disable":
        if len(sys.argv) < 3:
            log("Please specify a task to disable.")
            sys.exit(1)
        disable_task(sys.argv[2])
    elif command == "next":
        next_runs()
    elif command == "tools":
        list_tools()
    elif command == "install-pip":
        pip_install()
    elif command == "install-brew":
        brew_install()
    elif command == "version":
        show_version()
    elif command in ("help", "--help"):
        show_help()
    else:
        log(f"Unknown command: {command}")
        show_help()
        sys.exit(1)
