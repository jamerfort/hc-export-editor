#!/bin/bash

export EXPORT_DIRS="$PWD/exports_dir"
flask --app webapp/export_editor/app run --debug
