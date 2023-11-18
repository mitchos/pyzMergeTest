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
from requests import Response
from zscaler.utils import snake_to_camel
from zscaler.zia import ZIAClient
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FirewallPolicyAPI:
    # Firewall filter rule keys that only require an ID to be provided.
    _key_id_list = [
        "app_services",
        "app_service_groups",
        "departments",
        "dest_ip_groups",
        "devices",
        "device_groups",
        "groups",
        "labels",
        "locations",
        "location_groups",
        "nw_application_groups",
        "nw_services",
        "nw_service_groups",
        "src_ip_groups",
        "time_windows",
        "users",
    ]

    def __init__(self, client: ZIAClient):
        self.rest = client

    def list_rules(self) -> BoxList:
        """
        Returns a list of all firewall filter rules.

        Returns:
            :obj:`BoxList`: The list of firewall filter rules

        Examples:
            >>> for rule in zia.firewall.list_rules():
            ...    pprint(rule)

        """
        response = self.rest.get("/firewallFilteringRules")
        if isinstance(response, Response):
            return None
        return response

    def get_rule(self, rule_id: str) -> Box:
        """
        Returns information for the specified firewall filter rule.

        Args:
            rule_id (str): The unique identifier for the firewall filter rule.

        Returns:
            :obj:`Box`: The resource record for the firewall filter rule.

        Examples:
            >>> pprint(zia.firewall.get_rule('431233'))

        """
        return self.rest.get(f"firewallFilteringRules/{rule_id}")

    def add_rule(self, name: str, action: str, **kwargs) -> Box:
        """
        Adds a new firewall filter rule.

        Args:
            name (str): The name of the filter rule. 31 char limit.
            action (str): The action for the filter rule.

            device_trust_levels (list): List of device trust levels for which the rule must be applied. Accepted values are:
                `ANY`, `UNKNOWN_DEVICETRUSTLEVEL`, `LOW_TRUST`, `MEDIUM_TRUST`, and `HIGH_TRUST`
            **kwargs: Optional keyword args

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule.
            state (str): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            description (str): Additional information about the rule
            src_ips (list): The source IPs that this rule applies to. Individual IP addresses or CIDR ranges accepted.
            dest_addresses (list): The destination IP addresses that this rule applies to. Individual IP addresses or
            CIDR ranges accepted.
            dest_ip_categories (list): The IP address categories that this rule applies to.
            dest_countries (list): The destination countries that this rule applies to.
            enable_full_logging (bool): Enables full logging if True.
            nw_applications (list): The network service applications that this rule applies to.
            app_services (list): The IDs for the application services that this rule applies to.
            app_service_groups (list): The IDs for the application service groups that this rule applies to.
            departments (list): The IDs for the departments that this rule applies to.
            dest_ip_groups (list): The IDs for the destination IP groups that this rule applies to.
            devices (list): The IDs for the devices that are managed using Zscaler Client Connector that this rule applies to.
            device_groups (list): The IDs for the device groups that are managed using Zscaler Client Connector that this rule applies to.
            groups (list): The IDs for the groups that this rule applies to.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            nw_application_groups (list): The IDs for the network application groups that this rule applies to.
            nw_services (list): The IDs for the network services that this rule applies to.
            nw_service_groups (list): The IDs for the network service groups that this rule applies to.
            time_windows (list): The IDs for the time windows that this rule applies to.
            users (list): The IDs for the users that this rule applies to.

        Returns:
            :obj:`Box`: The new firewall filter rule resource record.

        Examples:
            Add a rule to allow all traffic to Google DNS (admin ranking is enabled):

            >>> zia.firewall.add_rule(rank='7',
            ...    dest_addresses=['8.8.8.8', '8.8.4.4'],
            ...    name='ALLOW_ANY_TO_GOOG-DNS',
            ...    action='ALLOW'
            ...    description='TT#1965432122')

            Add a rule to block all traffic to Quad9 DNS for all users in Finance Group and send an ICMP error:

            >>> zia.firewall.add_rule(rank='7',
            ...    dest_addresses=['9.9.9.9'],
            ...    name='BLOCK_GROUP-FIN_TO_Q9-DNS',
            ...    action='BLOCK_ICMP'
            ...    groups=['95016183']
            ...    description='TT#1965432122')

        """
        payload = {
            "name": name,
            "action": action,
            "order": kwargs.pop("order", len(self.list_rules())),
        }
        # Convert rule_state to API format if present
        if 'rule_state' in kwargs:
            kwargs['state'] = "ENABLED" if kwargs.pop('rule_state') else "DISABLED"

        # Add optional parameters to payload
        for key, value in kwargs.items():
            if key in self._key_id_list:
                payload[snake_to_camel(key)] = []
                for item in value:
                    payload[snake_to_camel(key)].append({"id": item})
            else:
                payload[snake_to_camel(key)] = value

        response = self.rest.post("firewallFilteringRules", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_rule(self, rule_id: str, **kwargs) -> Box:
        """
        Updates an existing firewall filter rule.

        Args:
            rule_id (str): The unique ID for the rule that is being updated.
            **kwargs: Optional keyword args.

        Keyword Args:
            order (str): The order of the rule, defaults to adding rule to bottom of list.
            rank (str): The admin rank of the rule.
            state (str): The rule state. Accepted values are 'ENABLED' or 'DISABLED'.
            description (str): Additional information about the rule
            src_ips (list): The source IPs that this rule applies to. Individual IP addresses or CIDR ranges accepted.
            dest_addresses (list): The destination IP addresses that this rule applies to. Individual IP addresses or
            CIDR ranges accepted.
            dest_ip_categories (list): The IP address categories that this rule applies to.
            dest_countries (list): The destination countries that this rule applies to.
            enable_full_logging (bool): Enables full logging if True.
            nw_applications (list): The network service applications that this rule applies to.
            app_services (list): The IDs for the application services that this rule applies to.
            app_service_groups (list): The IDs for the application service groups that this rule applies to.
            departments (list): The IDs for the departments that this rule applies to.
            dest_ip_groups (list): The IDs for the destination IP groups that this rule applies to.
            groups (list): The IDs for the groups that this rule applies to.
            labels (list): The IDs for the labels that this rule applies to.
            locations (list): The IDs for the locations that this rule applies to.
            location_groups (list): The IDs for the location groups that this rule applies to.
            nw_application_groups (list): The IDs for the network application groups that this rule applies to.
            nw_services (list): The IDs for the network services that this rule applies to.
            nw_service_groups (list): The IDs for the network service groups that this rule applies to.
            time_windows (list): The IDs for the time windows that this rule applies to.
            users (list): The IDs for the users that this rule applies to.

        Returns:
            :obj:`Box`: The updated firewall filter rule resource record.

        Examples:
            Update the destination IP addresses for a rule:

            >>> zia.firewall.update_rule('976598',
            ...    dest_addresses=['1.1.1.1'],
            ...    description="TT#1965232865")

            Update a rule to enable full logging:

            >>> zia.firewall.update_rule('976597',
            ...    enable_full_logging=True,
            ...    description="TT#1965232866")

        """

        # Fetch existing data - consider whether all fields should be merged or only specific ones
        existing_data = self.get_rule(rule_id)

        # Convert rule_state to API format if present in kwargs
        if 'rule_state' in kwargs:
            kwargs['state'] = "ENABLED" if kwargs.pop('rule_state') else "DISABLED"

        # Merge existing data with new data from kwargs
        payload = {snake_to_camel(k): v for k, v in existing_data.items()}
        for key, value in kwargs.items():
            # Override the existing data with new data
            payload[snake_to_camel(key)] = value

        response = self.rest.put(f"firewallFilteringRules/{rule_id}", json=payload)
        if isinstance(response, Response) and not response.ok:
            # Handle error response
            raise Exception(f"API call failed with status {response.status_code}: {response.json()}")

        # Return the updated object
        return self.get_rule(rule_id)

    def delete_rule(self, rule_id: str) -> int:
        """
        Deletes the specified firewall filter rule.

        Args:
            rule_id (str): The unique identifier for the firewall filter rule.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.firewall.delete_rule('278454')

        """
        response = self.rest.delete(f"firewallFilteringRules/{rule_id}")
        return response.status_code if isinstance(response, Response) else None

    def list_ip_destination_groups(self, exclude_type: str = None) -> BoxList:
        """
        Returns a list of IP Destination Groups.

        Args:
            exclude_type (str): Exclude all groups that match the specified IP destination group's type.
                Accepted values are: `DSTN_IP`, `DSTN_FQDN`, `DSTN_DOMAIN` and `DSTN_OTHER`.

        Returns:
            :obj:`BoxList`: List of IP Destination Group records.

        Examples:
            >>> for group in zia.firewall.list_ip_destination_groups():
            ...    pprint(group)

        """

        payload = {"excludeType": exclude_type}

        return self.rest.get("ipDestinationGroups", params=payload)

    def get_ip_destination_group(self, group_id: str) -> Box:
        """
        Returns information on the specified IP Destination Group.

        Args:
            group_id (str): The unique ID of the IP Destination Group.

        Returns:
            :obj:`Box`: The IP Destination Group resource record.

        Examples:
            >>> pprint(zia.firewall.get_ip_destination_group('287342'))

        """
        return self.rest.get(f"ipDestinationGroups/{group_id}")

    def delete_ip_destination_group(self, group_id: str) -> int:
        """
        Deletes the specified IP Destination Group.

        Args:
            group_id (str): The unique ID of the IP Destination Group.

        Returns:
            :obj:`int`: The status code of the operation.

        Examples:
            >>> zia.firewall.delete_ip_destination_group('287342')

        """
        return self.rest.delete(f"ipDestinationGroups/{group_id}").status_code

    def add_ip_destination_group(self, name: str, **kwargs) -> Box:
        """
        Adds a new IP Destination Group.

        Args:
            name (str): The name of the IP Destination Group.
            **kwargs: Optional keyword args.

        Keyword Args:
            type (str): Destination IP group type. Allowed values are DSTN_IP and DSTN_FQDN.
            addresses (list): Destination IP addresses or FQDNs within the group.
            description (str): Additional information about the destination IP group.
            ip_categories (list): Destination IP address URL categories.
            countries (list): Destination IP address counties.

        Returns:
            :obj:`Box`: The newly created IP Destination Group resource record.

        Examples:
            Add a Destination IP Group with IP addresses:

            >>> zia.firewall.add_ip_destination_group(name='Destination Group - IP',
            ...    addresses=['203.0.113.0/25', '203.0.113.131'],
            ...    type='DSTN_IP')

            Add a Destination IP Group with FQDN:

            >>> zia.firewall.add_ip_destination_group(name='Destination Group - FQDN',
            ...    description='Covers domains for Example Inc.',
            ...    addresses=['example.com', 'example.edu'],
            ...    type='DSTN_FQDN')

            Add a Destionation IP Group for the US:

            >>> zia.firewall.add_ip_destination_group(name='Destination Group - US',
            ...    description='Covers the US',
            ...    countries=['COUNTRY_US'])

        """

        payload = {"name": name}

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self.rest.post("ipDestinationGroups", json=payload)

    def update_ip_destination_group(self, group_id: str, **kwargs) -> Box:
        """
        Updates the specified IP Destination Group.

        Args:
            group_id (str): The unique ID of the IP Destination Group.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the IP Destination Group.
            addresses (list): Destination IP addresses or FQDNs within the group.
            description (str): Additional information about the IP Destination Group.
            ip_categories (list): Destination IP address URL categories.
            countries (list): Destination IP address countries.

        Returns:
            :obj:`Box`: The updated IP Destination Group resource record.

        Examples:
            Update the name of an IP Destination Group:

            >>> zia.firewall.update_ip_destination_group('9032667',
            ...    name="Updated IP Destination Group")

            Update the description and FQDNs for an IP Destination Group:

            >>> zia.firewall.update_ip_destination_group('9032668',
            ...    description="Tech News",
            ...    addresses=['arstechnica.com', 'slashdot.org'])

        """

        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_ip_destination_group(group_id).items()}

        # Update payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self.rest.put(f"ipDestinationGroups/{group_id}", json=payload)

    def list_ip_source_groups(self, search: str = None) -> BoxList:
        """
        Returns a list of IP Source Groups.

        Args:
            search (str): The search string used to match against a group's name or description attributes.

        Returns:
            :obj:`BoxList`: List of IP Source Group records.

        Examples:
            List all IP Source Groups:

            >>> for group in zia.firewall.list_ip_source_groups():
            ...    pprint(group)

            Use search parameter to find IP Source Groups with `fiji` in the name:

            >>> for group in zia.firewall.list_ip_source_groups('fiji'):
            ...    pprint(group)

        """

        payload = {"search": search}

        return self.rest.get("ipSourceGroups", json=payload)

    def get_ip_source_group(self, group_id: str) -> Box:
        """
        Returns information for the specified IP Source Group.

        Args:
            group_id (str): The unique ID of the IP Source Group.

        Returns:
            :obj:`Box`: The IP Source Group resource record.

        Examples:
            >>> pprint(zia.firewall.get_ip_source_group('762398')

        """
        return self.rest.get(f"ipSourceGroups/{group_id}")

    def delete_ip_source_group(self, group_id: str) -> int:
        """
        Deletes an IP Source Group.

        Args:
            group_id (str): The unique ID of the IP Source Group to be deleted.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.firewall.delete_ip_source_group('762398')

        """
        return self.rest.delete(f"ipSourceGroups/{group_id}").status_code

    def add_ip_source_group(self, name: str, ip_addresses: list, description: str = None) -> Box:
        """
        Adds a new IP Source Group.

        Args:
            name (str): The name of the IP Source Group.
            ip_addresses (str): The list of IP addresses for the IP Source Group.
            description (str): Additional information for the IP Source Group.

        Returns:
            :obj:`Box`: The new IP Source Group resource record.

        Examples:
            Add a new IP Source Group:

            >>> zia.firewall.add_ip_source_group(name='My IP Source Group',
            ...    ip_addresses=['198.51.100.0/24', '192.0.2.1'],
            ...    description='Contains the IP addresses for the local network.')

        """

        payload = {
            "name": name,
            "ipAddresses": ip_addresses,
            "description": description,
        }

        return self.rest.post("ipSourceGroups", json=payload)

    def update_ip_source_group(self, group_id: str, **kwargs) -> Box:
        """
        Update an IP Source Group.

        This method supports updating individual fields in the IP Source Group resource record.

        Args:
            group_id (str): The unique ID for the IP Source Group to update.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the IP Source Group.
            ip_addresses (list): The list of IP addresses for the IP Source Group.
            description (str): Additional information for the IP Source Group.

        Returns:
            :obj:`Box`: The updated IP Source Group resource record.

        Examples:
            Update the name of an IP Source Group:

            >>> zia.firewall.update_ip_source_group('9032674',
            ...    name='Updated Name')

            Update the description and IP addresses of an IP Source Group:

            >>> zia.firewall.update_ip_source_group('9032674',
            ...    description='Local subnets, updated on 3 JUL 21'
            ...    ip_addresses=['192.0.2.0/29', '192.0.2.8/29', '192.0.2.128/25'])

        """

        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_ip_source_group(group_id).items()}

        # Update payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        return self.rest.put(f"ipSourceGroups/{group_id}", json=payload)

    def list_network_app_groups(self, search: str = None) -> BoxList:
        """
        Returns a list of all Network Application Groups.

        Returns:
            :obj:`BoxList`: The list of Network Application Group resource records.

        Examples:
            >>> for group in zia.firewall.list_network_app_groups():
            ...    pprint(group)

        """
        payload = {"search": search}
        list = self.rest.get(path="/networkApplicationGroups", params=payload)
        if isinstance(list, Response):
            return None
        return list

        # payload = {"search": search}
        # return self.rest.get("networkApplicationGroups", params=payload)

    def get_network_app_group(self, group_id: str) -> Box:
        """
        Returns information for the specified Network Application Group.

        Args:
            group_id (str):
                The unique ID for the Network Application Group.

        Returns:
            :obj:`Box`: The Network Application Group resource record.
        """
        response = self.rest.get(f"networkApplicationGroups/{group_id}")

        # If 'response' is a Box, it should contain the response data directly
        # If 'response' is an HTTP response, it should have a 'status_code' attribute
        if hasattr(response, 'status_code'):
            # Check if the response is successful and the content is not empty
            if response.status_code == 200 and response.content:
                # Convert to Box for consistent return type
                return Box(response.json())
            else:
                # Handle non-200 responses
                response.raise_for_status()
        else:
            # Assume 'response' is a Box and contains the desired data
            if 'ok' in response and response.ok:
                # 'response' is a Box with the expected data
                return response
            else:
                # Handle cases where the response Box does not contain the expected data
                # For example, you might want to check for an 'error' or 'message' field
                # and raise an exception or handle the situation as needed
                # Example: raise ValueError("Failed to retrieve the network application group.")
                return Box()  # An empty Box indicates no data was found or an error occurred.


    def delete_network_app_group(self, group_id: str) -> int:
        """
        Deletes the specified Network Application Group.

        Args:
            group_id (str): The unique identifier for the Network Application Group.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zia.firewall.delete_network_app_group('762398')

        """
        return self.rest.delete(f"networkApplicationGroups/{group_id}").status_code


    def add_network_app_group(self, name: str, network_applications: list, description: str = None) -> Box:
        """
        Adds a new Network Application Group.

        Args:
            name (str): The name of the Network Application Group.
            description (str): Additional information about the Network Application Group.
            network_applications (list): A list of Application IDs to add to the group.

        Returns:
            :obj:`Box`: The newly created Network Application Group resource record.

        Examples:
            Add a new Network Application Group:

            >>> zia.firewall.add_network_app_group(name='New Network Application Group',
            ...    network_applications=['SALESFORCE', 'GOOGLEANALYTICS', 'OFFICE365'],
            ...    description='Additional information about the Network Application Group.')

        """

        payload = {
            "name": name,
            "networkApplications": network_applications,
            "description": description,
        }

        response = self.rest.post("networkApplicationGroups", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

        # return self.rest.post("networkApplicationGroups", json=payload)

    def update_network_app_group(self, group_id: str, **kwargs) -> Box:
        """
        Update an Network Application Group.

        This method supports updating individual fields in the Network Application Group resource record.

        Args:
            group_id (str): The unique ID for the Network Application Group to update.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the Network Application Group.
            network_applications (list): The list of applications for the Network Application Group.
            description (str): Additional information for the Network Application Group.

        Returns:
            :obj:`Box`: The updated Network Application Group resource record.

        Examples:
            Update the name of an Network Application Group:

            >>> zia.firewall.update_network_app_group('9032674',
            ...    name='Updated Network Application Group Name')

            Update the description and applications for a Network Application Group:

            >>> zia.firewall.update_network_app_group('9032674',
            ...    description='Network Application Group, updated on May 27, 2023'
            ...    network_applications=['SALESFORCE', 'GOOGLEANALYTICS', 'OFFICE365'])

        """

        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_network_app_group(group_id).items()}

        # Update payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"networkApplicationGroups/{group_id}", json=payload).status_code

        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_network_app_group(group_id)


    def list_network_apps(self, search: str = None) -> BoxList:
        """
        Returns a list of all predefined Network Applications.

        Args:
            search (str): The search string used to match against a network application's description attribute.

        Returns:
            :obj:`BoxList`: The list of Network Application resource records.

        Examples:
            >>> for app in zia.firewall.list_network_apps():
            ...    pprint(app)

        """
        payload = {"search": search}
        return self.rest.get("networkApplications", params=payload)

    def get_network_app(self, app_id: str) -> Box:
        """
        Returns information for the specified Network Application.

        Args:
            app_id (str): The unique ID for the Network Application.

        Returns:
            :obj:`Box`: The Network Application resource record.

        Examples:
            >>> pprint(zia.firewall.get_network_app('762398'))

        """
        return self.rest.get(f"networkApplications/{app_id}")

    def list_network_svc_groups(self, search: str = None) -> BoxList:
        """
        Returns a list of Network Service Groups.

        Args:
            search (str):  The search string used to match against a group's name or description attributes.

        Returns:
            :obj:`BoxList`: List of Network Service Group resource records.

        Examples:
            >>> for group in zia.firewall.list_network_svc_groups():
            ...    pprint(group)

        """

        payload = {}
        if search:
            payload["search"] = search
        return self.rest.get("networkServiceGroups", params=payload)

    def get_network_svc_group(self, group_id: str) -> Box:
        """
        Returns information for the specified Network Service Group.

        Args:
            group_id (str): The unique ID for the Network Service Group.

        Returns:
            :obj:`Box`: The Network Service Group resource record.

        Examples:
            >>> pprint(zia.firewall.get_network_svc_group('762398'))

        """
        return self.rest.get(f"networkServiceGroups/{group_id}")

    def delete_network_svc_group(self, group_id: str) -> int:
        """
        Deletes the specified Network Service Group.

        Args:
            group_id (str): The unique identifier for the Network Service Group.

        Returns:
            :obj:`int`: The response code for the operation.

        Examples:
            >>> zia.firewall.delete_network_svc_group('762398')

        """
        return self.rest.delete(f"networkServiceGroups/{group_id}").status_code

    def add_network_svc_group(self, name: str, service_ids: list, description: str = None) -> Box:
        """
        Adds a new Network Service Group.

        Args:
            name (str): The name of the Network Service Group.
            service_ids (list): A list of Network Service IDs to add to the group.
            description (str): Additional information about the Network Service Group.

        Returns:
            :obj:`Box`: The newly created Network Service Group resource record.

        Examples:
            Add a new Network Service Group:

            >>> zia.firewall.add_network_svc_group(name='New Network Service Group',
            ...    service_ids=['159143', '159144', '159145'],
            ...    description='Group for the new Network Service.')

        """

        payload = {"name": name, "services": [], "description": description}

        for service_id in service_ids:
            payload["services"].append({"id": service_id})

        return self.rest.post("networkServiceGroups", json=payload)

    def update_network_svc_group(self, group_id: str, **kwargs) -> Box:
        """
        Update a Network Service Group.

        Args:
            group_id (str): The unique ID of the Network Service Group.
            **kwargs: Optional keyword args.

        Keyword Args:
            name (str): The name of the Network Service Group.
            service_ids (list): A list of Network Service IDs to add to the group.
            description (str): Additional information about the Network Service Group.

        Returns:
            :obj:`Box`: The updated Network Service Group resource record.

        Examples:
            Update the name Network Service Group:

            >>> zia.firewall.update_network_svc_group(name='Update Network Service Group',
            ...    service_ids=['159143', '159144', '159145'],
            ...    description='Group for the new Network Service.')

        """

        # Set payload to value of existing record
        payload = {snake_to_camel(k): v for k, v in self.get_network_svc_group(group_id).items()}

        # Update payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        # return self.rest.put(f"networkServiceGroups/{group_id}", json=payload)

        resp = self.rest.put(f"networkServiceGroups/{group_id}", json=payload).status_code

        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_network_svc_group(group_id)

    def list_network_services(self, search: str = None, protocol: str = None) -> BoxList:
        """
        Returns a list of all Network Services.

        The search parameters find matching values within the "name" or "description" attributes.

        Args:
            search (str): The search string used to match against a service's name or description attributes.
            protocol (str): Filter based on the network service protocol. Accepted values are `ICMP`, `TCP`, `UDP`,
                `GRE`, `ESP` and `OTHER`.

        Returns:
            :obj:`BoxList`: The list of Network Service resource records.

        Examples:
            >>> for service in zia.firewall.list_network_services():
            ...    pprint(service)

        """
        payload = {"search": search, "protocol": protocol}
        return self.rest.get("networkServices", params=payload)

    def get_network_service(self, service_id: str) -> Box:
        """
        Returns information for the specified Network Service.

        Args:
            service_id (str): The unique ID for the Network Service.

        Returns:
            :obj:`Box`: The Network Service resource record.

        Examples:
            >>> pprint(zia.firewall.get_network_service('762398'))

        """
        return self.rest.get(f"networkServices/{service_id}")

    def delete_network_service(self, service_id: str) -> int:
        """
        Deletes the specified Network Service.

        Args:
            service_id (str): The unique ID for the Network Service.

        Returns:
            :obj:`int`: The status code for the operation.

        Examples:
            >>> zia.firewall.delete_network_service('762398')

        """
        return self.rest.delete(f"networkServices/{service_id}").status_code

    def add_network_service(self, name: str, ports: list = None, **kwargs) -> Box:
        """
        Adds a new Network Service.

        Args:
            name: The name of the Network Service
            ports (list):
                A list of port protocol tuples. Tuples must follow the convention `src/dest`, `protocol`,
                `start port`, `end port`. If this is a single port and not a port range then `end port` can be omitted.
                E.g.

                .. code-block:: python

                    ('src', 'tcp', '49152', '65535'),
                    ('dest', 'tcp', '22),
                    ('dest', 'tcp', '9010', '9012'),
                    ('dest', 'udp', '9010', '9012')

            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information on the Network Service.

        Returns:
            :obj:`Box`: The newly created Network Service resource record.

        Examples:
            Add Network Service for Microsoft Exchange:

            >>> zia.firewall.add_network_service('MS LDAP',
            ...    description='Covers all ports used by MS LDAP',
            ...    ports=[
            ...        ('dest', 'tcp', '389'),
            ...        ('dest', 'udp', '389'),
            ...        ('dest', 'tcp', '636'),
            ...        ('dest', 'tcp', '3268', '3269')])

            Add Network Service designed to match inbound SSH traffic:

            >>> zia.firewall.add_network_service('Inbound SSH',
            ...    description='Inbound SSH',
            ...    ports=[
            ...        ('src', 'tcp', '22'),
            ...        ('dest', 'tcp', '1024', '65535')])

        """

        payload = {"name": name}

        # Convert tuple list to dict and add to payload
        if ports is not None:
            for items in ports:
                port_range = [{"start": items[2]}]
                if len(items) == 4:
                    port_range.append({"end": items[3]})
                payload.setdefault(f"{items[0]}{items[1].title()}Ports", []).extend(port_range)

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        response = self.rest.post("networkServices", json=payload)
        if isinstance(response, Response):
            # this is only true when the creation failed (status code is not 2xx)
            status_code = response.status_code
            # Handle error response
            raise Exception(f"API call failed with status {status_code}: {response.json()}")
        return response

    def update_network_service(self, service_id: str, ports: list = None, **kwargs) -> Box:
        """
        Updates the specified Network Service.

        If ports aren't provided then no changes will be made to the ports already defined. If ports are provided then
        the existing ports will be overwritten.

        Args:
            service_id (str): The unique ID for the Network Service.
            ports (list):
                A list of port protocol tuples. Tuples must follow the convention `src/dest`, `protocol`, `start port`,
                `end port`. If this is a single port and not a port range then `end port` can be omitted. E.g.

                .. code-block:: python

                    ('src', 'tcp', '49152', '65535'),
                    ('dest', 'tcp', '22),
                    ('dest', 'tcp', '9010', '9012'),
                    ('dest', 'udp', '9010', '9012')

            **kwargs: Optional keyword args.

        Keyword Args:
            description (str): Additional information on the Network Service.

        Returns:
            :obj:`Box`: The newly created Network Service resource record.

        Examples:
            Update the name and description for a Network Service:

            >>> zia.firewall.update_network_service('959093',
            ...    name='MS Exchange',
            ...    description='All ports related to the MS Exchange service.')

            Updates the ports for a Network Service, leaving other fields intact:

            >>> zia.firewall.add_network_service('959093',
            ...    ports=[
            ...        ('dest', 'tcp', '500', '510')])


        """
        payload = {snake_to_camel(k): v for k, v in self.get_network_service(service_id).items()}

        # Convert tuple list to dict and add to payload
        if ports is not None:
            # Clear existing ports and set new values
            for items in ports:
                port_key = f"{items[0]}{items[1].title()}Ports"
                payload[port_key] = []
                payload[port_key].append({"start": items[2]})
                if len(items) == 4:
                    payload[port_key].append({"end": items[3]})

        # Add optional parameters to payload
        for key, value in kwargs.items():
            payload[snake_to_camel(key)] = value

        resp = self.rest.put(f"networkServices/{service_id}", json=payload).status_code

        # Return the object if it was updated successfully
        if not isinstance(resp, Response):
            return self.get_network_service(service_id)

    def list_time_windows(self) -> Box:
        """
        Returns a list of time intervals used for by the Firewall policy or the URL Filtering policy.

        Args:
            id (int): The unique id for the Time Interval.
            name (str): The name of the Time Interval.

        Returns:
            :obj:`Box`: The ZIA Time Interval resource record.

        Examples:
            >>> pprint(zia.firewall.list_time_windows_lite)

        """
        response = self.rest.get("/timeWindows")
        if isinstance(response, Response):
            return None
        return response

    def list_time_windows_lite(self) -> Box:
        """
        Returns name and ID dictionary of time intervals used by the Firewall policy or the URL Filtering policy.

        Args:
            id (int): The unique id for the Time Interval.
            name (str): The name of the Time Interval.

        Returns:
            :obj:`Box`: The ZIA Time Interval resource record.

        Examples:
            >>> pprint(zia.firewall.list_time_windows_lite)

        """
        response = self.rest.get("/timeWindows/lite")
        if isinstance(response, Response):
            return None
        return response