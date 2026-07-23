"""Universal cell: account (subscription, usage, support, version tabs)."""


def cell(config: dict) -> dict:
    """Return account management cell with tabbed output."""
    slug = config["business"]["slug"]
    name = config["business"]["name"]
    domain = config.get("site", {}).get("domain", f"{slug}.pysolvr.com")
    version = config["notebook"]["version"]
    public_repo = config["business"].get("public_repo", f"{slug}-client")
    changelog_url = f"https://github.com/dAIvdMercer/{public_repo}/blob/main/CHANGELOG.md"
    raw_changelog_url = f"https://raw.githubusercontent.com/dAIvdMercer/{public_repo}/main/CHANGELOG.md"

    source = [
        "# @title Account\n",
        "import requests as _req\n",
        "result_acct = client.call('GET', '/account')\n",
        "result_usage = client.get_usage()\n",
        "\n",
        "sub_html = ''\n",
        "if result_acct['ok']:\n",
        "    d = result_acct['data']\n",
        "    plan_label = d.get('plan', 'free').capitalize()\n",
        "    limits = d.get('tier_limits', {})\n",
        "    def _fmt(v):\n",
        "        if v == 0: return 'Unlimited'\n",
        "        if v == 'none': return 'Not included'\n",
        "        return str(v)\n",
        "    limits_rows = ''.join(f\"<tr><td style='padding:3px 8px 3px 0;color:#94a3b8;text-transform:capitalize'>{k.replace('_', ' ')}</td><td style='padding:3px 0;color:#e2e8f0'>{_fmt(v)}</td></tr>\" for k, v in limits.items())\n",
        "    limits_html = f\"<table style='border-collapse:collapse;margin-top:6px'>{limits_rows}</table>\" if limits_rows else ''\n",
        f"    topup = f\"Top-up balance: ${{d.get('topup_balance_usd', 0):.2f}}<br>\" if d.get('topup_balance_usd') else ''\n",
        f"    sub_html = f\"<b>{{plan_label}}</b><br>Status: {{d.get('status', 'active')}}<br>Monthly limit: ${{d.get('monthly_limit_usd', 0):.2f}}<br>{{topup}}<br><b>Plan limits</b>{{limits_html}}<br><a href='https://{domain}/pricing' style='color:#60a5fa'>Manage plan</a>\"\n",
        "else:\n",
        "    sub_html = f\"<span style='color:#f87171'>{result_acct.get('error', 'Could not fetch account')}</span>\"\n",
        "\n",
        "usage_html = ''\n",
        "if result_usage['ok']:\n",
        "    data = result_usage['data']\n",
        "    limit = result_acct['data'].get('monthly_limit_usd', 1) if result_acct['ok'] else 1\n",
        "    usage_html = ui.usage_bar_html(data.get('current_month_spend_usd', 0), limit)\n",
        "else:\n",
        "    usage_html = f\"<span style='color:#f87171'>{result_usage.get('error', 'Could not fetch usage')}</span>\"\n",
        "\n",
        f"support_html = ('<p><b>Files:</b> Google Drive > pysolvr > {slug}</p>'\n",
        f"    '<p><b>Docs:</b> <a href=\"https://{domain}/docs\" style=\"color:#60a5fa\">{domain}/docs</a></p>')\n",
        "\n",
        f"_current_ver = '{version}'\n",
        "_latest_ver = _current_ver\n",
        "try:\n",
        f"    _cl = _req.get('{raw_changelog_url}', timeout=5).text\n",
        "    import re as _re\n",
        "    _m = _re.search(r'## (\\d+\\.\\d+\\.\\d+)', _cl)\n",
        "    if _m: _latest_ver = _m.group(1)\n",
        "except: pass\n",
        "\n",
        "_cur_parts = tuple(int(x) for x in _current_ver.split('.'))\n",
        "_lat_parts = tuple(int(x) for x in _latest_ver.split('.'))\n",
        "if _lat_parts <= _cur_parts:\n",
        "    _ver_status = '<span style=\"color:#10b981\">Up to date</span>'\n",
        "else:\n",
        "    _ver_status = f'<span style=\"color:#f59e0b\">Update available: v{_latest_ver}</span><br><small>Save a fresh copy from the link below</small>'\n",
        f"version_html = (f'<p><b>Current:</b> v{{_current_ver}}</p>'\n",
        f"    f'<p><b>Latest:</b> v{{_latest_ver}} -- {{_ver_status}}</p>'\n",
        f"    '<p><a href=\"{changelog_url}\" style=\"color:#60a5fa\">View changelog</a></p>')\n",
        "\n",
        "rotate_html = (\n",
        "    '<p>Generates a new API key and emails it to the address you subscribed with.</p>'\n",
        "    '<p style=\"color:#f59e0b\">Make sure you have access to that inbox before rotating -- "
        "your current key stops working immediately.</p>'\n",
        "    '<button onclick=\"(function(){"
        "var r=confirm(\\\"Rotate your API key? Your current key will stop working immediately.\\\");"
        "if(r){IPython.notebook.kernel.execute(\\\"_rotate=client.call(\\\\\\\"POST\\\\\\\",\\\\\\\"/account/rotate-key\\\\\\\");print(_rotate.get(\\\\\\\"data\\\\\\\",{}).get(\\\\\\\"message\\\\\\\",_rotate.get(\\\\\\\"error\\\\\\\",\\\\\\\"Unknown error\\\\\\\")))\\\")}})()\""
        " style=\"background:#dc2626;color:white;border:none;padding:8px 16px;border-radius:4px;cursor:pointer;margin-top:8px\">Rotate API key</button>')\n",
        "\n",
        "import ipywidgets as _w\n",
        "from IPython.display import display as _display\n",
        "_acct_out = _w.Output()\n",
        "_display(_acct_out)\n",
        "_type_dd = _w.Dropdown(\n",
        "    options=['question', 'bug', 'feature_request', 'feedback', 'billing', 'data_request'],\n",
        "    description='Ticket type:',\n",
        "    style={'description_width': 'initial'},\n",
        "    layout=_w.Layout(width='320px'),\n",
        ")\n",
        "_text = _w.Textarea(placeholder='Describe your issue or feedback...', layout=_w.Layout(width='480px', height='100px'))\n",
        "_btn = _w.Button(description='Submit ticket', button_style='primary')\n",
        "_out = _w.Output()\n",
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
        "_btn.on_click(_on_submit)\n",
        "with _acct_out:\n",
        "    ui.tabs({'Subscription': sub_html, 'Usage': usage_html, 'Version': version_html, 'Rotate Key': rotate_html, 'Support': support_html})\n",
        "    _display(ui.card_widget([_type_dd, _text, _btn, _out], title='Submit a support ticket'))\n",
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
