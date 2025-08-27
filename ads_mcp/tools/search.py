# Copyright 2025 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, List
from ads_mcp.coordinator import mcp
import ads_mcp.utils as utils
from mcp.server.fastmcp import Context

def search(
    customer_id: str,
    fields: str,
    resource: str,
    condition: str = None,
    ordering:str = None,
    limit:int|str = None
    ) -> List[Dict[str, Any]] :
    """Fetches data from the Google Ads API using the search method
    
    Args:
        customer_id: The id of the customer
        fields: The fields to fetch, separated by commas
        resource: The resource to return fields from
        condiiton: How the data is filtered
        ordering: How the data is ordered
        limit: The maximum number of rows to return

    """

    ga_service = utils.googleads_client.get_service("GoogleAdsService")

    query = f"SELECT {fields} FROM {resource}"
    
    if condition:
        query += f" WHERE {condition}"
        
    if ordering:
        query += f" ORDER BY {ordering}"

    if limit:
        query += f" LIMIT {limit}"        

    utils.logger.info(f"ads_mcp.search query {query}")


    query_result = ga_service.search(customer_id=customer_id, query=query)
    
    final_output:List = []    
    for row in query_result.results:          
        final_output.append(utils.format_output_row(row, query_result.field_mask.paths))          
    return final_output



def search_tool_description() -> str:
    """Returns the description for the `search` tool."""
    try:
        with open(utils.GAQL_FILEPATH, 'r') as file:
            file_content = file.read()            
    except FileNotFoundError:
        print("Error: The specified file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return f"""
    Fetches data from the Google Ads API using the search method
    
    Args:
        customer_id: The id of the customer, this must not be empty
        fields: The fields to fetch, separated by commas, the SelectClause in the grammar, this must not be empty
        resource: The resource to return fields from, the FromClause in the gammar, this must not be empty
        condiiton: How the data is filtered, the WhereClause in the grammar, this must not be empty
        ordering: How the data is ordered, the OrderByClause in the grammar
        limit: The maximum number of rows to return

    ### Hints
        Language Grammar can be found at https://developers.google.com/google-ads/api/docs/query/grammar
        All resources and descriptions are found at https://developers.google.com/google-ads/api/fields/v21/overview
        
        For Conversion issues try looking in offline_conversion_upload_conversion_action_summary

    ## Hints for Dates
        All dates should be in the form YYYY-MM-DD and must include the dashes (-)
        Date litorals from the Grammar must NEVER be expanded or joined, only used exactly as listed
        Date ranges should be finite and must include a start and end date

    ### Hints for limits
        Requests to resource change_event must specify a LIMIT of less than or equal to 10000

    ### Hints for all fields
        What follows is a table of resources and their selectable fields (fields), filterable fields (used in the condition) and sortable fields (use in the ordering)
        Fields are comma seperated, the whole field must be used, wildcards and partial fields are not allowed
        All fields must come from this table and be prefixed with the resource being searched
        {file_content}
    """


# The `search` tool requires a more complex description that's generated at
# runtime. Uses the `add_tool` method instead of an annnotation since `add_tool`
# provides the flexibility needed to generate the description while also
# including the `search` method's docstring.
mcp.add_tool(
    search,
    title="Fetches data from the Google Ads API using the search method",
    description=search_tool_description()
)