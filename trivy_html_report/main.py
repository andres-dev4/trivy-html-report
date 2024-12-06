"""Main Function"""
import argparse
from trivy_html_report.report_generator import generate_html_report

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate an HTML report from a Trivy JSON report.")
    parser.add_argument("--project-name", required=True, help="Name of the project.")
    parser.add_argument("--scan-author", required=True, help="Name of the scan author.")
    parser.add_argument("--project-url", required=True, help="URL of the project.")
    parser.add_argument("--input-json", required=True, help="Path to the Trivy JSON report.")
    parser.add_argument("--output-html", default="report.html", help="Path to save the HTML report.")
    parser.add_argument("--report-title", default="Trivy Security Report", help="Title of the report.")
    args = parser.parse_args()

    generate_html_report(
        input_json_path=args.input_json,
        output_html_path=args.output_html,
        project_name=args.project_name,
        scan_author=args.scan_author,
        project_url=args.project_url,
        report_title=args.report_title
    )

if __name__ == "__main__":
    main()
