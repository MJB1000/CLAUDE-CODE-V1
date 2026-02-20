"""Gather project file context to include in the prompt."""

from __future__ import annotations

from pathlib import Path

from .config import ProjectContextConfig


def gather_context(project_dir: Path, ctx_config: ProjectContextConfig) -> str:
    """Read project files matching the include/exclude globs and return them as
    a single string block, truncated to max_context_chars."""
    matched_files: list[Path] = []

    for pattern in ctx_config.include:
        matched_files.extend(project_dir.glob(pattern))

    # Deduplicate and sort for deterministic output.
    matched_files = sorted(set(matched_files))

    # Filter out excluded patterns.
    def is_excluded(file: Path) -> bool:
        rel = file.relative_to(project_dir)
        return any(rel.match(exc) for exc in ctx_config.exclude)

    matched_files = [f for f in matched_files if f.is_file() and not is_excluded(f)]

    parts: list[str] = []
    total_chars = 0

    for file in matched_files:
        try:
            content = file.read_text(errors="replace")
        except OSError:
            continue

        rel_path = file.relative_to(project_dir)
        block = f"--- {rel_path} ---\n{content}\n"

        if total_chars + len(block) > ctx_config.max_context_chars:
            remaining = ctx_config.max_context_chars - total_chars
            if remaining > 100:
                parts.append(block[:remaining] + "\n... (truncated)")
            break

        parts.append(block)
        total_chars += len(block)

    return "\n".join(parts)
