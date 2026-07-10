"""Universal cell: account (subscription, usage, support tabs)."""


def cell(config: dict) -> dict:
    """Return account management cell with tabbed output."""
    slug = config["business"]["slug"]
    name = config["business"]["name"]
    domain = config.get("site", {}).get("domain", f"{slug}.pysolvr.com")

    source = [
        "# @title Account\n",
        "# @markdown Subscription, usage, and support\n",
        f"ACTION = 'Subscription'  # @param [\"Subscription\", \"Usage\", \"Support\"]\n",
        "\n",
        "if ACTION == 'Subscription':\n",
        "    result = client.call('GET', '/account')\n",
        "    if result['ok']:\n",
        "        d = result['data']\n",
        "        ui.card('Subscription', f\"<b>{d.get('plan', 'Free')}</b><br>\"\n",
        f"            f\"Status: {{d.get('status', 'active')}}<br>\"\n",
        f"            f\"<a href='https://{domain}/pricing' style='color:#60a5fa'>Manage plan</a>\",\n",
        "            status='success')\n",
        "    else:\n",
        "        ui.error(result.get('error', 'Could not fetch account'), actions=result.get('actions'))\n",
        "\n",
        "elif ACTION == 'Usage':\n",
        "    result = client.get_usage()\n",
        "    if result['ok']:\n",
        "        data = result['data']\n",
        "        ui.usage_bar(data.get('current_month_spend_usd', 0), data.get('monthly_limit_usd', 1))\n",
        "        if data.get('recent'):\n",
        "            ui.table(data['recent'])\n",
        "    else:\n",
        "        ui.error(result.get('error', 'Could not fetch usage'), actions=result.get('actions'))\n",
        "\n",
        "elif ACTION == 'Support':\n",
        "    from IPython.display import HTML, display\n",
        f"    display(HTML('<div style=\"font-family:Inter,system-ui,sans-serif;color:#f1f5f9;font-size:13px\">'\n",
        f"        '<p><b>Files:</b> Google Drive > pysolvr > {slug}</p>'\n",
        f"        '<p><b>Docs:</b> <a href=\"https://{domain}/docs\" style=\"color:#60a5fa\">https://{domain}/docs</a></p>'\n",
        f"        '<p><b>Support:</b> <a href=\"mailto:support@pysolvr.com?subject={name}\" style=\"color:#60a5fa\">support@pysolvr.com</a></p>'\n",
        "        '</div>'))\n",
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
