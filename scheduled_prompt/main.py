"""Entry point: run the prompt once immediately, or start the scheduler."""

from __future__ import annotations

import argparse
import signal
import sys
from pathlib import Path

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from .config import load_config
from .runner import run_prompt

DAY_MAP = {
    "monday": "mon",
    "tuesday": "tue",
    "wednesday": "wed",
    "thursday": "thu",
    "friday": "fri",
    "saturday": "sat",
    "sunday": "sun",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Deploy a Claude prompt on a recurring schedule."
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=Path("config.yaml"),
        help="Path to the YAML config file (default: config.yaml)",
    )
    parser.add_argument(
        "-p",
        "--project-dir",
        type=Path,
        default=Path("."),
        help="Root directory of the project to analyze (default: current directory)",
    )
    parser.add_argument(
        "--run-once",
        action="store_true",
        help="Run the prompt once immediately and exit (skip scheduling)",
    )
    return parser


def scheduled_job(config_path: Path, project_dir: Path) -> None:
    """Job function invoked by APScheduler on each tick."""
    config = load_config(config_path)
    try:
        run_prompt(config, project_dir.resolve())
    except Exception as e:
        print(f"Error running prompt: {e}", file=sys.stderr)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    config = load_config(args.config)
    project_dir = args.project_dir.resolve()

    if args.run_once:
        run_prompt(config, project_dir)
        return

    # Parse schedule.
    hour, minute = config.schedule.time.split(":")
    days_of_week = ",".join(
        DAY_MAP.get(d.lower(), d.lower()[:3]) for d in config.schedule.days
    )

    trigger = CronTrigger(
        day_of_week=days_of_week,
        hour=int(hour),
        minute=int(minute),
        timezone=config.schedule.timezone,
    )

    scheduler = BlockingScheduler()
    scheduler.add_job(
        scheduled_job,
        trigger=trigger,
        args=[args.config, project_dir],
        id="scheduled_prompt",
        name="Scheduled Claude Prompt",
        misfire_grace_time=3600,
    )

    # Graceful shutdown on SIGINT / SIGTERM.
    def shutdown(signum, frame):
        print("\nShutting down scheduler...")
        scheduler.shutdown(wait=False)
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    print(
        f"Scheduler started. Prompt will run at {config.schedule.time} "
        f"{config.schedule.timezone} on {', '.join(config.schedule.days)}."
    )
    print("Press Ctrl+C to stop.\n")
    scheduler.start()


if __name__ == "__main__":
    main()
