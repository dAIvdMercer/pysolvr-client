"""Universal cell: account (subscription, usage, support tabs)."""


def cell(config: dict) -> dict:
    """Return account management cell with tabbed output."""
    slug = config["business"]["slug"]
    name = config["business"]["name"]
    domain = config.get("site", {}).get("domain", f"{slug}.pysolvr.com")

    source = [
        "# @title Account\n",
        "result_acct = client.call('GET', '/account')\n",
        "result_usage = client.get_usage()\n",
        "\n",
        "sub_html = ''\n",
        "if result_acct['ok']:\n",
        "    d = result_acct['data']\n",
        "    sub_html = (f\"<b>{d.get('plan', 'Free')}</b><br>\"\n",
        "        f\"Status: {d.get('status', 'active')}<br>\"\n",
        f"        f\"<a href='https://{domain}/pricing' style='color:#60a5fa'>Manage plan</a>\")\n",
        "else:\n",
        "    sub_html = f\"<span style='color:#f87171'>{result_acct.get('error', 'Could not fetch account')}</span>\"\n",
        "\n",
        "usage_html = ''\n",
        "if result_usage['ok']:\n",
        "    data = result_usage['data']\n",
        "    usage_html = ui.usage_bar_html(data.get('current_month_spend_usd', 0), data.get('monthly_limit_usd', 1))\n",
        "else:\n",
        "    usage_html = f\"<span style='color:#f87171'>{result_usage.get('error', 'Could not fetch usage')}</span>\"\n",
        "\n",
        f"support_html = ('<p><b>Files:</b> Google Drive > pysolvr > {slug}</p>'\n",
        f"    '<p><b>Docs:</b> <a href=\"https://{domain}/docs\" style=\"color:#60a5fa\">{domain}/docs</a></p>'\n",
        f"    '<p><b>Support:</b> <a href=\"mailto:support@pysolvr.com?subject={name}\" style=\"color:#60a5fa\">support@pysolvr.com</a></p>')\n",
        "\n",
        "ui.tabs({'Subscription': sub_html, 'Usage': usage_html, 'Support': support_html})\n",
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
