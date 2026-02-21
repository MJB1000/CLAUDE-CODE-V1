"""Execute the Claude prompt and handle the response."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic

from .config import AppConfig
from .context import gather_context


def run_prompt(config: AppConfig, project_dir: Path) -> str:
    """Send the configured prompt to Claude and return the response text."""
    import os

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "Error: ANTHROPIC_API_KEY environment variable is not set.\n"
            "Set it with: export ANTHROPIC_API_KEY='sk-ant-...'",
            file=sys.stderr,
        )
        sys.exit(1)

    client = anthropic.Anthropic()

    # Build project context.
    context_text = gather_context(project_dir, config.project_context)

    # Assemble the user message: the prompt plus any project context.
    user_content = config.prompt.strip()
    if context_text:
        user_content += (
            "\n\n<project-context>\n" + context_text + "\n</project-context>"
        )

    print(
        f"[{datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S UTC}] "
        f"Sending prompt to {config.model.name}..."
    )

    try:
        with client.messages.stream(
            model=config.model.name,
            max_tokens=config.model.max_tokens,
            thinking={"type": "adaptive"},
            system=config.system_prompt.strip(),
            messages=[{"role": "user", "content": user_content}],
        ) as stream:
            response = stream.get_final_message()
    except anthropic.AuthenticationError:
        print("Error: Invalid ANTHROPIC_API_KEY.", file=sys.stderr)
        sys.exit(1)
    except anthropic.APIConnectionError as e:
        print(f"Error: Could not connect to Claude API: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract text from response content blocks.
    text_parts: list[str] = []
    for block in response.content:
        if block.type == "text":
            text_parts.append(block.text)

    response_text = "\n".join(text_parts)

    # Print to stdout if configured.
    if config.output.print_stdout:
        print("\n" + "=" * 60)
        print("CLAUDE RESPONSE")
        print("=" * 60)
        print(response_text)
        print("=" * 60)
        print(
            f"Tokens — input: {response.usage.input_tokens}, "
            f"output: {response.usage.output_tokens}"
        )

    # Save to file.
    save_response(config, project_dir, response_text)

    return response_text


def save_response(config: AppConfig, project_dir: Path, response_text: str) -> None:
    """Write the response to a timestamped file in the output directory."""
    output_dir = project_dir / config.output.directory
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"response_{timestamp}.md"
    output_file.write_text(
        f"# Scheduled Prompt Response\n\n"
        f"**Date:** {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S UTC}\n"
        f"**Model:** {config.model.name}\n\n"
        f"---\n\n"
        f"{response_text}\n"
    )
    print(f"Response saved to {output_file}", file=sys.stderr)
