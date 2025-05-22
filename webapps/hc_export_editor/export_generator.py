from export_details.interface import Interface
from export_details.lookup_table import Table
from export_details.toc import TOC

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
  action: str
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
    # key|subkeys[|action]
    # keytype:keyname|changetype:changename[|action]
    # Table:USER.ExampleTable|Row:key1
    # Interface:operation1|Attr:Name
    # Interface:operation3|Setting:HTTPPort
    # Interface:operation3|Setting:HTTPPort|set
    # Interface:operation1|Setting:HTTPPort|delete
    # TOC:3848931|PTD:Settings:operation3.PTD|delete
    key, _, subkeys = fullkey.partition('|')
    if '|' in subkeys:
      subkeys, _, action = subkeys.partition('|')
    else:
      action = ''

    if not action:
      action = 'set'
    
    keytype, _, keyname = key.partition(':')

    if key not in changes:
      changes[key] = Item(keytype, keyname, [])

    item = changes[key]

    changetype, _, changename = subkeys.partition(':')
    change = Change(action, changetype, changename, value)
    item.changes.append(change)

  return changes

def generate_export(export_path, changes):
  with open(export_path) as f:
    parser = etree.XMLParser(strip_cdata=False)
    root = etree.parse(f, parser)

    change_types = set([k.partition(':')[0] for k in changes.keys()])

    if 'TOC' in change_types:
      # This will remove any items being removed
      # before modifying the same items below.
      TOC.apply_changes(root, changes)
    
    if 'Interface' in change_types:
      Interface.apply_changes(root, changes)
    
    if 'Table' in change_types:
      Table.apply_changes(root, changes)
    
    yield '<?xml version="1.0" encoding="UTF-8"?>\n'
    yield etree.tostring(root, encoding='UTF-8', xml_declaration=False)
