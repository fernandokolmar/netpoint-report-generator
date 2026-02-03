import zipfile
from xml.dom import minidom

# Read the table XML from template
z = zipfile.ZipFile('Temple PRSA  - estatísitcas - 2025-11-18.xlsx')
xml_content = z.read('xl/tables/table2.xml').decode('utf-8')

# Parse and pretty print
dom = minidom.parseString(xml_content)
print(dom.toprettyxml())
