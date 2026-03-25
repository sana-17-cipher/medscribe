import pdfkit
import os
import tempfile
from datetime import datetime

# Tell pdfkit exactly where wkhtmltopdf is installed
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

def generate_pdf(patient_name, doc_type, report_data, transcript):
    """
    Takes structured report dict, returns PDF as bytes.
    """

    date_str = datetime.now().strftime("%d %b %Y, %I:%M %p")

    # Build the report rows
    rows = ""
    for key, val in report_data.items():
        is_empty = not val or val == "Not mentioned"
        val_style = "color:#888;font-style:italic" if is_empty else "color:#111"
        rows += f"""
        <tr>
            <td class="key">{key}</td>
            <td style="{val_style}">{"—" if is_empty else val}</td>
        </tr>"""

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: Arial, sans-serif;
            font-size: 13px;
            color: #111;
            padding: 40px;
        }}

        /* Header */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 3px solid #00d4aa;
            padding-bottom: 16px;
            margin-bottom: 24px;
        }}
        .logo {{
            font-size: 20px;
            font-weight: 700;
            color: #0a1628;
        }}
        .logo span {{ color: #00a88a; }}
        .meta {{
            text-align: right;
            font-size: 12px;
            color: #555;
            line-height: 1.7;
        }}

        /* Patient info bar */
        .info-bar {{
            background: #f0fdf9;
            border: 1px solid #b2f0e0;
            border-radius: 8px;
            padding: 14px 20px;
            margin-bottom: 24px;
            display: flex;
            gap: 40px;
        }}
        .info-item label {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: .05em;
            color: #666;
            display: block;
            margin-bottom: 3px;
        }}
        .info-item span {{
            font-size: 14px;
            font-weight: 600;
            color: #0a1628;
        }}

        /* Report table */
        .section-title {{
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: .07em;
            color: #00a88a;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 28px;
        }}
        tr {{ border-bottom: 1px solid #e8e8e8; }}
        tr:last-child {{ border-bottom: none; }}
        td {{ padding: 9px 12px; vertical-align: top; line-height: 1.5; }}
        td.key {{
            width: 170px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: .04em;
            color: #444;
            background: #f8f8f8;
        }}
        tr:nth-child(even) td.key {{ background: #f0f0f0; }}

        /* Transcript */
        .transcript-box {{
            background: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 14px 16px;
            font-size: 13px;
            color: #444;
            line-height: 1.7;
            margin-bottom: 28px;
        }}

        /* Footer */
        .footer {{
            border-top: 1px solid #e0e0e0;
            padding-top: 12px;
            font-size: 11px;
            color: #999;
            display: flex;
            justify-content: space-between;
        }}
    </style>
    </head>
    <body>

    <!-- Header -->
    <div class="header">
        <div class="logo">Med<span>Scribe</span> AI</div>
        <div class="meta">
            <strong>Clinical Documentation Report</strong><br>
            Generated: {date_str}<br>
            CONFIDENTIAL — For authorized medical personnel only
        </div>
    </div>

    <!-- Patient info bar -->
    <div class="info-bar">
        <div class="info-item">
            <label>Patient</label>
            <span>{patient_name or "Not specified"}</span>
        </div>
        <div class="info-item">
            <label>Document Type</label>
            <span>{doc_type.upper()}</span>
        </div>
        <div class="info-item">
            <label>Date</label>
            <span>{date_str}</span>
        </div>
    </div>

    <!-- Structured report -->
    <div class="section-title">Structured Report</div>
    <table>{rows}</table>

    <!-- Original transcript -->
    <div class="section-title">Original Transcript</div>
    <div class="transcript-box">{transcript}</div>

    <!-- Footer -->
    <div class="footer">
        <span>MedScribe AI — Auto-generated clinical note</span>
        <span>Verify all details before clinical use</span>
    </div>

    </body>
    </html>
    """

    # Generate PDF to a temp file, return as bytes
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp_path = tmp.name

    pdfkit.from_string(html, tmp_path, configuration=config, options={
        "page-size": "A4",
        "margin-top": "10mm",
        "margin-bottom": "10mm",
        "margin-left": "10mm",
        "margin-right": "10mm",
        "encoding": "UTF-8",
        "quiet": ""
    })

    with open(tmp_path, "rb") as f:
        pdf_bytes = f.read()

    os.unlink(tmp_path)
    return pdf_bytes