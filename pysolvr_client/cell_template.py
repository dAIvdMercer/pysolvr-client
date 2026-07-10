"""Cell template - enforces notebook cell structure and styling.

Business cells declare content. This module handles packaging into notebook JSON.
"""
import inspect
import textwrap


def cell_template(title: str, instructions=None, form_fields=None, execute=None) -> dict:
    """Build a notebook cell dict from declared content.

    Args:
        title: Cell title (sentence case, e.g. "Compare models")
        instructions: str, list of str (bullets), or None
        form_fields: list of @param lines (plain python assignment strings)
        execute: function containing the cell logic (source is extracted)

    Returns:
        dict: valid notebook cell (cell_type, metadata, source, etc.)
    """
    source = []

    # Title
    source.append(f"# @title {title}\n")

    # Instructions (normal font markdown - no --- separators, no bold)
    if instructions:
        if isinstance(instructions, str):
            source.append(f"# @markdown {instructions}\n")
        elif isinstance(instructions, list):
            for line in instructions:
                source.append(f"# @markdown {line}\n")

    # Form fields
    if form_fields:
        for field in form_fields:
            source.append(f"{field}\n")
        source.append("\n")

    # Execute function body (extracted, dedented)
    if execute:
        body = _extract_body(execute)
        for line in body:
            source.append(f"{line}\n")

    return {
        "cell_type": "code",
        "metadata": {
            "cellView": "form",
            "pysolvr": {"cell_type": "business", "cell_id": title.lower().replace(" ", "_")},
        },
        "source": source,
        "execution_count": None,
        "outputs": [],
    }


def _extract_body(func) -> list:
    """Extract the body lines of a function (skip def line, dedent)."""
    src = inspect.getsource(func)
    lines = src.splitlines()

    # Skip def line and any decorators
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("def "):
            body_start = i + 1
            break

    body_lines = lines[body_start:]

    # Skip docstring if present
    if body_lines and body_lines[0].strip().startswith(('"""', "'''")):
        # Single or multi-line docstring
        if body_lines[0].strip().count('"""') >= 2 or body_lines[0].strip().count("'''") >= 2:
            body_lines = body_lines[1:]
        else:
            quote = body_lines[0].strip()[:3]
            for i in range(1, len(body_lines)):
                if quote in body_lines[i]:
                    body_lines = body_lines[i + 1:]
                    break

    # Dedent
    dedented = textwrap.dedent("\n".join(body_lines))
    return dedented.splitlines()
