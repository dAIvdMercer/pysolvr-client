# pysolvr-client

Shared notebook client library for [pysolvr](https://pysolvr.com) businesses.

Provides API wrapper, HTML display components, and Google Drive integration for Colab notebooks.

## Install

```
pip install pysolvr-client
```

## Usage

```python
from pysolvr_client import ApiClient, Display, DriveManager

client = ApiClient(base_url, api_key)
ui = Display('#6366F1', '#10B981')
drive_mgr = DriveManager('my-business', ['outputs', 'reports'])
```
