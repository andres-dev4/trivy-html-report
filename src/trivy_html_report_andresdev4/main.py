import click
from trivy_html_report_andresdev4.report_generator import generate_html_report

@click.command()
@click.option("--project-name", required=True, help="Name of the project.")
@click.option("--scan-author", required=True, help="Author of the scan.")
@click.option("--project-url", required=True, help="URL of the project.")
@click.option("--input-json", required=True, type=click.Path(exists=True), help="Path to the Trivy JSON report.")
@click.option("--output-html", required=True, type=click.Path(), help="Path to save the output HTML.")
@click.option("--report-title", required=True, help="Title for the HTML report.")
def main(project_name, scan_author, project_url, input_json, output_html, report_title):
    """CLI entry point."""
    generate_html_report(
        input_json_path=input_json,
        output_html_path=output_html,
        project_name=project_name,
        scan_author=scan_author,
        project_url=project_url,
        report_title=report_title
    )

if __name__ == "__main__":
    main()
