# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup

def get_version():
    # Define the path to the __init__.py file
    init_path = os.path.join(os.path.dirname(__file__), "zscaler", "__init__.py")
    # Use a regular expression to find the version number
    version_pattern = re.compile(r"^__version__ = ['\"]([^'\"]*)['\"]")
    with open(init_path, "rt") as version_file:
        for line in version_file:
            match = version_pattern.search(line)
            if match:
                return match.group(1)
    raise RuntimeError("Unable to find version string.")

packages = [
    "zscaler",
    "zscaler.cache",
    "zscaler.errors",
    "zscaler.exceptions",
    "zscaler.ratelimiter",
    "zscaler.zia",
    "zscaler.zpa",
]

package_data = {"": ["*"]}

install_requires = [
    "aenum",
    "arrow",
    "certifi",
    "charset-normalizer",
    "flatdict",
    "idna",
    "pycryptodomex",
    "pydash",
    "python-box>=7.0,<8.0",
    "python-dateutil",
    "pytz",
    "pyyaml",
    "requests",
    "responses",
    "restfly==1.4.7",
    "six",
    "urllib3>=1.25.4,<1.27",
    "xmltodict",
    "yarl",
]

setup_kwargs = {
    "name": "zscaler-sdk-python",
    "version": get_version(),
    "description": "Official Python SDK for the Zscaler Products",
    "long_description": "# Official Python SDK for the Zscaler Products\n\n[![CI/CD](https://github.com/zscaler/zscaler-sdk-python/actions/workflows/ci.yml/badge.svg)](https://github.com/zscaler/zscaler-sdk-python/actions/workflows/ci.yml)\n[![Documentation Status](https://readthedocs.org/projects/zscaler-sdk-python/badge/?version=latest)](https://zscaler-sdk-python.readthedocs.io/en/latest/?badge=latest)\n[![License](https://img.shields.io/github/license/zscaler/zscaler-sdk-python.svg)](https://github.com/zscaler/zscaler-sdk-python)\n[![Latest version released on PyPi](https://img.shields.io/pypi/v/zscaler-sdk-python.svg)](https://pypi.org/project/zscaler-sdk-python)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/zscaler-sdk-python.svg)](https://pypi.python.org/pypi/zscaler-sdk-python/)\n[![GitHub Release](https://img.shields.io/github/release/zscaler/zscaler-sdk-python.svg)](https://github.com/zscaler/zscaler-sdk-python/releases/)\n[![Zscaler Community](https://img.shields.io/badge/zscaler-community-blue)](https://community.zscaler.com/)\n\n## Support Disclaimer\n\n-> **Disclaimer:** Please refer to our [General Support Statement](docs/guides/support.md) before proceeding with the use of this provider. You can also refer to our [troubleshooting guide](docs/guides/troubleshooting.md) for guidance on typical problems.\n\n## Zscaler Python SDK Overview\n\nThis repository contains the Zscaler SDK for Python. This SDK can be used to interact with several Zscaler services such as:\n\n* Zscaler Private Access (ZPA)\n* Zscaler Internet Access (ZIA)\n* [Documentation](http://zscaler-sdk-python.readthedocs.io)\n\n-----\n\nEach Zscaler product has separate developer documentation and authentication methods. This SDK aims to simplify\nsoftware development using the Zscaler API for both customers and partners.\n\n- [Release Status](#release-status)\n- [Need help?](#need-help)\n- [Getting Started](#getting-started)\n- [Pagination](#pagination)\n- [Logging](#logging)\n- [Rate Limiting](#rate-limiting)\n- [Environment variables](#environment-variables)\n- [Building the SDK](#building-the-sdk)\n- [Contributing](#contributing)\n\n> Requires Python version 3.8.0 or higher.\n\n## Need help?\n\nIf you run into problems using the SDK, you can:\n\n- Ask questions on the [Zenith Community][zenith]\n- Post [issues on GitHub][github-issues] (for code errors)\n- Support [customer support portal][zscaler-support]\n\n## Getting started\n\nTo install the Zscaler Python SDK in your project:\n\n```sh\npip install zscaler-sdk-python\n```\n\n## Usage\n\nBefore you can interact with any of the Zscaler APIs, you need to generate API keys or retrieve tenancy information for each product that you are interfacing with. Once you have the requirements and you have installed Zscaler SDK Python, you're ready to go.\n\n### Quick ZIA Example\n\n```python\nfrom zscaler import ZIAClientHelper\nfrom pprint import pprint\n\nzia = ZIAClientHelper(username='ZIA_USERNAME', password='ZIA_PASSWORD', api_key='ZIA_API_KEY', cloud='ZIA_CLOUD')\nfor user in zia.users.list_users():\n    pprint(user)\n```\n\n### Quick ZPA Example\n\n```python\nfrom zscaler import ZPAClientHelper\nfrom pprint import pprint\n\nzpa = ZPAClientHelper(client_id='ZPA_CLIENT_ID', client_secret='ZPA_CLIENT_SECRET', customer_id='ZPA_CUSTOMER_ID', cloud='ZPA_CLOUD')\nfor app_segment in zpa.app_segments.list_segments():\n    pprint(app_segment)\n```\n\n~> **NOTE** The `ZPA_CLOUD` environment variable is optional and only required if your project needs to interact with any other ZPA cloud other than production cloud. In this case, use the `ZPA_CLOUD` environment variable followed by the name of the corresponding environment: `ZPA_CLOUD=BETA`, `ZPA_CLOUD=ZPATWO`, `ZPA_CLOUD=GOV`, `ZPA_CLOUD=GOVUS`, `ZPA_CLOUD=PREVIEW`, `ZPA_CLOUD=DEV`.\n\n## Pagination\n\nThis SDK provides methods that retrieve a list of resources from the API, which return paginated results due to the volume of data. Each method capable of returning paginated data is prefixed as `list_` and handles the pagination internally by providing an easy interface to iterate through pages. The user does not need to manually fetch each page; instead, they can process items as they iterate through them.\n\n### Example of Iterating Over Paginated Results\n\nThe following example shows how you can list ZPA items using this SDK, processing each item one at a time. This pattern is useful for operations that need to handle large datasets efficiently.\n\n```python\nfrom zscaler import ZPAClientHelper\nfrom pprint import pprint\n\n# Initialize the client\nzpa = ZPAClientHelper(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, customer_id=CUSTOMER_ID, cloud=CLOUD)\n\nfor apps in zpa.app_segments.list_segments():\n    pprint(apps)\n```\n\n### Customizing Pagination Parameters\n\nWhile pagination is handled automatically, you can also customize pagination behavior by specifying parameters such as data_per_page and max_items. These parameters give you control over the volume of data fetched per request and the total amount of data to process. This is useful for limiting the scope of data fetched\n\n* `max_pages`: controls the number of items fetched per API call (per page).\n* `max_items`: controls the total number of items to retrieve across all pages. \n\n```python\nfrom zscaler import ZPAClientHelper\nfrom pprint import pprint\n\n# Initialize the client\nzpa = ZPAClientHelper(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, customer_id=CUSTOMER_ID, cloud=CLOUD)\n\npagination_params = {\n    'max_pages': 1,\n    'max_items': 5\n}\n\n# Fetch data using custom pagination settings\nsegments = zpa.app_segments.list_segments(**pagination_params)\nfor segment in segments:\n    pprint(segment)\n```\n\n### Efficient Pagination Handling\n\nFor more details on each pagination parameter see:\n[ZPA Pagination Parameters](zscaler/zpa/README.md)\n[ZIA Pagination Parameters](zscaler/zia/README.md)\n\n## Logging\n\nThe Zscaler SDK Python, provides robust logging for debug purposes.\nLogs are disabled by default and should be enabled explicitly via custom environment variable:\n\n* `ZSCALER_SDK_LOG` - Turn on logging\n* `ZSCALER_SDK_VERBOSE` - Turn on logging in verbose mode\n\n```sh\nexport ZSCALER_SDK_LOG=true\nexport ZSCALER_SDK_VERBOSE=true\n```\n\n**NOTE**: DO NOT SET DEBUG LEVEL IN PRODUCTION!\n\nYou should now see logs in your console. Notice that API tokens are **NOT** logged to the console; however, we still advise to use caution and never use `DEBUG` level logging in production.\n\nWhat it being logged? `requests`, `responses`,  `http errors`, `caching responses`.\n\n### Environment variables\n\nEach one of the configuration values above can be turned into an environment variable name with the `_` (underscore) character and UPPERCASE characters. The following are accepted:\n\n- `ZSCALER_CLIENT_CACHE_ENABLED` - Enable or disable the caching mechanism within the clien\n- `ZSCALER_CLIENT_CACHE_DEFAULT_TTL` - Duration (in seconds) that cached data remains valid. By default data is cached in memory for `3600` seconds.\n- `ZSCALER_CLIENT_CACHE_DEFAULT_TTI` - This environment variable sets the maximum amount of time (in seconds) that cached data can remain in the cache without being accessed. If the cached data is not accessed within this timeframe, it is removed from the cache, regardless of its TTL. The default TTI is `1800` seconds (`30 minutes`) \n- `ZSCALER_SDK_LOG` - Turn on logging\n- `ZSCALER_SDK_VERBOSE` - Turn on logging in verbose mode\n\n## Rate Limiting\n\nZscaler provides unique rate limiting numbers for each individual product. Regardless of the product, a 429 response will be returned if too many requests are made within a given time. \nPlease see:\n* [ZPA Rate Limiting][rate-limiting-zpa] for rate limiting requirements.\n* [ZIA Rate Limiting][rate-limiting-zia] for a complete list of which endpoints are rate limited.\n\nWhen a 429 error is received, the `Retry-After` header will tell you the time at which you can retry. This section discusses the method for handling rate limiting with this SDK.\n\n### Built-In Retry\n\nThis SDK uses the built-in retry strategy to automatically retry on 429 errors. The default Maximum Retry Attempts for both ZIA and ZPA explicitly limits the number of retry attempts to a maximum of `5`.\n\nRetry Conditions: The client for both ZPA and ZIA retries a request under the following conditions:\n\n* HTTP status code 429 (Too Many Requests): This indicates that the rate limit has been exceeded. The client waits for a duration specified by the `Retry-After` header, if present, or a default of `2 ` seconds, before retrying.\n\n* Exceptions during request execution: Any requests.RequestException encountered during the request triggers a retry, except on the last attempt, where the exception is raised.\n\n## Building the SDK\n\nIn most cases, you won't need to build the SDK from source. If you want to build it yourself, you'll need these prerequisites:\n\n- Clone the repo\n- Run `make build:dist` from the root of the project (assuming Python is installed)\n- Ensure tests run succesfully. \n- Install `tox` if not installed already using: `pip install tox`. \n- Run tests using `tox` in the root directory of the project.\n\n## Contributing\n\nAt this moment we are not accepting contributions, but we welcome suggestions on how to improve this SDK or feature requests, which can then be added in  future releases.\n\n[zenith]: https://community.zscaler.com/\n[zscaler-support]: https://help.zscaler.com/contact-support\n[github-issues]: https://github.com/zscaler/zscaler-sdk-python/issues\n[rate-limiting-zpa]: https://help.zscaler.com/zpa/understanding-rate-limiting\n[rate-limiting-zia]: https://help.zscaler.com/zia/understanding-rate-limiting\n\nContributors\n------------\n\n- William Guilherme - [willguibr](https://github.com/willguibr)\n- Eddie Parra - [eparra](https://github.com/eparra)\n- Paul Abbot - [abbottp](https://github.com/abbottp)\n\n## License\nMIT License\n\n=======\n\nCopyright (c) 2023 [Zscaler](https://github.com/zscaler)\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the \"Software\"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n",
    "author": "Zscaler Technology Alliances",
    "author_email": "devrel@zscaler.com",
    "maintainer": "None",
    "maintainer_email": "None",
    "url": "https://github.com/zscaler/zscaler-sdk-python",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.8,<4.0",
}


setup(**setup_kwargs)
