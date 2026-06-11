import os
from datetime import datetime
from tabulate import tabulate

def format_currency(val):
    """Formats a float value as Brazilian currency string R$."""
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def generate_markdown_report(agg_df, partner_name, csv_path, ai_analysis):
    """
    Generates a professional Markdown report and saves it locally.
    Also creates a beautifully styled HTML version for managers.
    Returns:
        tuple: (report_path, html_report_path)
    """
    import markdown
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"report_{partner_name.replace(' ', '_')}_{timestamp}.md"
    report_path = os.path.join(reports_dir, report_filename)
    
    # Format aggregate metrics into a copy for Markdown rendering
    md_df = agg_df.copy()
    md_df['Total Comissão'] = md_df['Total Comissão'].apply(format_currency)
    md_df['Total Cashback'] = md_df['Total Cashback'].apply(format_currency)
    md_df['Total Vendas'] = md_df['Total Vendas'].apply(format_currency)
    md_df['ROI'] = md_df['ROI'].apply(format_currency)
    md_df['ROI %'] = md_df['ROI %'].apply(lambda x: f"{x:.2f}%")
    md_df['Ticket Médio'] = md_df['Ticket Médio'].apply(format_currency)
    md_df['Taxa de Comissão %'] = md_df['Taxa de Comissão %'].apply(lambda x: f"{x:.2f}%")
    md_df['Taxa de Cashback %'] = md_df['Taxa de Cashback %'].apply(lambda x: f"{x:.2f}%")
    
    metrics_table = tabulate(md_df, headers='keys', tablefmt='github', showindex=False)
    
    csv_filename = os.path.basename(csv_path)
    current_time_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    report_content = f"""# Relatório de Teste A/B: {partner_name}
 
## 1. Metadados do Teste
- **Data da Análise**: {current_time_str}
- **Arquivo de Origem**: `{csv_filename}`
- **Parceiro**: {partner_name}
 
## 2. Métricas Financeiras e de Conversão Agregadas
{metrics_table}
 
---
 
## 3. Análise do Growth Analyst (AI Gemini)
 
### Resumo Executivo
{ai_analysis.get('executive_summary', 'N/A')}
 
### Análise Detalhada
{ai_analysis.get('detailed_analysis', 'N/A')}
 
---
 
## 4. Decisão de Escala e Próximos Passos
- **Variante Vencedora (a ser escalada para 100%)**: **{ai_analysis.get('winning_variant_name', 'N/A')}**
 
### Ação Recomendada
> {ai_analysis.get('actionable_decision', 'N/A')}
 
---
*Relatório gerado de forma autônoma pelo Growth Analyst AI CLI.*
"""
    
    # Write local Markdown report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    # Convert Markdown to HTML and wrap tables in a responsive container
    html_body = markdown.markdown(report_content, extensions=['extra'])
    html_body = html_body.replace("<table>", '<div class="table-container"><table>')
    html_body = html_body.replace("</table>", '</table></div>')
    
    # Wrap in modern styled corporate template
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Teste A/B - {partner_name}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #0f172a;
            --primary-light: #38bdf8;
            --background: #f8fafc;
            --card-bg: #ffffff;
            --text: #334155;
            --text-dark: #0f172a;
            --border: #e2e8f0;
            --success: #10b981;
            --accent: #f59e0b;
        }}

        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--background);
            color: var(--text);
            line-height: 1.6;
            margin: 0;
            padding: 40px 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background-color: var(--card-bg);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--border);
            position: relative;
            overflow: hidden;
        }}

        .container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 6px;
            background: linear-gradient(90deg, var(--primary-light), #818cf8);
        }}

        h1 {{
            color: var(--text-dark);
            font-size: 2.5rem;
            margin-top: 0;
            margin-bottom: 20px;
            font-weight: 700;
            border-bottom: 2px solid var(--border);
            padding-bottom: 15px;
        }}

        h2 {{
            color: var(--text-dark);
            font-size: 1.5rem;
            margin-top: 35px;
            margin-bottom: 15px;
            font-weight: 600;
            position: relative;
            padding-left: 12px;
        }}

        h2::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 4px;
            bottom: 4px;
            width: 4px;
            background-color: var(--primary-light);
            border-radius: 2px;
        }}

        h3 {{
            color: var(--text-dark);
            font-size: 1.2rem;
            margin-top: 25px;
            margin-bottom: 10px;
            font-weight: 600;
        }}

        p {{
            margin-bottom: 20px;
        }}

        ul, ol {{
            margin-bottom: 20px;
            padding-left: 20px;
        }}

        li {{
            margin-bottom: 8px;
        }}

        code {{
            font-family: 'Courier New', Courier, monospace;
            background-color: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
            color: #e21d48;
        }}

        blockquote {{
            margin: 25px 0;
            padding: 15px 20px;
            background-color: #f0f9ff;
            border-left: 4px solid var(--primary-light);
            border-radius: 0 8px 8px 0;
            color: #0369a1;
            font-style: italic;
        }}

        blockquote p {{
            margin: 0;
        }}

        .table-container {{
            width: 100%;
            overflow-x: auto;
            margin: 25px 0;
            border-radius: 8px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
        }}

        th {{
            background-color: var(--primary);
            color: white;
            text-align: left;
            font-weight: 600;
            padding: 12px 15px;
            white-space: nowrap;
        }}

        td {{
            padding: 12px 15px;
            border-bottom: 1px solid var(--border);
            white-space: nowrap;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:nth-child(even) td {{
            background-color: #f8fafc;
        }}

        tr:hover td {{
            background-color: #f1f5f9;
            transition: background-color 0.2s ease;
        }}

        hr {{
            border: 0;
            height: 1px;
            background: var(--border);
            margin: 40px 0;
        }}

        footer {{
            margin-top: 45px;
            font-size: 0.85rem;
            color: #94a3b8;
            text-align: center;
            border-top: 1px solid var(--border);
            padding-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_body}
    </div>
</body>
</html>
"""
    
    html_filename = f"report_{partner_name.replace(' ', '_')}_{timestamp}.html"
    html_report_path = os.path.join(reports_dir, html_filename)
    
    with open(html_report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    return report_path, html_report_path

def print_terminal_summary(agg_df, partner_name, ai_analysis, report_path, html_report_path):
    """
    Outputs a premium visual summary of the test results to the terminal.
    """
    # Create console-friendly df
    con_df = agg_df.copy()
    con_df['Total Vendas'] = con_df['Total Vendas'].apply(format_currency)
    con_df['Total Cashback'] = con_df['Total Cashback'].apply(format_currency)
    con_df['ROI'] = con_df['ROI'].apply(format_currency)
    con_df['ROI %'] = con_df['ROI %'].apply(lambda x: f"{x:.2f}%")
    
    # Select subset of key columns for terminal readability
    terminal_table_data = con_df[[
        'Grupo', 'Total Compradores', 'Total Vendas', 'Total Cashback', 'ROI', 'ROI %'
    ]]
    
    print("\n" + "=" * 80)
    print(f" A/B TEST GROWTH REPORT SUMMARY: {partner_name.upper()}")
    print("=" * 80)
    
    # Print metrics table
    print("\nMetrics Summary Table:")
    print(tabulate(terminal_table_data, headers='keys', tablefmt='simple', showindex=False))
    
    print("\n" + "-" * 80)
    print("AI ANALYSIS SUMMARY:")
    print(f"Executive Summary:\n{ai_analysis.get('executive_summary', 'N/A')}")
    print("-" * 80)
    
    # Visual winner highlight
    winner = ai_analysis.get('winning_variant_name', 'N/A')
    print(f"🏆 DECISÃO DE ESCALA (WINNING VARIANT): {winner}")
    print(f"Decisão Acionável:\n{ai_analysis.get('actionable_decision', 'N/A')}")
    print("-" * 80)
    
    abs_html_path = os.path.abspath(html_report_path)
    file_uri = f"file://{abs_html_path}"
    print(f"📄 Full Markdown report saved to: {report_path}")
    print(f"🖥️  Beautiful HTML report for managers: {file_uri}")
    print("=" * 80 + "\n")


