import zipfile
import re

z = zipfile.ZipFile('Temple PRSA  - estatísitcas - 2025-11-18.xlsx')

for i in range(1, 6):
    try:
        xml = z.read(f'xl/tables/table{i}.xml').decode()
        name = re.search(r'name="([^"]+)"', xml)
        ref = re.search(r'ref="([^"]+)"', xml)
        totals = re.search(r'totalsRowShown="([^"]+)"', xml)
        totals_count = re.search(r'totalsRowCount="([^"]+)"', xml)

        print(f'table{i}.xml:')
        print(f'  name={name.group(1) if name else "?"}')
        print(f'  ref={ref.group(1) if ref else "?"}')
        print(f'  totalsRowShown={totals.group(1) if totals else "N/A"}')
        print(f'  totalsRowCount={totals_count.group(1) if totals_count else "N/A"}')
        print()
    except Exception as e:
        print(f"Error reading table{i}: {e}")
        print()
