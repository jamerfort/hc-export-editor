from dataclasses import dataclass
from typing import List

@dataclass
class TOCEntry:
  name: str
  type: str

  @classmethod
  def from_element(cls, el):
    key = el.get('key', '')
    value = el.text
    return Row(key, value)

  def form_name(self):
    return f'Row:{self.key}'

@dataclass
class TOC:
  entries: List[TOCEntry]

  @classmethod
  def from_exportxml_tree(cls, tree):
    for item in tree.xpath('/Export/Project/Items/ProjectItem'):
      name = item.get('name', '')
      itype = item.get('type', '')

      yield TOCEntry(name, itype)

@dataclass
class AltTOC:
  entries: List[TOCEntry]

  @classmethod
  def from_exportxml_tree(cls, tree):
    # If there's an actual TOC, return nothing
    if tree.xpath('/Export/Project/Items/ProjectItem'):
      return

    for item in tree.xpath('/*/*'):
      itype = item.tag

      if itype == 'Task':
        name_el = item.xpath('./Name')[0]
        name = name_el.text

      else:
        name = item.get('name', '')
        Name = item.get('Name', '')
        name = name or Name

      yield TOCEntry(name, itype)
