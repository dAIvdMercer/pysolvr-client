"""Universal cell: subscription (manage plan)."""


def cell(config: dict) -> dict:
    """Return subscription management cell."""
    source = [
        "# @title Subscription\n",
        "# @markdown Manage your plan\n",
        "ACTION = 'View Current Plan'  # @param ['View Current Plan', 'Upgrade', 'Downgrade', 'Pause', 'Resume', 'Cancel']\n",
        "from IPython.display import clear_output\n",
        "\n",
        "if ACTION == 'View Current Plan':\n",
        "    result = client.call('GET', '/subscription')\n",
        "    if result['ok']:\n",
        "        d = result['data']\n",
        "        ui.card('Current Plan', f\"<b>{d.get('plan', 'Free')}</b> - ${d.get('price_usd', 0)}/mo<br>Renews: {d.get('renewal_date', 'N/A')}<br>Status: {d.get('status', 'active')}\", status='success')\n",
        "    else:\n",
        "        ui.error(result.get('error', 'Could not fetch subscription'))\n",
        "elif ACTION == 'Cancel':\n",
        "    confirm = input('Type CANCEL to confirm: ')\n",
        "    if confirm == 'CANCEL':\n",
        "        result = client.call('POST', '/subscription', {'action': 'cancel'})\n",
        "        ui.success('Subscription cancelled') if result['ok'] else ui.error(result.get('error'))\n",
        "    else:\n",
        "        ui.card('Cancelled', 'No changes made')\n",
        "else:\n",
        "    action_map = {'Upgrade': 'upgrade', 'Downgrade': 'downgrade', 'Pause': 'pause', 'Resume': 'resume'}\n",
        "    result = client.call('POST', '/subscription', {'action': action_map[ACTION]})\n",
        "    if result['ok']:\n",
        "        ui.success(f'{ACTION} successful', result['data'].get('message', ''))\n",
        "    else:\n",
        "        ui.error(result.get('error', f'{ACTION} failed'), 'Check your current plan allows this action')",
    ]

    return {
        "cell_type": "code",
        "metadata": {
            "cellView": "form",
            "pysolvr": {"cell_type": "universal", "cell_id": "subscription"},
        },
        "source": source,
        "execution_count": None,
        "outputs": [],
    }
