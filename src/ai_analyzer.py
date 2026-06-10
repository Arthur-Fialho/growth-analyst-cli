import os
import json
import google.generativeai as genai

def analyze_growth_data(agg_df, partner_name):
    """
    Sends aggregate A/B test data to Gemini API and retrieves a structured growth analysis.
    Returns:
        dict: A dictionary containing:
            - executive_summary
            - detailed_analysis
            - winning_variant_name
            - actionable_decision
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    
    # Configure Gemini SDK
    genai.configure(api_key=api_key)
    
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # Format aggregate metrics as a readable JSON string for the prompt
    metrics_records = agg_df.to_dict(orient='records')
    # Convert numeric fields to clean string representations for easier LLM reading
    for record in metrics_records:
        for k, v in record.items():
            if isinstance(v, float):
                record[k] = round(v, 2)
                
    metrics_json_str = json.dumps(metrics_records, indent=2, ensure_ascii=False)
    
    prompt = f"""
Você é um Growth Analyst Sênior especialista em campanhas de cashback e canais de parceiros.
Sua tarefa é analisar os resultados agregados de um teste A/B do parceiro "{partner_name}".

Os dados agregados por grupo (variante) estão em formato JSON abaixo:
{metrics_json_str}

Métricas explicadas:
- Total Compradores: número acumulado de compradores únicos que realizaram compra.
- Total Comissão: comissão bruta total gerada pelo parceiro para nós (R$).
- Total Cashback: cashback total distribuído aos usuários (R$).
- Total Vendas: Volume de Vendas bruto total (GMV) gerado pelo parceiro (R$).
- ROI: Retorno do Investimento financeiro da campanha de cashback (Comissão - Cashback) em R$.
- ROI %: Retorno percentual sobre o cashback investido ((ROI / Cashback) * 100).
- Ticket Médio: Valor de vendas médio por comprador (Vendas / Compradores) em R$.
- Taxa de Comissão %: Porcentagem de comissão sobre as vendas (Comissão / Vendas * 100).
- Taxa de Cashback %: Porcentagem de cashback dado sobre as vendas (Cashback / Vendas * 100).

Instruções de análise:
1. **Sustentabilidade Financeira**: O ROI (Comissão - Cashback) deve ser prioritariamente positivo. Variantes com ROI negativo geram prejuízo para a plataforma no longo prazo.
2. **Eficiência e Escala**: Avalie a eficiência de conversão e geração de vendas (GMV).
3. **Decisão Acionável**: Determine qual variante (e.g., "Grupo 1", "Grupo 2", "Grupo 3") deve ser escalada para 100% do tráfego. Se todas as variantes forem financeiramente insustentáveis, recomende desativar ou redefinir a campanha de cashback (vencedor: "Nenhum").
4. **Responda Estritamente em JSON**: O retorno deve ser formatado com as chaves exatas listadas abaixo, sem blocos markdown extras ou explicações adicionais fora do JSON.

Esquema JSON esperado:
{{
  "executive_summary": "Resumo executivo conciso do teste A/B em português.",
  "detailed_analysis": "Análise detalhada comparando os resultados financeiros e de engajamento de cada grupo em português.",
  "winning_variant_name": "O nome exato do grupo vencedor (por exemplo: 'Grupo 1', 'Grupo 2', ou 'Nenhum')",
  "actionable_decision": "Recomendação acionável detalhada sobre como proceder em português."
}}
"""
    
    # Configure generation for JSON response format
    generation_config = {
        "response_mime_type": "application/json"
    }
    
    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config
        )
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parse output
        analysis = json.loads(response_text)
        
        # Validate that all required keys are present
        required_keys = ["executive_summary", "detailed_analysis", "winning_variant_name", "actionable_decision"]
        for key in required_keys:
            if key not in analysis:
                analysis[key] = "N/A"
                
        return analysis
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini API returned an invalid JSON response. Response: {response.text}") from e
    except Exception as e:
        raise RuntimeError(f"Error calling Gemini API: {str(e)}") from e
