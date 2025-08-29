# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools for generating file containing a list of resources and their fields."""

import utils, json, sys
from google.ads.googleads.v21.services.types.google_ads_field_service import (
    SearchGoogleAdsFieldsRequest,
    SearchGoogleAdsFieldsResponse,
)

from google.ads.googleads.v21.resources.types.google_ads_field import (
    GoogleAdsField,
)


def get_data_for_resource(resource_name):
    """For a given resource_name, return selectable, filterable and sortable fields"""
    ga_service = utils.googleads_client.get_service("GoogleAdsFieldService")

    request: SearchGoogleAdsFieldsRequest = utils.googleads_client.get_type(
        "SearchGoogleAdsFieldsRequest"
    )

    query = f"SELECT name, selectable, filterable, sortable WHERE name like '{resource_name}.%'"

    request.query = query

    response: SearchGoogleAdsFieldsResponse = (
        ga_service.search_google_ads_fields(request=request)
    )

    if response.total_results_count == 0:
        raise ValueError(
            "No GoogleAdsFields found with a name that begins with "
            f"'{resource_name}'."
        )

    selectable: list = []
    filterable: list = []
    sortable: list = []

    googleads_field: GoogleAdsField
    for googleads_field in response:
        if googleads_field.selectable:
            selectable.append(googleads_field.name)
        if googleads_field.filterable:
            filterable.append(googleads_field.name)
        if googleads_field.sortable:
            sortable.append(googleads_field.name)
        # todo if googleads_field.selectable_with:

    output = f"""{{'resource:': '{resource_name}', 'selectable': ['{ "','".join(selectable) }'], 'filterable': ['{ "','".join(filterable) }'], 'sortable': ['{ "','".join(sortable) }']}},"""

    return output


def update_gaql_resource_file():
    """Find all resources, geneate field data for each and save to a file"""
    ga_service = utils.googleads_client.get_service("GoogleAdsFieldService")

    request: SearchGoogleAdsFieldsRequest = utils.googleads_client.get_type(
        "SearchGoogleAdsFieldsRequest"
    )

    query = f"SELECT name WHERE category = 'RESOURCE'"

    request.query = query

    response: SearchGoogleAdsFieldsResponse = (
        ga_service.search_google_ads_fields(request=request)
    )

    if response.total_results_count == 0:
        raise ValueError("No resources found")

    with open(utils.GAQL_FILEPATH, "w") as file:
        for googleads_field in response:
            json.dump(
                get_data_for_resource(googleads_field.name), file, indent=4
            )
            file.write("\n")


if __name__ == "__main__":
    update_gaql_resource_file()
