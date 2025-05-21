from collections import OrderedDict
from dataclasses import dataclass
from export_details import ExportDetails, TOC, AltTOC, Notes
from lxml import etree
from typing import List
import datetime
import os
from pathlib import Path

@dataclass
class Directory:
  id: str
  path: str
  inode: int
  exports_glob: str
  link: str

  @classmethod
  def from_path(cls, path, exports_glob="*.xml"):
    inode = path.stat().st_ino
    id = str(inode)
    link = f'/exports/{id}'
    return Directory(id, path, inode, exports_glob, link)

  def _exports(self):
    for f in self.path.glob(self.exports_glob):
      e = Export.from_path(f, self.link)
      if e.is_valid():
        yield e

  def exports(self, sortby='mtime', reverse=True):
    rslt = sorted(self._exports(), key=lambda e: getattr(e, sortby), reverse=reverse)
    return rslt

  def get_export(self, id, default=None):
    for e in self._exports():
      if e.id == id:
        return e

    return default

@dataclass
class Export:
  id: str
  path: str
  inode: int
  link: str
  date_modified: str = ''
  mtime: int = 0
  _notes: List[Notes] = None
  _contents: List[TOC] = None

  @classmethod
  def from_path(cls, path, linkbase):
    stat = path.stat()
    inode = stat.st_ino
    id = str(inode)
    link = f'{linkbase}/{id}'
    mtime = stat.st_mtime
    date_modified = datetime.datetime.fromtimestamp(stat.st_mtime)
    return Export(id, path, inode, link, date_modified, mtime)

  def is_valid(self):
    if self.path.is_dir():
      return False

    return True

  def link(self):
    return f'./exports/{self.dir}{self.inode}/'

  def details(self):
    return ExportDetails.from_export(self)

  def __parse_file(self):
    if self._notes == None or self._contents == None:
      try:
        with open(self.path) as f:
          root = etree.parse(f)

          self._notes = list(Notes.from_exportxml_tree(root))

          self._contents = [
            *TOC.from_exportxml_tree(root),
            *AltTOC.from_exportxml_tree(root),
          ]

      except Exception as e:
        pass

  def contents(self):
    self.__parse_file()
    return self._contents or []

  def content_names(self):
    return [c.name for c in self.contents()]

  def notes(self):
    self.__parse_file()
    if self._notes:
      return self._notes[0]

    return None

class ExportManager:
  def __init__(self, dirs=None, exports_glob="*.xml"):
    self.reload()

  def reload(self, dirs=None, exports_glob="*.xml"):
    dirs = self._find_dirs_exists(dirs)

    dirs = [
      Directory.from_path(p, exports_glob=exports_glob)
      for p in dirs
    ]

    self.dirs_by_id = OrderedDict()
    for d in dirs:
      self.dirs_by_id[d.id] = d

  @classmethod
  def _find_dirs_exists(cls, dirs=None):
    for p in cls._find_dirs(dirs):
      if p.exists() and p.is_dir():
        yield p

  @classmethod
  def _find_dirs(cls, dirs=None):

    # dirs ######################################################
    if dirs:
      if isinstance(dirs, str):
        # split on ":" in unix, ";" in windows
        for d in dirs.split(os.pathsep):
          yield Path(d)

        return
    
    # iris global ###############################################
    try:
      import iris

      # Check for global configuration
      config = iris.gref('^hc.export.editor.config')
      if config.data(['dirs']):
        dirs = config.get(['dirs']).strip()
        if dirs:
          for d in dirs.split(os.pathsep):
            yield Path(d)
          
          # Return here, as this overrides all other directory options
          return
    except:
      pass

    # environment vars ##########################################
    envdirs = os.environ.get('EXPORT_DIRS', '')
    if envdirs:
      for d in envdirs.split(os.pathsep):
        if d != '':
          yield Path(d)
      return
    
    # iris defaults #############################################
    try:
      import iris
      iris_installdir = iris.system.Util.InstallDirectory()

      yield Path(iris_installdir) / 'exports'
      yield Path(iris_installdir) / 'mgr' / 'exports'

    except:
      pass

  def dirs(self):
    return self.dirs_by_id.values()
