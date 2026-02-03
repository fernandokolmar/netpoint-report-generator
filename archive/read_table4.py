import zipfile
import re
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

z = zipfile.ZipFile('Temple PRSA  - estatísitcas - 2025-11-18.xlsx')
xml = z.read('xl/tables/table4.xml').decode('utf-8')

name = re.search(r'name="([^"]+)"', xml)
ref = re.search(r'ref="([^"]+)"', xml)
totals = re.search(r'totalsRowShown="([^"]+)"', xml)
totals_count = re.search(r'totalsRowCount="([^"]+)"', xml)

print(f'name={name.group(1) if name else "?"}')
print(f'ref={ref.group(1) if ref else "?"}')
print(f'totalsRowShown={totals.group(1) if totals else "N/A"}')
print(f'totalsRowCount={totals_count.group(1) if totals_count else "N/A"}')
