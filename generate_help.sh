#!/bin/bash

. ./setup.sh

if [ ! -e "$(which markdown_py)" ]
then
  pip install markdown
fi

rm webapps/hc_export_editor/static/docs/images/*
cp -p docs/images/* webapps/hc_export_editor/static/docs/images/

(
echo '{% extends "base.html" %}'
echo '{% block title %}Help{% endblock %}'
echo '{% block body %}'
echo '<div class="help">'

cmark-gfm -e table README.md | sed "s|./docs/images/\(.*png\)|{{url_for('static', filename='./docs/images/\1')}}|g"

echo '</div>'
echo '{% endblock %}'
) > webapps/hc_export_editor/templates/help.html

