import json
import pytest
import os
from trivy_html_report.report_generator import generate_html_report

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
    with open(json_path, "w") as f:
        json.dump(sample_data, f)
    return str(json_path)

@pytest.fixture
def output_html_path(tmp_path):
    """Provide a temporary output path for the HTML report."""
    return str(tmp_path / "test_report.html")

def test_generate_html_report(report_json_path, output_html_path):
    """Test that generate_html_report creates an HTML report successfully."""
    project_name = "Sample Project"
    scan_author = "Test Author"
    project_url = "https://example.com"
    report_title = "Sample Security Report"

    # Generate the HTML report
    generate_html_report(
        input_json_path=report_json_path,
        output_html_path=output_html_path,
        project_name=project_name,
        scan_author=scan_author,
        project_url=project_url,
        report_title=report_title
    )

    # Assert the HTML file is created
    assert os.path.exists(output_html_path), "HTML report was not created."

    # Assert the HTML file contains key information
    with open(output_html_path, "r") as f:
        html_content = f.read()
        assert project_name in html_content, "Project name is missing in the HTML."
        assert scan_author in html_content, "Scan author is missing in the HTML."
        assert project_url in html_content, "Project URL is missing in the HTML."
        assert report_title in html_content, "Report title is missing in the HTML."
