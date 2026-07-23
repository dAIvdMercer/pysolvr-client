"""Universal cell: support ticket submission."""


def cell(config: dict) -> dict:
    slug = config["business"]["slug"]
    name = config["business"]["name"]

    source = [
        "# @title Support\n",
        "import ipywidgets as _w\n",
        "from IPython.display import display as _display\n",
        "\n",
        "_type_dd = _w.Dropdown(\n",
        "    options=['question', 'bug', 'feature_request', 'feedback', 'billing', 'data_request'],\n",
        "    description='Type:',\n",
        "    layout=_w.Layout(width='320px'),\n",
        ")\n",
        "_text = _w.Textarea(\n",
        "    placeholder='Describe your issue or feedback...',\n",
        "    layout=_w.Layout(width='480px', height='120px'),\n",
        ")\n",
        "_btn = _w.Button(description='Submit', button_style='primary')\n",
        "_out = _w.Output()\n",
        "\n",
        "def _on_submit(b):\n",
        "    _out.clear_output()\n",
        "    with _out:\n",
        "        if not _text.value.strip():\n",
        "            display(ui.warning_html('Please describe your issue before submitting.'))\n",
        "            return\n",
        "        result = client.call('POST', '/support', body={\n",
        "            'type': _type_dd.value,\n",
        f"            'feature_tag': '{slug}',\n",
        "            'free_text': _text.value.strip(),\n",
        "        })\n",
        "        if result['ok']:\n",
        "            display(ui.success_html(f\"Ticket submitted. Reference: {result['data']['ticket_id']}\"))\n",
        "            _text.value = ''\n",
        "        else:\n",
        "            display(ui.error_html(result.get('error', 'Submission failed. Please try again.')))\n",
        "\n",
        "_btn.on_click(_on_submit)\n",
        f"_display(ui.card_html('<b>Contact support for {name}</b><br><small>We typically respond within 24 hours.</small>'))\n",
        "_display(_w.VBox([_type_dd, _text, _btn, _out]))\n",
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
