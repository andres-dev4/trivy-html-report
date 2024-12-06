import json
import pytest
import os
import sys


# Agregar 'src' al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from trivy_html_report_andresdev4.report_generator import generate_html_report


@pytest.fixture
def report_json_path(tmp_path):
    """Generate a sample JSON report dynamically for testing."""
    sample_data = {
        "CreatedAt": "2024-12-05T12:00:00Z",
        "Results": [
            {
                "Target": "Test Target",
                "Type": "Test Type",
                "Vulnerabilities": [
                    {
                        "VulnerabilityID": "VULN-001",
                        "Severity": "High",
                        "Title": "Test Vulnerability",
                        "Description": "This is a test vulnerability.",
                        "FixedVersion": "1.2.3"
                    }
                ]
            }
        ]
    }
    json_path = tmp_path / "report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(sample_data, f, indent=4)
    return str(json_path)

@pytest.fixture
def output_html_path(tmp_path):
    """Provide a temporary output path for the HTML report."""
    return str(tmp_path / "test_report.html")

def test_generate_html_report(report_json_path, output_html_path):
    """Test that generate_html_report creates an HTML report successfully."""
    # Test parameters
    params = {
        "input_json_path": report_json_path,
        "output_html_path": output_html_path,
        "project_name": "Sample Project",
        "scan_author": "Test Author",
        "project_url": "https://example.com",
        "report_title": "Sample Security Report"
    }

    # Generate the HTML report directly using the function
    generate_html_report(**params)

    # Assert the HTML file is created
    assert os.path.exists(output_html_path), "HTML report was not created."