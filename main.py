import os
import sys
import argparse
from dotenv import load_dotenv

# Import our modular subsystems
from src.data_processor import process_dataset
from src.ai_analyzer import analyze_growth_data
from src.report_generator import generate_markdown_report, print_terminal_summary
from src.sheets_tracker import record_test_result

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Set up command-line arguments
    parser = argparse.ArgumentParser(
        description="Growth-Analyst AI-Native CLI: Processes A/B test data for cashback variations and returns a complete analysis with an actionable decision."
    )
    parser.add_argument(
        "csv_path",
        help="Path to the CSV dataset file containing A/B test data."
    )
    parser.add_argument(
        "--sheet-id",
        help="Google Sheet ID to append results. If not specified, reads GOOGLE_SHEET_ID from .env."
    )
    parser.add_argument(
        "--test-name",
        help="Name of the test to record. Defaults to 'A/B Test - [Partner Name]'."
    )
    parser.add_argument(
        "--test-description",
        help="Description of the test to record. Defaults to 'Analysis of cashback variations for [Partner Name]'."
    )
    
    args = parser.parse_args()
    
    csv_path = args.csv_path
    
    # Smart Data Routing:
    # Check if the provided file is already inside the data/ directory.
    # If not, automatically copy it to the data/ directory.
    try:
        import shutil
        abs_csv_path = os.path.abspath(csv_path)
        data_dir = os.path.abspath("data")
        os.makedirs(data_dir, exist_ok=True)
        
        if not os.path.exists(abs_csv_path):
            raise FileNotFoundError(f"Dataset not found at: {csv_path}")
            
        in_data_dir = abs_csv_path.startswith(data_dir + os.sep) or abs_csv_path == os.path.join(data_dir, os.path.basename(abs_csv_path))
        if not in_data_dir:
            destination = os.path.join(data_dir, os.path.basename(csv_path))
            shutil.copy2(abs_csv_path, destination)
            print(f"📂 File copied to local data directory for organization: {destination}")
            csv_path = destination
    except Exception as e:
        print(f"⚠️ Smart data routing warning: {str(e)}. Proceeding with original path.", file=sys.stderr)
        
    print(f"🚀 Starting analysis for dataset: {csv_path}")
    
    # Step A: Data processing and sanitization
    try:
        agg_df, partner_name = process_dataset(csv_path)
        print(f"✅ Data processed successfully for Partner: {partner_name}")
    except FileNotFoundError as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Data processing failed: {str(e)}", file=sys.stderr)
        sys.exit(1)
        
    # Step B: AI Growth Analysis (Gemini)
    try:
        print("🤖 Running AI Growth Analysis using Gemini API...")
        ai_analysis = analyze_growth_data(agg_df, partner_name)
        print("✅ AI analysis completed.")
    except Exception as e:
        print(f"❌ AI analysis failed: {str(e)}", file=sys.stderr)
        sys.exit(1)
        
    # Step D: Presentation Layer (Markdown Report & Terminal Summary)
    try:
        report_path, html_report_path = generate_markdown_report(agg_df, partner_name, csv_path, ai_analysis)
        print_terminal_summary(agg_df, partner_name, ai_analysis, report_path, html_report_path)
    except Exception as e:
        print(f"❌ Presentation layer generation failed: {str(e)}", file=sys.stderr)
        sys.exit(1)
        
    # Step C: Storage and Tracking (Google Sheets API or Local Fallback)
    try:
        # Determine test metadata for logging
        test_name = args.test_name or f"A/B Test - {partner_name}"
        test_description = args.test_description or f"Analysis of cashback variations for {partner_name}"
        winning_variant = ai_analysis.get('winning_variant_name', 'Nenhum')
        actionable_decision = ai_analysis.get('actionable_decision', 'N/A')
        
        # Calculate Net ROI of the winning variant or overall test
        winning_row = agg_df[agg_df['Grupo'] == winning_variant]
        if not winning_row.empty:
            net_roi = float(winning_row.iloc[0]['ROI'])
        else:
            net_roi = float(agg_df['ROI'].sum())
            
        print("logging result to tracker...")
        record_test_result(
            test_name=test_name,
            description=test_description,
            winning_variant=winning_variant,
            actionable_decision=actionable_decision,
            net_roi=net_roi,
            sheet_id_override=args.sheet_id
        )
    except Exception as e:
        print(f"⚠️ Tracking failed: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()
