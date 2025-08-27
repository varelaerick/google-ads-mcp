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

from google.ads.googleads.v21.services.types.customer_service import (
    ListAccessibleCustomersResponse,
)



@mcp.tool()
def list_accessible_customers() -> List[str]:
    ga_service = utils.googleads_client.get_service("CustomerService")
    accessible_customers: ListAccessibleCustomersResponse = (
        ga_service.list_accessible_customers()
    )
    
    return  accessible_customers.resource_names    

