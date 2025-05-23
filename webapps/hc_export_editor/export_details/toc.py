from dataclasses import dataclass
from typing import List

@dataclass
class TOCEntry:
  name: str
  type: str

  def form_name(self):
    return f'TOC:{self.name}'

@dataclass
class TOC:
  entries: List[TOCEntry]

  @classmethod
  def from_exportxml_tree(cls, tree):
    for item in tree.xpath('/Export/Project/Items/ProjectItem'):
      name = item.get('name', '')
      itype = item.get('type', '')

      yield TOCEntry(name, itype)

  @classmethod
  def apply_changes(cls, tree, changes):
    for item in tree.xpath('/Export/Project/Items/ProjectItem'):
      name = item.get('name', '')
      itype = item.get('type', '')

      item_changes = changes.get(f'TOC:{name}', None)
      if item_changes == None:
        # skip to next toc item
        continue
      
      for change in item_changes.changes:
        # Make sure we can't escape quotes
        if '"' in change.name:
          continue

        if change.action == 'delete':
          # Remove from toc
          item.getparent().remove(item)

          # Remove from body
          for doc in tree.xpath('/Export/*'):
            docname = doc.get('name')
            docName = doc.get('Name')
            docname = docname or docName

            if docname == name:
              doc.getparent().remove(doc)
              break

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
