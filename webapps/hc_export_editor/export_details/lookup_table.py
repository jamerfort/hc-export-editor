from dataclasses import dataclass
from typing import List

@dataclass
class Row:
  key: str
  value: str

  @classmethod
  def from_element(cls, el):
    key = el.get('key', '')
    value = el.text
    return Row(key, value)

  def form_name(self):
    return f'Row:{self.key}'

@dataclass
class Table:
  name: str
  rows: List[Row]

  def form_name(self):
    return f'Table:{self.name}'

  @classmethod
  def from_exportxml_tree(cls, tree):
      for lut in tree.xpath('//Document/lookupTable'):
        name = lut.getparent().attrib['name'].rstrip('.LUT')

        rows = [Row.from_element(entry) for entry in lut.xpath('./entry')]

        yield Table(name, rows)

  @classmethod
  def apply_changes(cls, tree, changes):
    for lut in tree.xpath('//Document/lookupTable'):
      modified = False
      name = lut.getparent().attrib['name'].rstrip('.LUT')

      item_changes = changes.get(f'Table:{name}', None)
      if item_changes == None:
        # skip to next table
        continue
      
      for change in item_changes.changes:
        # Make sure we can't escape quotes
        if '"' in change.name:
          continue

        if change.type == 'Row':
          for r in lut.xpath(f'./entry[@key="{change.name}"]'):
            if r.text != change.value:
              r.text = change.value
              modified = True
