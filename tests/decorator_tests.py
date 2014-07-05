# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest
from base import GAETestCase
from gaecookie import facade
from gaecookie.decorator import is_csrf_secure, no_csrf
from gaecookie.middleware import CSRFMiddleware, CSRFInputToDependency
from mock import Mock


class CSRFTests(unittest.TestCase):
    def test_secure_function(self):
        def secure():
            pass

        self.assertTrue(is_csrf_secure(secure))

    def test_unsecure_function(self):
        @no_csrf
        def unsecure():
            self.executed = True

        self.assertFalse(is_csrf_secure(unsecure))
        unsecure()
        self.assertTrue(self.executed)


class MiddlewareTests(GAETestCase):
    def assert_csrf_setup(self, dependencies, handler):
        set_cookies_args = handler.response.method_calls[0][1]
        cookie_name, token = set_cookies_args
        self.assertEqual(cookie_name, 'XSRF-RANDOM')
        extracted_code = facade.retrieve('XSRF-RANDOM', token).execute().result
        self.assertEqual(dependencies['_csrf_code'], extracted_code)

    def test_first_access_unsecure_handler(self):
        handler = Mock()
        handler.request.method = 'GET'
        handler.request.cookies.get = Mock(return_value=None)

        @no_csrf
        def unsecure():
            pass

        dependencies = {'_fcn': unsecure}
        request_args = {}
        csrf_middleware = CSRFMiddleware(handler, dependencies, request_args)
        self.assertFalse(csrf_middleware.set_up())
        self.assert_csrf_setup(dependencies, handler)

    def test_http_get_no_working_on_secure(self):
        handler = Mock()
        handler.request.method = 'GET'

        # Making a perfect valid call but the http method GET
        csrf_code = 'abc'
        token = facade.sign('XSRF-RANDOM', csrf_code).execute().result

        def get_cookie(name):
            if name == 'XSRF-RANDOM':
                return token

        handler.request.cookies.get = get_cookie

        def secure():
            pass

        dependencies = {'_fcn': secure}
        request_args = {'_csrf_code': csrf_code}
        # removes _csrf_code from request_args to dependencies
        CSRFInputToDependency(handler, dependencies, request_args).set_up()
        csrf_middleware = CSRFMiddleware(handler, dependencies, request_args)
        self.assertTrue(csrf_middleware.set_up(), 'should be false because the http method is GET')


    def test_first_access_secure_handler(self):
        handler = Mock()
        handler.request.cookies.get = Mock(return_value=None)

        def secure():
            pass

        dependencies = {'_fcn': secure}
        request_args = {}
        csrf_middleware = CSRFMiddleware(handler, dependencies, request_args)
        self.assertTrue(csrf_middleware.set_up())
        self.assert_csrf_setup(dependencies, handler)

    def test_secure_angular_ajax_access(self):
        handler = Mock()
        csrf_code = 'abc'
        token = facade.sign('XSRF-RANDOM', csrf_code).execute().result

        handler.request.cookies.get = lambda k: token
        handler.request.headers.get = lambda k: csrf_code

        def secure():
            pass

        dependencies = {'_fcn': secure}
        request_args = {}
        csrf_middleware = CSRFMiddleware(handler, dependencies, request_args)
        self.assertFalse(csrf_middleware.set_up())

    def test_secure_form_access(self):
        handler = Mock()
        csrf_code = 'abc'
        token = facade.sign('XSRF-RANDOM', csrf_code).execute().result

        def get_cookie(name):
            if name == 'XSRF-RANDOM':
                return token

        handler.request.cookies.get = get_cookie

        def secure():
            pass

        dependencies = {'_fcn': secure}
        request_args = {'_csrf_code': csrf_code}
        # removes _csrf_code from request_args to dependencies
        CSRFInputToDependency(handler, dependencies, request_args).set_up()
        csrf_middleware = CSRFMiddleware(handler, dependencies, request_args)
        self.assertFalse(csrf_middleware.set_up())
        self.assertDictEqual({}, request_args, '_csrf_code must be removed from request_args')
