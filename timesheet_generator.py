import pandas as pd
import os

def generate_csv(df, output_file="timesheet.csv"):
    """
    Save aggregated data as a CSV and return its path safely.
    """
    try:
        os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
        df.to_csv(output_file, index=False)
        print(f"✅ Timesheet CSV created: {output_file}")
        return {"status": "ok", "csv_path": os.path.abspath(output_file)}
    except Exception as e:
        print(f"❌ Error creating CSV: {e}")
        return {"status": "error", "message": str(e), "csv_path": None}
