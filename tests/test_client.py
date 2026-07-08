"""Tests for pysolvr_client package."""
import json
from unittest.mock import patch, MagicMock

import pytest

from pysolvr_client import ApiClient, Display, DriveManager


class TestApiClient:

    def test_init_strips_trailing_slash(self):
        c = ApiClient("https://example.com/api/", "key123")
        assert c.base_url == "https://example.com/api"

    def test_headers_set_correctly(self):
        c = ApiClient("https://x.com", "mykey")
        assert c.headers["X-Api-Key"] == "mykey"
        assert c.headers["Content-Type"] == "application/json"

    @patch("pysolvr_client.api.requests.request")
    def test_call_returns_ok_on_200(self, mock_req):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"status": "ok"}
        mock_req.return_value = mock_resp

        c = ApiClient("https://x.com", "k")
        result = c.call("GET", "/health")
        assert result["ok"] is True
        assert result["data"] == {"status": "ok"}

    @patch("pysolvr_client.api.requests.request")
    def test_call_returns_ok_on_202(self, mock_req):
        mock_resp = MagicMock()
        mock_resp.status_code = 202
        mock_resp.json.return_value = {"job_id": "abc", "status": "pending"}
        mock_req.return_value = mock_resp

        c = ApiClient("https://x.com", "k")
        result = c.call("POST", "/compare")
        assert result["ok"] is True
        assert result["data"]["job_id"] == "abc"

    @patch("pysolvr_client.api.requests.request")
    def test_call_returns_error_on_403(self, mock_req):
        mock_resp = MagicMock()
        mock_resp.status_code = 403
        mock_resp.headers = {"content-type": "application/json"}
        mock_resp.json.return_value = {"error": "forbidden"}
        mock_req.return_value = mock_resp

        c = ApiClient("https://x.com", "k")
        result = c.call("POST", "/compare")
        assert result["ok"] is False
        assert result["error"] == "forbidden"
        assert result["status"] == 403

    @patch("pysolvr_client.api.requests.request")
    def test_run_async_returns_sync_response_if_no_job_id(self, mock_req):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"demo": True, "results": []}
        mock_req.return_value = mock_resp

        c = ApiClient("https://x.com", "k")
        result = c.run_async("/compare", {"prompt": "hi"})
        assert result["ok"] is True
        assert result["data"]["demo"] is True

    @patch("pysolvr_client.api.requests.request")
    def test_run_async_returns_preflight_error_immediately(self, mock_req):
        mock_resp = MagicMock()
        mock_resp.status_code = 429
        mock_resp.headers = {"content-type": "application/json"}
        mock_resp.json.return_value = {"error": "rate limited"}
        mock_req.return_value = mock_resp

        c = ApiClient("https://x.com", "k")
        result = c.run_async("/compare", {"prompt": "hi"})
        assert result["ok"] is False
        assert result["status"] == 429


class TestDisplay:

    def test_init_stores_colors(self):
        d = Display("#111", "#222")
        assert d.primary == "#111"
        assert d.accent == "#222"


class TestDriveManager:

    def test_init_sets_root(self):
        dm = DriveManager("testbiz", ["out", "reports"])
        assert "testbiz" in str(dm.root)
        assert dm.folders == ["out", "reports"]

    @patch("pysolvr_client.drive.Path.mkdir")
    def test_ensure_folders_creates_dirs(self, mock_mkdir):
        dm = DriveManager("testbiz", ["a", "b"])
        dm.ensure_folders()
        assert mock_mkdir.call_count == 3  # root + 2 folders
