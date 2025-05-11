from .toc import TOC
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
    self.toc = self.read_toc()
    self.interfaces = self.read_interfaces()
    self.tables = self.read_tables()

  def read_toc(self):
    with open(self.export.path) as f:
      root = etree.parse(f)
      return list(TOC.from_exportxml_tree(root))

  def read_interfaces(self):
    with open(self.export.path) as f:
      root = etree.parse(f)
      return list(Interface.from_exportxml_tree(root))

  def read_tables(self):
    with open(self.export.path) as f:
      root = etree.parse(f)
      return list(Table.from_exportxml_tree(root))
