# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest
from base import GAETestCase
from gaecookie.cookie import RetrieveCookieData
from gaecookie.security import SignCmd
from mock import Mock
from gaecookie import cookie, facade


class DeleteCookieTests(unittest.TestCase):
    def test_success(self):
        resp = Mock()
        cmd = facade.delete_cookie(resp, 'user')
        cmd.execute()
        resp.delete_cookie.assert_called_once_with('user')


class WriteCookieTests(GAETestCase):
    def test_success(self):
        resp = Mock()
        cmd = facade.write_cookie(resp, 'user', 'foo')
        cmd.execute()
        self.assertTrue(resp.set_cookie.called)
        self.assertEqual('user', resp.set_cookie.call_args[0][0])
        self.assertTrue(resp.set_cookie.call_args[1]['httponly'])

class RetrieveCookieDataTests(GAETestCase):
    def test_success(self):
        user_detail = {'email': 'foo@bar.com', 'id': '4'}
        sign_cmd = SignCmd('user', user_detail)
        sign_cmd.execute()
        request = Mock()
        request.cookies.get = Mock(return_value=sign_cmd.result)
        retrieve_cmd = RetrieveCookieData(request, 'user')
        retrieve_cmd.execute()
        self.assertDictEqual(user_detail, retrieve_cmd.result)