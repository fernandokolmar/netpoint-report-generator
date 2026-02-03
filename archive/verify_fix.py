"""
VERIFICATION SCRIPT: Test the fix works in the actual application
"""
import pandas as pd
from core.excel_generator import ExcelGenerator
import zipfile
import re

def create_test_data():
    """Create sample data matching the actual application structure"""

    # Sample data for each DataFrame
    dfs = {
        'totalizado_processed': pd.DataFrame({
            'Data': pd.to_datetime(['2024-01-01 10:00:00', '2024-01-01 10:01:00', '2024-01-01 10:02:00']),
            'Usuarios conectados': [100, 150, 120]
        }),

        'mensagens_processed': pd.DataFrame({
            'Data': ['10:00', '10:01', '10:02'],
            'Nome': ['Alice', 'Bob', 'Charlie'],
            'Mensagem': ['Hello', 'World', 'Test']
        }),

        'relatorio_processed': pd.DataFrame({
            'Nome': ['Alice', 'Bob'],
            'Tempo_Minutos': [90.5, 120.0],
            'Retenção (hh:mm)': ['1:30:00', '2:00:00']
        }),

        'inscritos_processed': pd.DataFrame({
            'Nome': ['Alice', 'Bob', 'Charlie'],
            'Data de Cadastro': ['01/01/2024', '02/01/2024', '03/01/2024']
        })
    }

    return dfs

def verify_xml_attributes(filename):
    """Verify all tables have correct XML attributes"""

    print(f"\nVerifying {filename}...")
    print("="*70)

    with zipfile.ZipFile(filename, 'r') as z:
        table_files = [f for f in z.namelist() if f.startswith('xl/tables/table') and f.endswith('.xml')]

        all_good = True

        for table_file in table_files:
            xml = z.read(table_file).decode('utf-8')

            # Extract table name
            name_match = re.search(r'displayName="([^"]+)"', xml)
            table_name = name_match.group(1) if name_match else "UNKNOWN"

            # Check for totalsRowShown
            totals_shown_match = re.search(r'totalsRowShown="([^"]+)"', xml)
            totals_shown = totals_shown_match.group(1) if totals_shown_match else None

            # Check for totalsRowCount
            totals_count_match = re.search(r'totalsRowCount="([^"]+)"', xml)
            totals_count = totals_count_match.group(1) if totals_count_match else None

            print(f"\n{table_file}:")
            print(f"  Table name: {table_name}")
            print(f"  totalsRowShown: {totals_shown}")
            print(f"  totalsRowCount: {totals_count}")

            # Validate
            if totals_shown == "1" and totals_count != "1":
                print(f"  ERROR: totalsRowShown=1 but totalsRowCount={totals_count}")
                print(f"  This WILL cause corruption!")
                all_good = False
            elif totals_shown == "1" and totals_count == "1":
                print(f"  OK: Totals row properly configured")
            elif totals_shown is None or totals_shown == "0":
                print(f"  OK: No totals row")

        print("\n" + "="*70)
        if all_good:
            print("VERIFICATION PASSED: All tables correctly configured!")
            print("File should open in Excel WITHOUT corruption errors.")
        else:
            print("VERIFICATION FAILED: Some tables missing totalsRowCount!")
            print("File WILL show corruption errors in Excel.")
        print("="*70)

        return all_good

def main():
    print("="*70)
    print(" TESTING THE FIX IN ACTUAL APPLICATION")
    print("="*70)

    # Create test data
    print("\n1. Creating test data...")
    dfs = create_test_data()

    # Generate Excel file using the FIXED code
    print("\n2. Generating Excel file with ExcelGenerator...")
    generator = ExcelGenerator(progress_callback=print)

    output_file = "test_FINAL_VERIFICATION.xlsx"

    try:
        generator.generate(dfs, output_file)
        print(f"\n3. File generated: {output_file}")
    except Exception as e:
        print(f"\nERROR generating file: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Verify XML attributes
    print("\n4. Verifying XML attributes...")
    result = verify_xml_attributes(output_file)

    if result:
        print("\n" + "="*70)
        print(" SUCCESS!")
        print("="*70)
        print(f"\nThe fix is working correctly!")
        print(f"\nNext step: Open {output_file} in Excel")
        print(f"Expected result: File opens WITHOUT any corruption errors")
        print("="*70)
    else:
        print("\n" + "="*70)
        print(" FAILED!")
        print("="*70)
        print("\nThe fix did NOT work correctly.")
        print("Please review the code changes.")
        print("="*70)

    return result

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
