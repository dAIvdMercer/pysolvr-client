"""Universal cell: usage (spend, limits, visual bar)."""


def cell(config: dict) -> dict:
    """Return usage display cell."""
    source = [
        "# @title Usage\n",
        "result = client.get_usage()\n",
        "if result['ok']:\n",
        "    data = result['data']\n",
        "    ui.usage_bar(data.get('current_month_spend_usd', 0), data.get('monthly_limit_usd', 1))\n",
        "    if data.get('recent'):\n",
        "        ui.table(data['recent'])\n",
        "else:\n",
        "    ui.error(result.get('error', 'Could not fetch usage'), 'Check your API key')",
    ]

    return {
        "cell_type": "code",
        "metadata": {
            "cellView": "form",
            "pysolvr": {"cell_type": "universal", "cell_id": "usage"},
        },
        "source": source,
        "execution_count": None,
        "outputs": [],
    }
