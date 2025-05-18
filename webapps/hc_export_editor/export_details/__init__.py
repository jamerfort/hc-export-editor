from .notes import Notes
from .toc import TOC, AltTOC
from .interface import Interface
from .lookup_table import Table

from dataclasses import dataclass
from lxml import etree
from typing import Dict, List

class ExportDetails:
  @classmethod
  def from_export(cls, export):
    return ExportDetails(export)

  def __init__(self, export):
    self.export = export

    with open(self.export.path) as f:
      root = etree.parse(f)

      self.notes = self.read_notes(root)
      self.toc = self.read_toc(root)
      self.alt_toc = self.read_alttoc(root)
      self.interfaces = self.read_interfaces(root)
      self.tables = self.read_tables(root)

  def read_notes(self, root):
    return list(Notes.from_exportxml_tree(root))

  def read_toc(self, root):
    return list(TOC.from_exportxml_tree(root))

  def read_alttoc(self, root):
    return list(AltTOC.from_exportxml_tree(root))

  def read_interfaces(self, root):
    return list(Interface.from_exportxml_tree(root))

  def read_tables(self, root):
    return list(Table.from_exportxml_tree(root))
