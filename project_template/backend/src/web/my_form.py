# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.tmpl_middleware import TemplateResponse


def index(name):
    return TemplateResponse({'name': name}, 'form.html')
