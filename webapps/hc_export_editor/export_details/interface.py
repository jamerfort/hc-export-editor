from dataclasses import dataclass
from lxml import etree
from typing import Dict

@dataclass
class Setting:
  name: str
  value: str
  target: str

  @classmethod
  def from_element(cls, el):
    name = el.get('Name')
    target = el.get('Target')
    value = el.text
    return Setting(name, value, target)

  def form_name(self):
    if self.name.startswith('@'):
      return f'Attr:{self.name[1:]}'

    return f'Setting:{self.name}'

@dataclass
class Attr:
  name: str
  value: str

@dataclass
class Interface:
  name: str
  attrs: Dict[str, Attr]
  settings: Dict[str, Setting]

  def settings_and_attrs(self):
    return list(self._settings_and_attrs())

  def _settings_and_attrs(self):
    for name, attr in self.attrs.items():
      yield Setting('@' + name, attr.value, "")

    for setting in self.settings.values():
      yield setting

  def form_name(self):
    return f'Interface:{self.name}'

  @classmethod
  def from_exportxml_tree(cls, tree):
    empty_setting = Setting('', '', '')

    for ptd in tree.xpath('//Document[starts-with(@name, "Settings:")]/ProjectTextDocument'):
      item = cls._etree_fromstring(ptd.text)
      name = item.attrib['Name']

      attrs = [Attr(name, value) for name, value in item.attrib.items()]
      attrs_dict = {a.name: a for a in attrs}

      settings = [Setting.from_element(s) for s in item.xpath('//Setting')]
      settings_dict = {s.name: s for s in settings}

      yield Interface(name, attrs_dict, settings_dict)

  @classmethod
  def _etree_fromstring(cls, text):
    try:
      item = etree.fromstring(text)
    except etree.XMLSyntaxError as e:
      if 'CData section not finished' in e.msg:
        return etree.fromstring(text.replace(']*]', ']]'))

    return item

  @classmethod
  def apply_changes(cls, tree, changes):
    for ptd in tree.xpath('//Document[starts-with(@name, "Settings:")]/ProjectTextDocument'):
      item = cls._etree_fromstring(ptd.text)
      modified = False
      name = item.attrib['Name']

      item_changes = changes.get(f'Interface:{name}', None)
      if item_changes == None:
        # skip to next interface
        continue
      
      for change in item_changes.changes:
        # Make sure we can't escape quotes
        if '"' in change.name:
          continue

        if change.type == 'Setting':
          for s in item.xpath(f'//Setting[@Name="{change.name}"]'):
            if s.text != change.value:
              s.text = change.value
              modified = True

        elif change.type == 'Attr':
          if change.name == 'Name':
            ptd.set('name', f'Settings:{change.value}')
            doc = ptd.getparent()
            doc.set('name', f'Settings:{change.value}.PTD')

            # allow to fall through to set the attribute

          if item.get(change.name) != change.value:
            item.set(change.name, change.value)
            modified = True

      if modified:
        ptd.text = etree.CDATA('\n' + etree.tostring(item, encoding='unicode', method='xml') + '\n')
