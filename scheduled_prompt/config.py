"""Load and validate the YAML configuration."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class ScheduleConfig:
    time: str = "09:00"
    timezone: str = "UTC"
    days: list[str] = field(
        default_factory=lambda: [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
        ]
    )


@dataclass
class ModelConfig:
    name: str = "claude-opus-4-6"
    max_tokens: int = 4096


@dataclass
class ProjectContextConfig:
    include: list[str] = field(default_factory=lambda: ["*.md", "src/**/*.py"])
    exclude: list[str] = field(
        default_factory=lambda: ["**/__pycache__/**", "*.pyc", ".git/**"]
    )
    max_context_chars: int = 100_000


@dataclass
class OutputConfig:
    directory: str = "prompt_outputs"
    print_stdout: bool = True


@dataclass
class AppConfig:
    prompt: str = "Summarize the current state of this project."
    system_prompt: str = "You are a project analyst. Be concise and actionable."
    schedule: ScheduleConfig = field(default_factory=ScheduleConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    project_context: ProjectContextConfig = field(
        default_factory=ProjectContextConfig
    )
    output: OutputConfig = field(default_factory=OutputConfig)


def load_config(config_path: Path) -> AppConfig:
    """Load configuration from a YAML file."""
    if not config_path.exists():
        print(f"Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path) as f:
        raw = yaml.safe_load(f) or {}

    schedule_raw = raw.get("schedule", {})
    model_raw = raw.get("model", {})
    context_raw = raw.get("project_context", {})
    output_raw = raw.get("output", {})

    schedule = ScheduleConfig(
        time=schedule_raw.get("time", "09:00"),
        timezone=schedule_raw.get("timezone", "UTC"),
        days=schedule_raw.get("days", ScheduleConfig().days),
    )

    model = ModelConfig(
        name=model_raw.get("name", "claude-opus-4-6"),
        max_tokens=model_raw.get("max_tokens", 4096),
    )

    project_context = ProjectContextConfig(
        include=context_raw.get("include", ProjectContextConfig().include),
        exclude=context_raw.get("exclude", ProjectContextConfig().exclude),
        max_context_chars=context_raw.get("max_context_chars", 100_000),
    )

    output = OutputConfig(
        directory=output_raw.get("directory", "prompt_outputs"),
        print_stdout=output_raw.get("print_stdout", True),
    )

    return AppConfig(
        prompt=raw.get("prompt", AppConfig().prompt),
        system_prompt=raw.get("system_prompt", AppConfig().system_prompt),
        schedule=schedule,
        model=model,
        project_context=project_context,
        output=output,
    )
