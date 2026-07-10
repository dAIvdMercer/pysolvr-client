"""Universal cell: account (subscription, usage, support tabs)."""


def cell(config: dict) -> dict:
    """Return account management cell with tabbed output."""
    slug = config["business"]["slug"]
    name = config["business"]["name"]
    domain = config.get("site", {}).get("domain", f"{slug}.pysolvr.com")

    source = [
        "# @title Account\n",
        "\n",
        "_tab_out = [widgets.Output() for _ in range(3)]\n",
        "_tabs = widgets.Tab(children=_tab_out)\n",
        "_tabs.set_title(0, 'Subscription')\n",
        "_tabs.set_title(1, 'Usage')\n",
        "_tabs.set_title(2, 'Support')\n",
        "\n",
        "# Subscription tab\n",
        "with _tab_out[0]:\n",
        "    result = client.call('GET', '/account')\n",
        "    if result['ok']:\n",
        "        d = result['data']\n",
        "        ui.card('Subscription', f\"<b>{d.get('plan', 'Free').title()}</b><br>\"\n",
        f"            f\"Status: {{d.get('status', 'active')}}<br>\"\n",
        f"            f\"<a href='https://{domain}/pricing' style='color:#60a5fa'>Manage plan</a>\",\n",
        "            status='success')\n",
        "    else:\n",
        "        ui.error(result.get('error', 'Could not fetch account'))\n",
        "\n",
        "# Usage tab\n",
        "with _tab_out[1]:\n",
        "    result = client.get_usage()\n",
        "    if result['ok']:\n",
        "        data = result['data']\n",
        "        ui.usage_bar(data.get('monthly_spend_usd', 0), data.get('monthly_limit_usd', 1))\n",
        "    else:\n",
        "        ui.error(result.get('error', 'Could not fetch usage'))\n",
        "\n",
        "# Support tab\n",
        "with _tab_out[2]:\n",
        f"    display(HTML('<div style=\"font-family:Inter,system-ui,sans-serif;color:#f1f5f9;font-size:13px;padding:8px\">'\n",
        f"        '<p><b>Files:</b> Google Drive > pysolvr > {slug}</p>'\n",
        f"        '<p><b>Docs:</b> <a href=\"https://{domain}/docs\" style=\"color:#60a5fa\">https://{domain}/docs</a></p>'\n",
        f"        '<p><b>Support:</b> <a href=\"mailto:support@pysolvr.com?subject={name}\" style=\"color:#60a5fa\">support@pysolvr.com</a></p>'\n",
        "        '</div>'))\n",
        "\n",
        "display(_tabs)\n",
    ]

    return {
        "cell_type": "code",
        "metadata": {
            "cellView": "form",
            "pysolvr": {"cell_type": "universal", "cell_id": "account"},
        },
        "source": source,
        "execution_count": None,
        "outputs": [],
    }
