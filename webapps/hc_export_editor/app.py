from flask import Flask, render_template, abort, request, redirect, url_for

import export_manager
import export_generator

app = Flask(__name__)
manager = export_manager.ExportManager()

@app.errorhandler(404)
def page_not_found(error):
  code = 404
  description = 'Page not found'
  return render_template('error_page_not_found.html', code=code, description=description), code

@app.route('/')
def slash():
  return redirect(url_for('exports'))

@app.route('/reload')
def reload():
  manager.reload()
  dirs = manager.dirs()
  return render_template("exports.html", dirs=dirs, notify="Reloaded configuration...")

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

  suffix = '_modified'

  headers = {
    'Content-Type': 'application/xml',
    'Content-Disposition': f'attachment;filename={e.path.stem}{suffix}.xml',
  }

  changes = export_generator.form_to_changes(request.form)
  return export_generator.generate_export(e.path, changes), headers
