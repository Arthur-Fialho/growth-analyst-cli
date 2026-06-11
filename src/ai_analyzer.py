import os
import json

def clean_and_parse_json(text):
    """
    Cleans markdown code block wraps and parses text as JSON by extracting
    the substring between the first '{' and the last '}'.
    """
    text = text.strip()
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and start < end:
        text = text[start:end+1]
    return json.loads(text)

def analyze_growth_data(agg_df, partner_name):
    """
    Sends aggregate A/B test data to the configured AI API (OpenAI, Anthropic, or Gemini)
    and retrieves a structured growth analysis.
    
    Returns:
        dict: A dictionary containing both Portuguese and English key mappings:
            - resumo_executivo / executive_summary
            - analise_detalhada / detailed_analysis
            - nome_variante_vencedora / winning_variant_name
            - decisao_acionavel / actionable_decision
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
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
  "resumo_executivo": "Resumo executivo conciso do teste A/B em português.",
  "analise_detalhada": "Análise detalhada comparando os resultados financeiros e de engajamento de cada grupo em português.",
  "nome_variante_vencedora": "O nome exato do grupo vencedor (por exemplo: 'Grupo 1', 'Grupo 2', ou 'Nenhum')",
  "decisao_acionavel": "Recomendação acionável detalhada sobre como proceder em português."
}}
"""
    
    # 1. OpenAI routing logic
    if openai_key:
        print("🤖 Initializing OpenAI client using gpt-4o-mini...")
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um Growth Analyst Sênior especialista em campanhas de cashback e canais de parceiros. Responda estritamente em JSON usando o esquema solicitado."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            response_text = response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Error calling OpenAI API: {str(e)}") from e
            
    # 2. Anthropic routing logic
    elif anthropic_key:
        print("🤖 Initializing Anthropic client using claude-3-5-sonnet-latest...")
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=anthropic_key)
            response = client.messages.create(
                model="claude-3-5-sonnet-latest",
                max_tokens=4000,
                system="Você é um Growth Analyst Sênior especialista em campanhas de cashback e canais de parceiros. Responda estritamente em JSON usando o esquema solicitado.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            response_text = response.content[0].text
        except Exception as e:
            raise RuntimeError(f"Error calling Anthropic API: {str(e)}") from e
            
    # 3. Gemini fallback routing logic
    elif gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
            
            generation_config = {
                "response_mime_type": "application/json"
            }
            print(f"🤖 Initializing Gemini client using {model_name}...")
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config
            )
            try:
                response = model.generate_content(prompt)
                response_text = response.text.strip()
            except Exception as e:
                # If we were using gemini-2.5-flash, try falling back to gemini-2.5-flash-lite
                if model_name == "gemini-2.5-flash":
                    print(f"⚠️ Request failed with {model_name}: {e}")
                    print("🔄 Falling back to gemini-2.5-flash-lite...")
                    fallback_model = genai.GenerativeModel(
                        model_name="gemini-2.5-flash-lite",
                        generation_config=generation_config
                    )
                    response = fallback_model.generate_content(prompt)
                    response_text = response.text.strip()
                else:
                    raise e
        except Exception as e:
            raise RuntimeError(f"Error calling Gemini API: {str(e)}") from e
            
    else:
        raise ValueError("No API key found. Please set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY.")
        
    try:
        # Parse output
        analysis_raw = clean_and_parse_json(response_text)
        
        # Enforce exact JSON schema (both Portuguese and English keys)
        analysis = {
            "resumo_executivo": analysis_raw.get("resumo_executivo", "N/A"),
            "analise_detalhada": analysis_raw.get("analise_detalhada", "N/A"),
            "nome_variante_vencedora": analysis_raw.get("nome_variante_vencedora", "N/A"),
            "decisao_acionavel": analysis_raw.get("decisao_acionavel", "N/A"),
            
            # Map back to English keys to ensure Module C (Google Sheets) and presentation layers don't break
            "executive_summary": analysis_raw.get("resumo_executivo", analysis_raw.get("executive_summary", "N/A")),
            "detailed_analysis": analysis_raw.get("analise_detalhada", analysis_raw.get("detailed_analysis", "N/A")),
            "winning_variant_name": analysis_raw.get("nome_variante_vencedora", analysis_raw.get("winning_variant_name", "N/A")),
            "actionable_decision": analysis_raw.get("decisao_acionavel", analysis_raw.get("actionable_decision", "N/A"))
        }
        
        return analysis
        
    except json.JSONDecodeError as e:
        raise ValueError(f"AI model returned an invalid JSON response. Response: {response_text}") from e
