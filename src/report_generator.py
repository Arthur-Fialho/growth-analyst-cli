import os
from datetime import datetime
from tabulate import tabulate

def format_currency(val):
    """Formats a float value as Brazilian currency string R$."""
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def generate_markdown_report(agg_df, partner_name, csv_path, ai_analysis):
    """
    Generates a professional Markdown report and saves it locally.
    Returns:
        report_path: str, path to the created markdown report.
    """
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
    
    metrics_table = tabulate(md_df, headers='keys', tablefmt='github', index=False)
    
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
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    return report_path

def print_terminal_summary(agg_df, partner_name, ai_analysis, report_path):
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
    print(tabulate(terminal_table_data, headers='keys', tablefmt='simple', index=False))
    
    print("\n" + "-" * 80)
    print("AI ANALYSIS SUMMARY:")
    print(f"Executive Summary:\n{ai_analysis.get('executive_summary', 'N/A')}")
    print("-" * 80)
    
    # Visual winner highlight
    winner = ai_analysis.get('winning_variant_name', 'N/A')
    print(f"🏆 DECISÃO DE ESCALA (WINNING VARIANT): {winner}")
    print(f"Decisão Acionável:\n{ai_analysis.get('actionable_decision', 'N/A')}")
    print("-" * 80)
    print(f"📄 Full Markdown report saved to: {report_path}")
    print("=" * 80 + "\n")
