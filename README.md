# Scheduled Claude Prompt Deployment

Run a Claude prompt against a specific project on a recurring schedule (e.g. every weekday at 9 AM). The tool gathers project files as context, sends the prompt to Claude, and saves the response.

## Setup

```bash
# Install dependencies
pip install -e .

# Set your Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Configuration

Edit `config.yaml` to set:

- **prompt** — the prompt text sent to Claude each run
- **system_prompt** — the system prompt that frames the conversation
- **schedule.time** — time of day in 24h format (e.g. `"09:00"`)
- **schedule.timezone** — IANA timezone (e.g. `"US/Eastern"`, `"UTC"`)
- **schedule.days** — which days of the week to run
- **model.name** — Claude model ID (default: `claude-opus-4-6`)
- **project_context.include** — glob patterns for files to include as context
- **project_context.exclude** — glob patterns for files to skip
- **output.directory** — where to save response files

## Usage

### Run once immediately

```bash
scheduled-prompt --run-once --project-dir /path/to/your/project
```

### Start the scheduler (runs continuously)

```bash
scheduled-prompt --config config.yaml --project-dir /path/to/your/project
```

This keeps running in the foreground and fires the prompt at the configured time each day. Use a process manager (systemd, supervisor, Docker) or `nohup` to run it in the background.

### Run as a systemd service

```ini
# /etc/systemd/system/scheduled-prompt.service
[Unit]
Description=Scheduled Claude Prompt
After=network.target

[Service]
Type=simple
User=deploy
WorkingDirectory=/opt/scheduled-prompt
ExecStart=/opt/scheduled-prompt/.venv/bin/scheduled-prompt --config config.yaml --project-dir /path/to/project
Environment=ANTHROPIC_API_KEY=sk-ant-...
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Run with cron (alternative)

If you prefer system cron over APScheduler:

```cron
0 9 * * 1-5 cd /opt/scheduled-prompt && /opt/scheduled-prompt/.venv/bin/scheduled-prompt --run-once --project-dir /path/to/project
```

## Output

Each run creates a timestamped Markdown file in the output directory (default: `prompt_outputs/`):

```
prompt_outputs/
  response_20260220_090001.md
  response_20260221_090003.md
```
