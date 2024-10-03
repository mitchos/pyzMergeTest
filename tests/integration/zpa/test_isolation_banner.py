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

import pytest

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestCBIBanners:
    """
    Integration Tests for the Cloud Browser Isolation Banner
    """

    def test_cbi_banner(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        banner_name = "tests-" + generate_random_string()
        banner_id = None  # Define banner_id here to ensure it's accessible throughout

        try:
            # Create a new isolation banner
            created_banner = client.isolation.add_banner(
                name=banner_name,
                logo="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAYQAAABQCAMAAAAuu/JsAAADAFBMVEUAAAAAgL8Ad8MAdr8Ad78Ad78Ad78Adr4Ad74Adr4Ad74Adr8Adr4Ad74Ad74Adr4Adr4Ad74Ad78AeL8Ad8AAd8AAeb4AgL8AktsAesAAd74Adr8Adr4Adr4Adr4Ad78AeMAAgMYAeL8Ad74Adr8Ad74AgP8Ae8EAd8AAdr8Ad8EA//8Ad78Ad74Aeb4Ae8YAdr4Ad74Adr8Ad74Ad78Adr8Ad78Adr4Ad78Adr8Ad78Ad74Ad8EAd78Adr8Ad78AeL4AecAAeckAeL8Ad78Ad74Ad74Ad78AecIAdr8Ad78Ad74Aer4AicQAd74Ad74AecAAi9EAfMEAd8AAeL8Ad78Ad78Ad78Ad74Ad78Ad8QAdsIAgMUAeL8Ad78Ad78AfMEAd8AAd78Ad78Ad78Adr8Ad74Adr8Ad74AeL8AeL4Ad74Adr4Aer8AecAAdr4AeMEAqv8Adr4Adr8Adr8AeL8Ad74Ad74Adr8Adr8Ad78AdsAAd78AeMEAdr8AgL8Aeb8AdsEAd78Adr8Ad78AgMgAd8AAeL4Ad78Adr4Ad78AecIAe78AeL8AgMQAd74Adr8AeMAAdr8AecEAgL8AeL4AmcwAdr8Adr8Ad74Ad78AesgAdr8AeL8AfMQAeL8AjsYAd78Ad78AecMAd78AdsEAeMAAd78Ad78AesIAdr8Ad74Aeb8AeMEAeMMAd8QAd8wAeL8Ad74Ad78AdsAAfMUAd78Adr4AeMMAgNUAgMwAd78Ad8AAd74AdsAAeL4Adr8Ad78Aeb4AesIAeL8Adr8AeL8Ad78AgL8Adr8Ad8EAdr8Ad78Ad74Adr8Ad74Adr4AeL4Ad78Ad78Adr8Ad74Ad78Ad78Ad74AgL8AeMAAdr8Ad8EAd74AeMAAd74Ad78Ad8AAdsAAd74Adr8AesIAdr8Adr8AeL8Ae8UAeb8AeMEAeL8AeMAAd78Ad8EAdsAAdr8AecEAer8Adr4Adr4Ad74Adr8Ad8AAd78Adr8AeL8Ad74Ad8EAeMAAdr5kTMBRAAABAHRSTlMABC9UeJy/0d3p9f78+fHl2My7oIVpPxAHQX689P/go1kSSPC3SwIdjeteAfvJNxum/X966tPIsa7C16Ut1s+QZj0TaPfknVgVqPOhQw29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",
                primary_color="#0076BE",
                text_color="#FFFFFF",
                banner=True,
                notification_title="Heads up, you’ve been redirected to Browser Isolation!",
                notification_text="The website you were trying to access is now rendered in a fully isolated environment to protect you from malicious content.",
            )
            if created_banner and "id" in created_banner:
                banner_id = created_banner.id
                assert banner_id is not None  # Asserting that a non-null ID is returned
            else:
                errors.append("Banner creation failed or returned unexpected data")

            # Assuming banner_id is valid and the banner was created successfully
            if banner_id:
                # Update the isolation banner
                updated_name = banner_name + " Updated"
                client.isolation.update_banner(banner_id, name=updated_name)
                updated_banner = client.isolation.get_banner(banner_id)
                assert updated_banner.name == updated_name  # Verify update by checking the updated attribute

                # List isolation banners and ensure the updated banner is in the list
                banners_list = client.isolation.list_banners()
                assert any(banner.id == banner_id for banner in banners_list)

        except Exception as exc:
            errors.append(exc)

        finally:
            # Attempt to delete the isolation banner if it was created
            if banner_id:
                try:
                    # Delete the isolation banner
                    delete_response_code = client.isolation.delete_banner(banner_id)
                    assert str(delete_response_code) == "200"  # Adjust to expect '200' as per API behavior
                except Exception as exc:
                    errors.append(exc)

        # Assert that no errors occurred during the test
        assert len(errors) == 0, f"Errors occurred during the isolation banner lifecycle test: {errors}"
