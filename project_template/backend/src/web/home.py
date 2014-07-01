# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.tmpl_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from web import my_form, rest
from tekton import router


@no_csrf
def index():
    url = router.to_path(my_form)

    return TemplateResponse({'form_url': url,
                             'ajax_path': router.to_path(rest.items)})
