"""Universal cell: support (FAQ, help, contact)."""


def cell(config: dict) -> dict:
    """Return support/help cell."""
    slug = config["business"]["slug"]

    source = [
        "# @title Support\n",
        "from IPython.display import HTML, display\n",
        f"display(HTML('<details style=\"margin:8px 0;font-family:Inter,system-ui,sans-serif;color:#f1f5f9\"><summary style=\"cursor:pointer;font-weight:500\">Quick Start</summary><ol style=\"color:#94a3b8;font-size:13px;padding-left:20px\"><li>Run Setup with your API key</li><li>Work through sections</li><li>Files saved to Google Drive</li></ol></details><details style=\"margin:8px 0;font-family:Inter,system-ui,sans-serif;color:#f1f5f9\"><summary style=\"cursor:pointer;font-weight:500\">FAQ</summary><p style=\"color:#94a3b8;font-size:13px\"><b>Files?</b> Drive > pysolvr > {slug}</p><p style=\"color:#94a3b8;font-size:13px\"><b>Help?</b> support@pysolvr.com</p></details>'))",
    ]

    return {
        "cell_type": "code",
        "metadata": {
            "cellView": "form",
            "pysolvr": {"cell_type": "universal", "cell_id": "support"},
        },
        "source": source,
        "execution_count": None,
        "outputs": [],
    }
