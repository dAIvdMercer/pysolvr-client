"""Tests for cell_template module."""
from pysolvr_client.cell_template import cell_template


def test_basic_cell():
    """Minimal cell with just title and logic."""
    def execute():
        result = client.call("GET", "/health")
        ui.success("Connected")

    cell = cell_template(title="Health check", execute=execute)

    assert cell["cell_type"] == "code"
    assert cell["metadata"]["cellView"] == "form"
    assert cell["metadata"]["pysolvr"]["cell_id"] == "health_check"
    source = "".join(cell["source"])
    assert "# @title Health check" in source
    assert "client.call" in source
    assert "ui.success" in source


def test_instructions_string():
    """Single string instruction renders as markdown."""
    cell = cell_template(
        title="Test",
        instructions="Enter your prompt below.",
    )
    source = "".join(cell["source"])
    assert "# @markdown Enter your prompt below." in source


def test_instructions_list():
    """List of instructions renders as bullet points."""
    cell = cell_template(
        title="Test",
        instructions=["Step one", "Step two"],
    )
    source = "".join(cell["source"])
    assert "# @markdown - Step one" in source
    assert "# @markdown - Step two" in source


def test_form_fields():
    """Form fields appear before logic."""
    def execute():
        print(PROMPT)

    cell = cell_template(
        title="Test",
        form_fields=[
            "PROMPT = ''  # @param {type: 'string'}",
            "MODEL = 'grok'  # @param [\"grok\", \"anthropic\"]",
        ],
        execute=execute,
    )
    source = "".join(cell["source"])
    # Form fields before logic
    prompt_idx = source.index("PROMPT = ''")
    model_idx = source.index("MODEL = 'grok'")
    print_idx = source.index("print(PROMPT)")
    assert prompt_idx < model_idx < print_idx


def test_no_def_line_in_output():
    """The def line itself should not appear in cell source."""
    def execute():
        x = 1

    cell = cell_template(title="Test", execute=execute)
    source = "".join(cell["source"])
    assert "def execute" not in source
    assert "x = 1" in source


def test_docstring_stripped():
    """Docstrings in execute function are stripped."""
    def execute():
        """This should not appear."""
        x = 1

    cell = cell_template(title="Test", execute=execute)
    source = "".join(cell["source"])
    assert "This should not appear" not in source
    assert "x = 1" in source


def test_multiline_logic():
    """Complex logic with indentation is preserved correctly."""
    def execute():
        result = client.run_async("POST", "/generate", body)
        if result["ok"]:
            ui.tabs({"Plan": result["data"]["content"]})
        else:
            ui.error(result["error"], actions=result.get("actions"))

    cell = cell_template(title="Generate", execute=execute)
    source = "".join(cell["source"])
    assert "if result[\"ok\"]:" in source
    assert "    ui.tabs" in source
    assert "    ui.error" in source
