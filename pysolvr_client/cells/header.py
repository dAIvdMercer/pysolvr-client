"""Universal cell: header (markdown, renders immediately on open)."""


def cell(config: dict) -> dict:
    """Return notebook header cell. No code execution required."""
    name = config["business"]["name"]
    description = config["business"]["description"]
    version = config["notebook"]["version"]

    return {
        "cell_type": "markdown",
        "metadata": {"pysolvr": {"cell_type": "universal", "cell_id": "header"}},
        "source": [
            f"# {name}\n",
            f"> {description}\n",
            "\n",
            f"*v{version}*",
        ],
    }
