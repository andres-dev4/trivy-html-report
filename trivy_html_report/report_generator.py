import json
from jinja2 import Environment, FileSystemLoader
from dateutil.parser import parse
import matplotlib.pyplot as plt
import io
import base64
import re
from collections import Counter

def clean_ansi_sequences(text):
    """Clean ANSI escape sequences from text."""
    text = str(text) if text is not None else ""  # Convert to string even if None
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def generate_html_report(input_json_path, output_html_path, project_name, scan_author, project_url, report_title):
    """Generate an HTML report from a Trivy JSON report."""
    with open(input_json_path, 'r') as f:
        report_data = json.load(f)

    severities = []
    results = report_data.get('Results', [])
    for result in results:
        if 'Vulnerabilities' in result:
            for vuln in result['Vulnerabilities']:
                severities.append(vuln.get('Severity', 'Unknown'))
        if 'Secrets' in result:
            for secret in result['Secrets']:
                severities.append(secret.get('Severity', 'Unknown'))
        if result.get('Class') == 'config':
            severities.append(result.get('Class', 'Config Issue'))

    severity_counts = Counter(severities)

    # Generate severity bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(severity_counts.keys(), severity_counts.values(), color=['#ff6b6b', '#feca57', '#48dbfb', '#1dd1a1'])
    plt.xlabel('Severity')
    plt.ylabel('Count')
    plt.title('Severity Summary')

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    created_at = parse(report_data.get('CreatedAt', ''))
    formatted_date = created_at.strftime("%d-%m-%Y %H:%M:%S")

    # Configure Jinja2 environment
    env = Environment(loader=FileSystemLoader('.'))
    template = env.from_string("""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Seguridad - Trivy</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
    background-color: #f0f2f5; /* Color más claro y suave */
    font-family: 'Arial', sans-serif;
    color: #333333; /* Tonalidad ligeramente más oscura para mejor legibilidad */
    line-height: 1.6; /* Espaciado para mejorar la lectura */
        }

        .container {
    margin: 30px auto; /* Centrado y mayor separación en la parte superior */
    max-width: 85%; /* Ligeramente más pequeño para mejor enmarcado */
    padding: 0 15px; /* Espaciado interno para evitar que el contenido toque los bordes */
    }

    h2, h3, h4 {
    color: #0056b3; /* Un azul ligeramente más oscuro y profesional */
    font-weight: 600; /* Resalta más los títulos */
    margin-bottom: 15px; /* Mayor espacio debajo */
    }

    .info-box, .card {
    background-color: #ffffff;
    padding: 20px; /* Mayor espaciado para mejor estructura */
    border-radius: 12px; /* Bordes más redondeados */
    margin-bottom: 25px; /* Mayor separación entre elementos */
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06); /* Sombra más suave y difusa */
    transition: box-shadow 0.3s ease; /* Efecto de hover */
    }

    .info-box:hover, .card:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12); /* Sombra más intensa al pasar el cursor */
    }

    .table-wrapper {
    overflow-x: auto;
    max-width: 100%;
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08); /* Sombra más sutil */
    padding: 10px; /* Relleno para que la tabla no toque los bordes del contenedor */
    }

    table {
    width: 100%;
    border-collapse: collapse;
    margin: 0 auto;
    }

    th, td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #dee2e6;
    }

    th {
    background-color: #f8f9fa;
    color: #495057;
    font-weight: bold;
    }

        td {
            padding: 11px;
            color: #495057;
            word-wrap: break-word;
        }
        .severity-critical {
            color: #e74c3c;
            font-weight: bold;
        }
        .severity-high {
            color: #ff6b6b;
            font-weight: bold;
        }
        .severity-medium {
            color: #feca57;
            font-weight: bold;
        }
        .severity-low {
            color: #1dd1a1;
            font-weight: bold;
        }
        .highlighted-title {
            font-size: 1.25em;
            font-weight: bold;
            color: #007bff;
            margin-top: 20px;
        }
        .list-group-item {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            color: #343a40;
        }
        .list-group-item strong {
            color: #007bff;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            font-size: 0.9em;
            color: #495057;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="info-box">
            <h2 style="color: #0056b3; font-weight: bold; margin-bottom: 15px;">{{ report_title }}</h2>
    <ul style="list-style-type: none; padding: 0; margin: 0;">
        <li style="margin-bottom: 10px;">
            <strong>Project:</strong> {{ project_name }}
        </li>
        <li style="margin-bottom: 10px;">
            <strong>Project URL:</strong> 
            <a href="{{ project_url }}" target="_blank" style="color: #007bff; text-decoration: none;">
                {{ project_url }}
            </a>
        </li>
        <li style="margin-bottom: 10px;">
            <strong>Generated by:</strong> {{ scan_author }}
        </li>
        <li style="margin-bottom: 10px;">
            <strong>Date:</strong> {{ formatted_date }}
        </li>
    </ul>
        </div>

        <!-- Tabla de resumen de severidades -->
        <div class="info-box">
            <h4>Error Summary</h4>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Severity</th>
                        <th>Quantity</th>
                    </tr>
                </thead>
                <tbody>
                    {% for severity, count in severity_counts.items() %}
                        <tr>
                            <td class="severity-{{ severity|lower }}">{{ severity }}</td>
                            <td>{{ count }}</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <!-- Severity Chart -->
        <div class="info-box">
            <h4>Severity Chart</h4>
            <img src="data:image/png;base64,{{ img_base64 }}" alt="Severity Chart" class="img-fluid rounded">
        </div>

        {% if report_data.Results %}
            {% for result in report_data.Results %}
                <div class="card mb-4">
                    <div class="card-header">
                        <h3 class="highlighted-title">{{ result.Target }} ({{ result.Class }})</h3>
                        <p><strong>Tipo:</strong> {{ result.Type }}</p>
                    </div>
                    <div class="card-body">
                        {% if result.Target == "src/Pipfile.lock" and result.Vulnerabilities %}
                            <h4>Vulnerabilities in Pipfile.lock</h4>
                            <div class="table-wrapper">
                                <table class="table table-striped table-bordered">
                                    <thead>
                                        <tr>
                                            <th>ID</th><th>Severity</th><th>Title</th><th>Description</th><th>Fixed Version</th><th>Raw JSON</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for vuln in result.Vulnerabilities %}
                                            <tr>
                                                <td>{{ vuln.VulnerabilityID }}</td>
                                                <td class="severity-{{ vuln.Severity|lower }}">{{ vuln.Severity }}</td>
                                                <td>{{ vuln.Title }}</td>
                                                <td>{{ vuln.Description }}</td>
                                                <td>{{ vuln.FixedVersion }}</td>
                                                <td><pre>{{ vuln | tojson(indent=2) }}</pre></td>
                                            </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        {% endif %}

                        {% if result.Secrets %}
                            <h4>Secrets</h4>
                            <div class="table-wrapper">
                                <table class="table table-striped table-bordered">
                                    <thead>
                                        <tr>
                                            <th>Rule ID</th><th>Categoría</th><th>Severity</th><th>Título</th><th>Inicio</th><th>Fin</th><th>Match</th><th>Código</th><th>CauseMetadata</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for secret in result.Secrets %}
                                            <tr>
                                                <td>{{ secret.RuleID }}</td>
                                                <td>{{ secret.Category }}</td>
                                                <td class="severity-{{ secret.Severity|lower }}">{{ secret.Severity }}</td>
                                                <td>{{ secret.Title }}</td>
                                                <td>{{ secret.StartLine }}</td>
                                                <td>{{ secret.EndLine }}</td>
                                                <td>{{ secret.Match }}</td>
                                                <td>
                                                    <ul>
                                                        {% for line in secret.Code.Lines %}
                                                            <li><strong>Línea {{ line.Number }}:</strong>
                                                                <pre>{{ clean_ansi_sequences(line.Highlighted) }}</pre>
                                                    
                                                                
                                                            </li>
                                                        {% endfor %}
                                                    </ul>
                                                </td>
                                                <td>
                                                    {% if secret.CauseMetadata %}
                                                        <pre>{{ secret.CauseMetadata | tojson(indent=2) }}</pre>
                                                    {% else %}
                                                        {% for line in secret.Code.Lines %}
                                                            <li <strong>Línea {{ line.Number }}:</strong>
                                                                <pre>{{ line }}</pre>
                                                    
                                                                
                                                            </li>
                                                        {% endfor %}
                                                    {% endif %}
                                                </td>
                                            </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        {% endif %}
                        {% if result.Misconfigurations %}
                            <h4>Misconfiguraciones</h4>
                            <div class="table-wrapper">
                                <table class="table table-striped table-bordered">
                                    <thead>
                                        <tr>
                                            <th>ID</th><th>Título</th><th>Descripción</th><th>Severity</th><th>Resolución</th>
                                            <th>Detalle</th><th>CauseMetadata</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for misconf in result.Misconfigurations %}
                                            <tr>
                                                <td>{{ misconf.ID }}</td>
                                                <td>{{ misconf.Title }}</td>
                                                <td>{{ misconf.Description }}</td>
                                                <td class="severity-{{ misconf.Severity|lower }}">{{ misconf.Severity }}</td>
                                                <td>{{ misconf.Resolution }}</td>
                                                <td>
                                                    <ul>
                                                        <li><strong>Message:</strong> {{ misconf.Message }}</li>
                                                        <li><strong>Provider:</strong> {{ misconf.CauseMetadata.Provider if misconf.CauseMetadata and misconf.CauseMetadata.Provider }}</li>
                                                        <li><strong>Service:</strong> {{ misconf.CauseMetadata.Service if misconf.CauseMetadata and misconf.CauseMetadata.Service }}</li>
                                                        <li><strong>Code Lines:</strong>
                                                            {% if misconf.CauseMetadata and misconf.CauseMetadata.Code and misconf.CauseMetadata.Code.Lines %}
                                                                <pre>{% for line in misconf.CauseMetadata.Code.Lines %}
{{ line.Number }}: {{ clean_ansi_sequences(line.Highlighted) }}{% endfor %}</pre>
                                                            {% endif %}
                                                        </li>
                                                    </ul>
                                                </td>
                                                <td>
                                                    {% if misconf.CauseMetadata %}
                                                        <pre>{{ misconf.CauseMetadata | tojson(indent=2) }}</pre>
                                                    {% else %}
                                                        <span>No disponible</span>
                                                    {% endif %}
                                                </td>
                                            </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        {% endif %}
                    </div>
                </div>
            {% endfor %}
        {% else %}
            <p>No results found.</p>
        {% endif %}
    </div>
</body>
</html>
    """, {'clean_ansi_sequences': clean_ansi_sequences})

    # Render the HTML
    html_content = template.render(
        report_data=report_data,
        project_name=project_name,
        project_url=project_url,
        scan_author=scan_author,
        formatted_date=formatted_date,
        severity_counts=severity_counts,
        img_base64=img_base64,
        report_title=report_title,
        results=results
    )

    # Write HTML to file
    with open(output_html_path, 'w') as f:
        f.write(html_content)

    print(f"HTML report generated: {output_html_path}")
