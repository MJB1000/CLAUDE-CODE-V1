import markdown
from weasyprint import HTML

with open("Marketing-Team-Framework-Review.md", "r") as f:
    md_content = f.read()

html_body = markdown.markdown(md_content, extensions=["tables", "fenced_code"])

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: A4;
    margin: 2cm 2.5cm;
    @bottom-center {{
      content: counter(page);
      font-size: 9px;
      color: #888;
    }}
  }}
  body {{
    font-family: -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 11px;
    line-height: 1.5;
    color: #1a1a1a;
  }}
  h1 {{
    font-size: 22px;
    border-bottom: 2px solid #333;
    padding-bottom: 6px;
    margin-top: 0;
  }}
  h2 {{
    font-size: 15px;
    color: #222;
    border-bottom: 1px solid #ddd;
    padding-bottom: 4px;
    margin-top: 20px;
  }}
  h3 {{
    font-size: 12px;
    color: #444;
    margin-top: 14px;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 10px 0;
    font-size: 10px;
  }}
  th {{
    background-color: #f5f5f5;
    font-weight: 600;
    text-align: left;
    padding: 6px 8px;
    border: 1px solid #ddd;
  }}
  td {{
    padding: 5px 8px;
    border: 1px solid #ddd;
    vertical-align: top;
  }}
  tr:nth-child(even) {{
    background-color: #fafafa;
  }}
  code {{
    background-color: #f4f4f4;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 10px;
  }}
  pre {{
    background-color: #f4f4f4;
    padding: 10px;
    border-radius: 4px;
    font-size: 9px;
    line-height: 1.4;
    overflow-x: auto;
  }}
  pre code {{
    background: none;
    padding: 0;
  }}
  hr {{
    border: none;
    border-top: 1px solid #ddd;
    margin: 16px 0;
  }}
  strong {{
    color: #111;
  }}
  p {{
    margin: 6px 0;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

HTML(string=html).write_pdf("Marketing-Team-Framework-Review.pdf")
print("PDF generated: Marketing-Team-Framework-Review.pdf")
