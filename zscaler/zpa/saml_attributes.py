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


from box import Box, BoxList
from restfly import APISession
from restfly.endpoint import APIEndpoint

from zscaler.utils import Iterator


class SAMLAttributesAPI(APIEndpoint):
    def __init__(self, api: APISession):
        super().__init__(api)

        self.v2_url = api.v2_url

    def list_attributes(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured SAML attributes.

        Keyword Args:
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: A list of all configured SAML attributes.

        Examples:
            >>> for saml_attribute in zpa.saml_attributes.list_attributes():
            ...    pprint(saml_attribute)

        """
        return BoxList(Iterator(self._api, f"{self.v2_url}/samlAttribute", **kwargs))

    def list_attributes_by_idp(self, idp_id: str, **kwargs) -> BoxList:
        """
        Returns a list of all configured SAML attributes for the specified IdP.

        Args:
            idp_id (str): The unique id of the IdP to retrieve SAML attributes from.

        Keyword Args:
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`BoxList`: A list of all configured SAML attributes for the specified IdP.

        Examples:
            >>> for saml_attribute in zpa.saml_attributes.list_attributes_by_idp('99999'):
            ...    pprint(saml_attribute)

        """
        return BoxList(Iterator(self._api, f"{self.v2_url}/samlAttribute/idp/{idp_id}", **kwargs))

    def get_attribute(self, attribute_id: str) -> Box:
        """
        Returns information on the specified SAML attributes.

        Args:
            attribute_id (str):
                The unique identifier for the SAML attributes.

        Returns:
            :obj:`dict`: The resource record for the SAML attributes.

        Examples:
            >>> pprint(zpa.saml_attributes.get_attribute('99999'))

        """

        return self._get(f"samlAttribute/{attribute_id}")
