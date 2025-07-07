# crondash

A lightweight cron-style task registry and disk usage dashboard for macOS.

[![GitHub](https://img.shields.io/badge/GitHub-crondash-blue?style=flat&logo=github)](https://github.com/git-steb/crondash)

---

## ⚡ Quickstart

```bash
# Install (pip, recommended)
./crondash.cli install-pip

# Or install system-wide (Homebrew, optional)
./crondash.cli install-brew

# Check system health
crondash doctor

# List all tasks
crondash list
```

---

## 🚀 Installation

### Option 1: pip (recommended for most users)

```bash
pip install .
# or from the repo root:
./crondash.cli install-pip
```
- Installs crondash for your current Python environment.
- No need for Homebrew.

### Option 2: Homebrew (for system-wide install)

```bash
brew install --HEAD --build-from-source ./crondash.rb
# or from the repo root:
./crondash.cli install-brew
```
- Installs crondash system-wide using Homebrew.
- Homebrew is **not required** for normal use.

---

## 🛠️ Usage

If installed with pip or Homebrew:
```bash
crondash doctor          # System health check
crondash list            # Show all tasks with status
crondash next            # Show next scheduled runs (requires croniter)
crondash tools            # List available optional tools
crondash run             # Execute scheduled tasks now (requires croniter)
```

If running from repo:
```bash
./crondash.cli list
./crondash.cli doctor
./crondash.cli next
./crondash.cli tools
./crondash.cli install-pip
./crondash.cli install-brew
```

---

## 📝 Features
- Minimal dependencies: core commands work with just Python 3.9+
- Optional: `croniter` and `pyyaml` enable advanced features
- macOS LaunchAgent integration supported
- All configuration in `config.yaml`
- Optional tools in `tools/` directory with YAML configuration

---

## 📦 Project Links
- GitHub: https://github.com/git-steb/crondash

---

## 📁 Project Structure

```
crondash/
├── crondash/                    # Main Python package
│   ├── __init__.py             # Package initialization
│   └── cli.py                  # Core CLI implementation
├── crondash.cli                # CLI entry point script
├── cronshim.py                 # Legacy cron wrapper (deprecated)
├── crontab/                    # Crontab examples and templates
│   └── mycrontab.txt           # Example crontab entries
├── launch_agents/              # macOS LaunchAgent integration
│   └── com.example.crondash.plist  # LaunchAgent plist template
├── tools/                      # Optional utility tools
│   └── disk_watch.py           # Disk usage monitoring tool
├── env/                        # Environment configuration
│   └── environment.yml         # Conda environment (optional)
├── Pipfile                     # Pipenv dependencies (optional)
├── pyproject.toml              # Python package configuration
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── LICENSE                     # MIT license
```

### Key Files Explained

**Core Package:**
- `crondash/cli.py` - Main CLI implementation with commands like `list`, `doctor`, `next`, `run`
- `crondash.cli` - Executable script that can be run directly from repo or installed system-wide

**Configuration:**
- `config.yaml` - Central configuration file (created in `~/.crondash/` on first run)
- `~/.crondash/crontab.txt` - Mutable scheduler state (not versioned, symlinked as `dot-crontab`)

**System Integration:**
- `launch_agents/com.example.crondash.plist` - macOS LaunchAgent template for system integration
- `crontab/mycrontab.txt` - Example crontab entries for traditional cron integration

**Optional Tools:**
- `tools/disk_watch.py` - Disk usage monitoring with YAML configuration for suggested schedules

**Package Management:**
- `pyproject.toml` - Modern Python package configuration
- `requirements.txt` - Minimal dependencies (Python 3.8+ compatible)
- `Pipfile` - Alternative dependency management (optional)

**Installation:**
- `crondash.rb` - Homebrew formula for system-wide installation
- `env/environment.yml` - Conda environment (optional)

---

## 🪄 Example

```bash
crondash doctor
crondash list
```

--- 

## License
MIT 