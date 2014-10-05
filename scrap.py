import xml.etree.ElementTree as ET

tree=ET.parse('startup.xml')
root=tree.getroot()

for chk in root[0]:
    print chk.tag
    print chk.text