import utils
import sys
from google.ads.googleads.v21.services.types.google_ads_field_service import (
    SearchGoogleAdsFieldsRequest,
    SearchGoogleAdsFieldsResponse
)

from google.ads.googleads.v21.resources.types.google_ads_field import (
    GoogleAdsField,
)

def get_data_for_resource(resource_name):
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
        print(
            "No GoogleAdsFields found with a name that begins with "
            f"'{resource_name}'."
        )
        sys.exit(0)

    selectable:list = []
    filterable:list = []
    sortable:list = []
    
    googleads_field: GoogleAdsField
    for googleads_field in response:
        if googleads_field.selectable :
            selectable.append(googleads_field.name)
        if googleads_field.filterable :
            filterable.append(googleads_field.name)
        if googleads_field.sortable :
            sortable.append(googleads_field.name)  
        #todo if googleads_field.selectable_with:

    output = f"""{{'resource:': '{resource_name}', 'selectable': ['{ "','".join(selectable) }'],'filterable': ['{ "','".join(filterable) }'], 'sortable': ['{ "','".join(sortable) }']}}"""

    return output

def update_gaql_resource_file():
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
        print("No resources found")
        sys.exit(1)

    with open(utils.GAQL_FILEPATH, "w") as file:
        file.write("[")
        googleads_field: GoogleAdsField
        for googleads_field in response:
            file.write(get_data_for_resource(googleads_field.name))
        file.write("]")


if __name__ == "__main__":
    update_gaql_resource_file()    