"""Universal cell: account (subscription, usage, support, version tabs)."""


def cell(config: dict) -> dict:
    """Return account management cell with tabbed output."""
    slug = config["business"]["slug"]
    domain = config.get("site", {}).get("domain", f"{slug}.pysolvr.com")
    version = config["notebook"]["version"]
    primary_color = config.get("growth", {}).get("site", {}).get("style", {}).get("primary_color", "#6366f1")
    public_repo = config["business"].get("public_repo", f"{slug}-client")
    changelog_url = f"https://github.com/dAIvdMercer/{public_repo}/blob/main/CHANGELOG.md"
    raw_changelog_url = f"https://raw.githubusercontent.com/dAIvdMercer/{public_repo}/main/CHANGELOG.md"

    tab_css = (
        ".jupyter-widgets.widget-tab > .p-TabBar .p-TabBar-tab,"
        ".jupyter-widgets.widget-tab > .lm-TabBar .lm-TabBar-tab,"
        ".jupyter-widgets.widget-tab > .p-TabBar .p-TabBar-tab.p-mod-current,"
        ".jupyter-widgets.widget-tab > .lm-TabBar .lm-TabBar-tab.lm-mod-current,"
        ".jupyter-widgets.widget-tab > .p-TabBar .p-TabBar-tab:hover,"
        ".jupyter-widgets.widget-tab > .lm-TabBar .lm-TabBar-tab:hover {"
        "background:transparent !important;color:#94a3b8;"
        "border-width:0 0 2px 0 !important;border-style:solid !important;"
        "border-color:transparent !important;box-shadow:none !important;"
        "font-size:13px;font-family:Inter,system-ui,sans-serif;padding:8px 16px;}"
        f".jupyter-widgets.widget-tab > .p-TabBar .p-TabBar-tab.p-mod-current,"
        f".jupyter-widgets.widget-tab > .lm-TabBar .lm-TabBar-tab.lm-mod-current {{color:#f1f5f9 !important;border-bottom-color:{primary_color} !important;}}"
        ".jupyter-widgets.widget-tab > .p-TabBar,"
        ".jupyter-widgets.widget-tab > .lm-TabBar {border-bottom:1px solid #475569 !important;border-top:none !important;}"
        ".jupyter-widgets.widget-tab > .widget-tab-contents,"
        ".jupyter-widgets.widget-tab > .p-Widget.widget-tab-contents {border:none !important;padding:12px 0 0;background:transparent;}"
    )

    source = f'''# @title Account
import requests as _req
import ipywidgets as _w
from IPython.display import display as _display, clear_output

result_acct = client.call('GET', '/account')
result_usage = client.get_usage()

sub_html = ''
if result_acct['ok']:
    d = result_acct['data']
    plan_label = d.get('plan', 'free').capitalize()
    sub_status = d.get('subscription_status', 'active')
    limits = d.get('tier_limits', {{}})
    def _fmt(v):
        if v == 0: return 'Unlimited'
        if v == 'none': return 'Not included'
        return str(v)
    limits_rows = ''.join(f"<tr><td style='padding:3px 8px 3px 0;color:#94a3b8;text-transform:capitalize'>{{k.replace('_', ' ')}}</td><td style='padding:3px 0;color:#e2e8f0'>{{_fmt(v)}}</td></tr>" for k, v in limits.items())
    limits_html = f"<table style='border-collapse:collapse;margin-top:6px'>{{limits_rows}}</table>" if limits_rows else ''
    topup = f"Top-up balance: ${{d.get('topup_balance_usd', 0):.2f}}<br>" if d.get('topup_balance_usd') else ''
    _status_badges = {{
        'active': "<span style='color:#10b981'>Active</span>",
        'trialing': "<span style='color:#60a5fa'>Free trial</span>",
        'past_due': "<span style='color:#f87171'>&#9888; Payment failed &mdash; update your payment method</span>",
        'paused': "<span style='color:#f59e0b'>Subscription paused</span>",
        'cancelled': "<span style='color:#94a3b8'>Subscription cancelled</span>",
    }}
    status_badge = _status_badges.get(sub_status, sub_status)
    sub_html = f"<b>{{plan_label}}</b><br>Status: {{status_badge}}<br>Monthly limit: ${{d.get('monthly_limit_usd', 0):.2f}}<br>{{topup}}<br><b>Plan limits</b>{{limits_html}}"
else:
    sub_html = f"<span style='color:#f87171'>{{result_acct.get('error', 'Could not fetch account')}}</span>"

_sub_widgets = [_w.HTML(sub_html)]
if result_acct['ok']:
    d = result_acct['data']
    sub_status = d.get('subscription_status', 'active')
    if sub_status != 'cancelled':
        _portal_btn = _w.Button(description='Manage subscription', button_style='', layout=_w.Layout(margin='8px 8px 0 0'))
        _portal_out = _w.Output()
        def _open_portal(b):
            with _portal_out:
                clear_output(wait=True)
                r = client.call('POST', '/portal')
                if r['ok']:
                    from IPython.display import Javascript
                    _display(Javascript(f"window.open('{{r['data']['url']}}', '_blank')"))
                else:
                    ui.error(r.get('error', 'Could not open portal'))
        _portal_btn.on_click(_open_portal)
        _sub_widgets += [_portal_btn, _portal_out]
    if sub_status in ('active', 'trialing') and d.get('topup_enabled'):
        _topup_amt = d.get('topup_amount_usd', 20)
        _topup_btn = _w.Button(description=f'Add ${{int(_topup_amt)}} credits', button_style='', layout=_w.Layout(margin='8px 0 0'))
        _topup_out = _w.Output()
        def _open_topup(b):
            with _topup_out:
                clear_output(wait=True)
                r = client.call('POST', '/topup')
                if r['ok']:
                    from IPython.display import Javascript
                    _display(Javascript(f"window.open('{{r['data']['url']}}', '_blank')"))
                else:
                    ui.error(r.get('error', 'Could not open top-up checkout'))
        _topup_btn.on_click(_open_topup)
        _sub_widgets += [_topup_btn, _topup_out]

usage_html = ''
if result_usage['ok']:
    data = result_usage['data']
    limit = result_acct['data'].get('monthly_limit_usd', 1) if result_acct['ok'] else 1
    usage_html = ui.usage_bar_html(data.get('current_month_spend_usd', 0), limit)
else:
    usage_html = f"<span style='color:#f87171'>{{result_usage.get('error', 'Could not fetch usage')}}</span>"

_current_ver = '{version}'
_latest_ver = _current_ver
try:
    _cl = _req.get('{raw_changelog_url}', timeout=5).text
    import re as _re
    _m = _re.search(r'## (\\d+\\.\\d+\\.\\d+)', _cl)
    if _m: _latest_ver = _m.group(1)
except: pass

_cur_parts = tuple(int(x) for x in _current_ver.split('.'))
_lat_parts = tuple(int(x) for x in _latest_ver.split('.'))
if _lat_parts <= _cur_parts:
    _ver_status = '<span style="color:#10b981">Up to date</span>'
else:
    _ver_status = f'<span style="color:#f59e0b">Update available: v{{_latest_ver}}</span><br><small>Save a fresh copy from the link below</small>'
version_html = (f'<p><b>Current:</b> v{{_current_ver}}</p>'
    f'<p><b>Latest:</b> v{{_latest_ver}} -- {{_ver_status}}</p>'
    f'<p><a href="{changelog_url}" style="color:#60a5fa">View changelog</a></p>')

rotate_html = ('<p>Generates a new API key and emails it to the address you subscribed with.</p>'
    '<p style="color:#f59e0b">Make sure you have access to that inbox before rotating -- your current key stops working immediately.</p>'
    '<button onclick="(function(){{var r=confirm(\\"Rotate your API key? Your current key will stop working immediately.\\");if(r){{IPython.notebook.kernel.execute(\\"_rotate=client.call(\\\\\\"POST\\\\\\",\\\\\\"/account/rotate-key\\\\\\");print(_rotate.get(\\\\\\"data\\\\\\",{{}}).get(\\\\\\"message\\\\\\",_rotate.get(\\\\\\"error\\\\\\",\\\\\\"Unknown error\\\\\\")))\\")}}}})()" style="background:#dc2626;color:white;border:none;padding:8px 16px;border-radius:4px;cursor:pointer;margin-top:8px">Rotate API key</button>')

_tab_style = _w.HTML('<style>{tab_css}</style>')

_type_dd = _w.Dropdown(
    options=[('Question', 'question'), ('Bug', 'bug'), ('Feature request', 'feature_request'), ('Feedback', 'feedback'), ('Billing', 'billing'), ('Data request', 'data_request')],
    description='Ticket type:',
    style={{'description_width': 'initial'}},
    layout=_w.Layout(width='320px'),
)
_text = _w.Textarea(placeholder='Describe your issue or feedback...', layout=_w.Layout(width='480px', height='100px'))
_btn = _w.Button(description='Submit ticket', button_style='primary')
_out = _w.Output()

def _on_submit(b):
    with _out:
        clear_output(wait=True)
        if not _text.value.strip():
            ui.warning('Please describe your issue before submitting.')
            return
        result = client.call('POST', '/support', payload={{
            'type': _type_dd.value,
            'feature_tag': '{slug}',
            'free_text': _text.value.strip(),
        }})
        if result['ok']:
            ui.success('Ticket submitted', f"We're on it — you'll hear back via email if needed. Reference: {{result['data']['ticket_id']}}")
            _text.value = ''
        else:
            ui.error(result.get('error', 'Submission failed. Please try again.'))

_btn.on_click(_on_submit)

_support_static = _w.HTML('<p><b>Files:</b> Google Drive > pysolvr > {slug}</p><p><b>Docs:</b> <a href="https://{domain}/docs" style="color:#60a5fa">{domain}/docs</a></p>')

_tabs = _w.Tab(children=[
    _w.VBox(_sub_widgets),
    _w.VBox([_w.HTML(usage_html)]),
    _w.VBox([_w.HTML(version_html)]),
    _w.VBox([_w.HTML(rotate_html)]),
    _w.VBox([_support_static, _w.HTML('<hr style="border-color:#475569;margin:12px 0">'), _type_dd, _text, _w.HBox([_btn], layout=_w.Layout(margin='6px 0 0')), _out]),
])
for _i, _t in enumerate(['Subscription', 'Usage', 'Version', 'Rotate Key', 'Support']):
    _tabs.set_title(_i, _t)

_display(ui.card_widget([_tab_style, _tabs]))
'''

    return {
        "cell_type": "code",
        "metadata": {
            "cellView": "form",
            "pysolvr": {"cell_type": "universal", "cell_id": "account"},
        },
        "source": [source],
        "execution_count": None,
        "outputs": [],
    }
