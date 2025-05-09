from .export_details import ExportDetails
from dataclasses import dataclass
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

  def exports(self, sortby='inode'):
    rslt = sorted(self._exports(), key=lambda e: getattr(e, sortby))
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

  @classmethod
  def from_path(cls, path, linkbase):
    inode = path.stat().st_ino
    id = str(inode)
    link = f'{linkbase}/{id}'
    return Export(id, path, inode, link)

  def is_valid(self):
    if self.path.is_dir():
      return False

    return True

  def link(self):
    return f'./exports/{self.dir}{self.inode}/'

  def details(self):
    return ExportDetails.from_export(self)
      

class ExportManager:
  def __init__(self, dirs=None, exports_glob="*.xml"):
    if not dirs:
      dirs = os.environ.get('EXPORT_DIRS', '')

    if isinstance(dirs, str):
      # split on ":" in unix, ";" in windows
      dirs = dirs.split(os.pathsep)

    dirs = [Path(d) for d in dirs]
    dirs = [d for d in dirs if self.is_valid_dir(d)]
    dirs = [
      Directory.from_path(p, exports_glob=exports_glob)
      for p in dirs
    ]

    self.dirs_by_id = {d.id: d for d in dirs}

  def dirs(self, sortkey="id"):
    return sorted(self.dirs_by_id.values(), key=lambda d: getattr(d, sortkey))

  def is_valid_dir(self, d):
    return d.is_dir()
