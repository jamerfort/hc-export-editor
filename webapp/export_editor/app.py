from flask import Flask, render_template, abort, request, redirect

from .export_manager import ExportManager
from .export_generator import generate_export, form_to_changes

app = Flask(__name__)
manager = ExportManager()

@app.errorhandler(404)
def page_not_found(error):
  code = 404
  description = 'Page not found'
  return render_template('error_page_not_found.html', code=code, description=description), code

@app.route('/')
def slash():
  return redirect('/exports')

@app.route("/exports")
def exports():
  dirs = manager.dirs()
  return render_template("exports.html", dirs=dirs)

@app.route("/exports/<did>")
def exports_dir(did):
  # did = Directory ID

  d = manager.dirs_by_id.get(did, None)

  if d == None:
    abort(404)

  return render_template("exports.html", dirs=[d])

@app.route("/exports/<did>/<eid>")
def edit_export(did, eid):
  # did = Directory ID
  # eid = Export ID

  d = manager.dirs_by_id.get(did, None)

  if d == None:
    abort(404)

  e = d.get_export(eid, None)

  if e == None:
    abort(404)

  return render_template("edit_export.html", dir=d, export=e, details=e.details())

@app.route("/exports/<did>/<eid>/modify", methods=['POST'])
def modify_export(did, eid):
  # did = Directory ID
  # eid = Export ID

  d = manager.dirs_by_id.get(did, None)

  if d == None:
    abort(404)

  e = d.get_export(eid, None)

  if e == None:
    abort(404)

  changes = form_to_changes(request.form)
  return generate_export(e.path, changes), {'Content-Type': 'application/xml'}
