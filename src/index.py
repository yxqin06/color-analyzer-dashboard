@app.route("/", methods=["GET"])
def index_page():
    """Show list of generated dashboards."""
    files = sorted(
        [f for f in os.listdir(ASSETS_REPORTS) if f.endswith(".html")],
        reverse=True
    )

    links = [
        f'<li><a href="/dashboard/{f}">{f}</a></li>'
        for f in files
    ]

    html = f"""
    <html>
    <head>
        <title>Color Analyzer Dashboards</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
            }}
            h1 {{
                margin-bottom: 10px;
            }}
            ul {{
                line-height: 1.8;
            }}
            a {{
                color: #0077cc;
                font-size: 18px;
            }}
        </style>
    </head>
    <body>
        <h1>Generated Dashboards</h1>
        <ul>
            {''.join(links)}
        </ul>
    </body>
    </html>
    """
    return html
