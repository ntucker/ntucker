#!/usr/bin/env python
from __future__ import unicode_literals
import os
import sys

sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)),'ntucker'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ntucker.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)