"""Universal cell: setup (install, auth, drive, health check)."""


def cell(config: dict) -> dict:
    """Return notebook setup cell. Must be run every session."""
    slug = config["business"]["slug"]
    slug_upper = slug.upper().replace("-", "_")
    name = config["business"]["name"]
    primary_color = config.get("growth", {}).get("site", {}).get("style", {}).get("primary_color", "#4F46E5")
    accent_color = config.get("growth", {}).get("site", {}).get("style", {}).get("accent_color", "#10B981")
    folders = config.get("notebook", {}).get("drive_structure", {}).get("folders", [])
    folders_str = ", ".join(f"'{f}'" for f in folders)

    source = [
        "# @title Setup\n",
        "# @markdown **Run this cell every session.** First time? See instructions below.\n",
        "# @markdown ---\n",
        f"# @markdown **First time setup:** [Getting started guide](https://{slug}.pysolvr.com/docs/getting-started) |\n",
        f"# @markdown Save a copy: File > Save a copy in Drive |\n",
        f"# @markdown Add API key: click key icon (left sidebar) > add `{slug_upper}_API_KEY`\n",
        "# @markdown ---\n",
        "!pip install -q pysolvr-client\n",
        "import sys\n",
        "from google.colab import userdata, drive\n",
        "\n",
        "try:\n",
        f"    API_KEY = userdata.get('{slug_upper}_API_KEY')\n",
        "except userdata.SecretNotFoundError:\n",
        "    from IPython.display import HTML, display\n",
        f"    display(HTML('<div style=\"background:#1e293b;border:1px solid #ef4444;border-radius:8px;padding:16px;font-family:Inter,system-ui,sans-serif;color:#f1f5f9\"><b style=\"color:#ef4444\">API key not found in Colab Secrets</b><ol style=\"color:#94a3b8;font-size:13px;margin-top:8px\"><li>Click the key icon in the left sidebar</li><li>Add secret: <code>{slug_upper}_API_KEY</code></li><li>Paste your API key as the value</li><li>Toggle Notebook access ON</li><li>Re-run this cell</li></ol></div>'))\n",
        "    assert False, 'API key not configured - see instructions above'\n",
        "\n",
        "drive.mount('/content/drive', force_remount=False)\n",
        "sys.path.insert(0, '/content')\n",
        "\n",
        "from pysolvr_client import ApiClient, Display, DriveManager\n",
        "\n",
        f"API_BASE = 'https://{slug}.pysolvr.com/api'\n",
        "client = ApiClient(API_BASE, API_KEY)\n",
        f"ui = Display('{primary_color}', '{accent_color}')\n",
        f"drive_mgr = DriveManager('{slug}', [{folders_str}])\n",
        "drive_mgr.ensure_folders()\n",
        "\n",
        "if client.health_check():\n",
        f"    ui.success('Connected to {name} API', f'Drive: {{drive_mgr.root}}')\n",
        "else:\n",
        "    ui.error('Could not connect to API', 'Check your API key and try again')",
    ]

    return {
        "cell_type": "code",
        "metadata": {
            "cellView": "form",
            "pysolvr": {"cell_type": "universal", "cell_id": "setup"},
        },
        "source": source,
        "execution_count": None,
        "outputs": [],
    }
