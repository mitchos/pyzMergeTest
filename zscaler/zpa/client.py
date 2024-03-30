# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


class ZPAClient:
    def __init__():
        pass

    def get(
        self,
        path: str,
        json=None,
        params=None,
        fail_safe: bool = False,
        api_version: str = None,
    ):
        """
        Send a GET request to the ZPA API.
        Parameters:
        - path (str): API endpoint path.
        - json (str): the request body.
        - params (dict): the query params
        - api_version (str): the api version, availbale values: v1, v2, userconfig_v1, cbiconfig_v1
        """
        pass

    def get_paginated_data(
        self,
        path: str = None,
        data_key_name: str = None,
        data_per_page: int = 500,
        expected_status_code=200,
        api_version: str = None,
    ):
        """
        Send a GET request to the ZPA API to fetch all pages of a resources.
        Parameters:
        - path (str): API endpoint path.
        - data_key_name (str): list field key.
        - data_per_page: the page size
        - params (dict): the query params
        - api_version (str): the api version, availbale values: v1, v2, userconfig_v1 or cbiconfig
        """
        pass

    def put(self, path: str, json=None, params=None, api_version: str = None):
        """
        Send a PUT request to the ZPA API.
        Parameters:
        - path (str): API endpoint path.
        - json (str): the request body.
        - params (dict): the query params
        - api_version (str): the api version, availbale values: v1, v2, userconfig_v1 or cbiconfig
        """
        pass

    def patch(self, path: str, json=None, params=None, api_version: str = None):
        """
        Send a PATCH request to the ZPA API.
        Parameters:
        - path (str): API endpoint path.
        - json (str): the request body.
        - params (dict): the query params
        - api_version (str): the api version, availbale values: v1, v2, userconfig_v1 or cbiconfig
        """
        pass

    def post(self, path: str, json=None, params=None, api_version: str = None):
        """
        Send a POST request to the ZPA API.
        Parameters:
        - path (str): API endpoint path.
        - json (str): the request body.
        - params (dict): the query params
        - api_version (str): the api version, availbale values: v1, v2, userconfig_v1 or cbiconfig
        """
        pass

    def delete(self, path: str, json=None, params=None, api_version: str = None):
        """
        Send a DELETE request to the ZPA API.
        Parameters:
        - path (str): API endpoint path.
        - json (str): the request body.
        - params (dict): the query params
        - api_version (str): the api version, availbale values: v1, v2, userconfig_v1 or cbiconfig
        """
        pass
