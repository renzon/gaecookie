# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.tmpl_middleware import TemplateMiddleware, TemplateWriteMiddleware
from gaecookie.middleware import CSRFMiddleware, CSRFInputToDependency
from tekton.gae.middleware.json_middleware import JsonResponseMiddleware
from tekton.gae.middleware.redirect import RedirectMiddleware
from tekton.gae.middleware.email_errors import EmailMiddleware
from tekton.gae.middleware.parameter import RequestParamsMiddleware
from tekton.gae.middleware.router_middleware import RouterMiddleware, ExecutionMiddleware
from tekton.gae.middleware.webapp2_dependencies import Webapp2Dependencies

SENDER_EMAIL = 'renzon@gmail.com'
TEMPLATE_404_ERROR = 'base/404.html'
TEMPLATE_400_ERROR = 'base/400.html'
MIDDLEWARES = [TemplateMiddleware,
               EmailMiddleware,
               Webapp2Dependencies,
               RequestParamsMiddleware,
               CSRFInputToDependency,
               RouterMiddleware,
               CSRFMiddleware,
               ExecutionMiddleware,
               TemplateWriteMiddleware,
               JsonResponseMiddleware,
               RedirectMiddleware]

