#!/bin/sh

# The goal is this wrapper is to produce output that can be parsed by GitHub
# Action problem matcher, and generate an annotation. To achieve this we do the
# following:
#
#   1. Change message template to always use absolute paths.
#   2. Use "parseable" output format instead of "colorized".
#
# Some related upstream issues:
#
#   - https://github.com/PyCQA/pylint/issues/352


TEMPLATE='{abspath}:{line}:{column}: {msg_id}: {msg} ({symbol})'
FORMAT=parseable
BIN="${PYLINT_PATH:-pylint}"

exec "$BIN" --output-format="$FORMAT" --msg-template="$TEMPLATE" "$@"
