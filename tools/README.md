# crondash Tools

This directory contains optional tools that can be scheduled with crondash.

## Available Tools

### disk_watch
Monitors disk usage and Docker storage consumption.

**Configuration:** `disk_watch.yaml`
**Script:** `disk_watch.py`

**To enable:**
1. Add to your crontab (`crontab/mycrontab.txt`):
   ```
   0 9 * * * /usr/bin/python3 tools/disk_watch.py
   ```
2. Or use the suggested schedule from `disk_watch.yaml`

**What it monitors:**
- System volume disk usage
- Docker storage consumption  
- System library assets size

## Adding New Tools

1. Create your tool script (e.g., `my_tool.py`)
2. Create a YAML config (e.g., `my_tool.yaml`) with:
   - Suggested schedules
   - Description
   - Example crontab entry
3. Add to your crontab when ready to use

## Tool Configuration Format

```yaml
name: "tool_name"
description: "What this tool does"
script: "script.py"
suggested_schedules:
  daily: "0 9 * * *"
  weekly: "0 9 * * 0"
default_schedule: "0 9 * * *"
example_crontab: "0 9 * * * /usr/bin/python3 tools/script.py"
``` 