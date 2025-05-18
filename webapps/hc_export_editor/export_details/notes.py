from dataclasses import dataclass
from lxml import etree
from typing import List

@dataclass
class Notes:
  utc: str
  production: str
  namespace: str
  instance: str
  machine: str
  user: str
  notes: str

  def as_fields(self):
    yield ('UTC', self.utc)
    yield ('Production', self.production)
    yield ('Namespace', self.namespace)
    yield ('Instance', self.instance)
    yield ('Machine', self.machine)
    yield ('User', self.user)
    yield ('Notes', self.notes)

  @classmethod
  def from_exportxml_tree(cls, tree):

    for ptd in tree.xpath('//ProjectTextDocument[starts-with(@name, "EnsExportNotes")]'):
      deployment = etree.fromstring(ptd.text)

      utc = ''
      production = ''
      namespace = ''
      instance = ''
      machine = ''
      user = ''
      notes = ''

      for el in deployment.xpath('//Machine'):
        machine = el.text

      for el in deployment.xpath('//Instance'):
        instance = el.text

      for el in deployment.xpath('//Namespace'):
        namespace = el.text

      for el in deployment.xpath('//SourceProduction'):
        production = el.text

      for el in deployment.xpath('//Username'):
        user = el.text

      for el in deployment.xpath('//UTC'):
        utc = el.text

      notes = '\n'.join([l.text for l in deployment.xpath('//Notes/Line')])

      yield Notes(utc, production, namespace, instance, machine, user, notes)
