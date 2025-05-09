from .export_details.interface import Interface
from .export_details.lookup_table import Table

from collections import OrderedDict
from dataclasses import dataclass
from lxml import etree
from typing import List

# Notes for modifying interface xml:
# parser = etree.XMLParser(strip_cdata=False)
# etree.parse(f, parser)
# etree.CDATA('\n' + etree.tostring(data, encoding='unicode', method='xml') + '\n')
#
# Manually write xml declaration:
# <?xml version="1.0" encoding="UTF-8"?>\n
# etree.tostring(root, encoding='UTF-8', xml_declaration=False)

@dataclass
class Change:
  type: str
  name: str
  value: str

@dataclass
class Item:
  type: str
  name: str
  changes: List[Change]

def form_to_changes(form):
  changes = OrderedDict()

  for (fullkey, value) in form.items():
    key, subkeys = fullkey.split('|', 1)
    keytype, keyname = key.split(':', 1)

    if key not in changes:
      changes[key] = Item(keytype, keyname, [])

    item = changes[key]

    changetype, changename = subkeys.split(':', 1)
    item.changes.append(Change(changetype, changename, value))

  return changes

def generate_export(export_path, changes):
  with open(export_path) as f:
    parser = etree.XMLParser(strip_cdata=False)
    root = etree.parse(f, parser)

    change_types = set([k.split(':')[0] for k in changes.keys()])
    
    if 'Interface' in change_types:
      Interface.apply_changes(root, changes)
    
    if 'Table' in change_types:
      Table.apply_changes(root, changes)
    
    yield '<?xml version="1.0" encoding="UTF-8"?>\n'
    yield etree.tostring(root, encoding='UTF-8', xml_declaration=False)
