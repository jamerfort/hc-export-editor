#!/bin/bash

export EXPORT_DIRS="$PWD/exports_dir"
flask --app webapps/hc_export_editor/app run --debug "$@"
