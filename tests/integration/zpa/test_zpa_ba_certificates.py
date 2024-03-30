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


def test_list_certificates(zpa):
    resp = zpa.certificates.list_issued_certificates()

    assert isinstance(resp, BoxList), "Response is not in the expected BoxList format."
    assert len(resp) > 0, "No certificates were found."

    first_certificate = resp[0]
    assert "id" in first_certificate, "The certificate does not have an 'id' attribute."


def test_get_certificate(zpa):
    certificates_list = zpa.certificates.list_issued_certificates()
    assert len(certificates_list) > 0, "No certificates to retrieve."

    first_certificate_id = certificates_list[0].id
    resp = zpa.certificates.get_certificate(first_certificate_id)

    assert isinstance(resp, Box), "Response is not in the expected Box format."
    assert (
        resp.id == first_certificate_id
    ), f"Retrieved certificate ID does not match requested ID: {first_certificate_id}"
