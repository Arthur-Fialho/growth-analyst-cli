import os
import pandas as pd
import numpy as np

def clean_financial_value(val):
    """
    Sanitizes Brazilian currency strings (e.g., 'R$ 10.273', 'R$ 1.250,50') into floats.
    Returns None if the value is null, corrupt, or unparseable.
    """
    if pd.isna(val) or not isinstance(val, (str, int, float)):
        return None
    
    if isinstance(val, (int, float)):
        return float(val)
        
    val_clean = val.replace("R$", "").strip()
    if not val_clean:
        return None
    
    # Standard Brazilian Portuguese currency format:
    # Thousands separator: '.'
    # Decimal separator: ','
    # If both exist, e.g. 1.250,50: remove dot, replace comma with dot
    # If only comma exists, e.g. 1250,50: replace comma with dot
    # If only dot exists, e.g. 10.273: in these datasets, dots are thousands separators.
    # Therefore, remove all dots and replace commas with dots.
    val_clean = val_clean.replace(".", "")
    val_clean = val_clean.replace(",", ".")
    
    try:
        return float(val_clean)
    except ValueError:
        return None

def process_dataset(csv_path):
    """
    Loads and sanitizes the CSV file.
    Applies strict drop-row policy for null/corrupt values in key metrics.
    Returns:
        aggregated_df: pd.DataFrame with metrics grouped by 'Grupos de usuários'
        partner_name: str, name of the partner in the dataset
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at: {csv_path}")
        
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # 1. Drop rows missing crucial categorical strings
    df = df.dropna(subset=['Data', 'Grupos de usuários', 'Parceiro'])
    
    # 2. Clean numerical/financial columns
    # 'compradores' should be a valid integer
    def parse_buyers(val):
        try:
            val_int = int(float(val))
            return val_int if val_int >= 0 else None
        except (ValueError, TypeError):
            return None
            
    df['compradores'] = df['compradores'].apply(parse_buyers)
    df['comissão'] = df['comissão'].apply(clean_financial_value)
    df['cashback'] = df['cashback'].apply(clean_financial_value)
    df['vendas totais'] = df['vendas totais'].apply(clean_financial_value)
    
    # 3. Apply strict drop-row policy: drop rows with any null in key metrics
    df = df.dropna(subset=['compradores', 'comissão', 'cashback', 'vendas totais'])
    
    if df.empty:
        raise ValueError(f"No valid data remaining in {csv_path} after applying drop-row policy.")
        
    # Extract partner name (take the first one as it should be consistent)
    partner_name = str(df['Parceiro'].iloc[0]).strip()
    
    # 4. Group by 'Grupos de usuários' and calculate aggregates
    agg_df = df.groupby('Grupos de usuários').agg({
        'compradores': 'sum',
        'comissão': 'sum',
        'cashback': 'sum',
        'vendas totais': 'sum'
    }).reset_index()
    
    # Rename columns for clarity in Portuguese
    agg_df = agg_df.rename(columns={
        'Grupos de usuários': 'Grupo',
        'compradores': 'Total Compradores',
        'comissão': 'Total Comissão',
        'cashback': 'Total Cashback',
        'vendas totais': 'Total Vendas'
    })
    
    # Calculate ROI (commission - cashback)
    agg_df['ROI'] = agg_df['Total Comissão'] - agg_df['Total Cashback']
    
    # Additional growth metrics for LLM evaluation
    agg_df['ROI %'] = (agg_df['ROI'] / agg_df['Total Cashback']).replace([np.inf, -np.inf], 0).fillna(0) * 100
    agg_df['Ticket Médio'] = (agg_df['Total Vendas'] / agg_df['Total Compradores']).fillna(0)
    agg_df['Taxa de Comissão %'] = (agg_df['Total Comissão'] / agg_df['Total Vendas']).fillna(0) * 100
    agg_df['Taxa de Cashback %'] = (agg_df['Total Cashback'] / agg_df['Total Vendas']).fillna(0) * 100
    
    return agg_df, partner_name
