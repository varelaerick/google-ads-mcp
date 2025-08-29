#!/usr/bin/env python

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

"""Common utilities used by the MCP server."""

from typing import Any, Dict
import proto
import logging
from google.ads.googleads.client import GoogleAdsClient
from google.protobuf.json_format import MessageToDict
from google.ads.googleads.v21.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)

from google.ads.googleads.util import get_nested_attr
import google.auth
import os

GAQL_FILEPATH = "ads_mcp/gaql_resources.txt"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Read-only scope for Analytics Admin API and Analytics Data API.
_READ_ONLY_ADS_SCOPE = "https://www.googleapis.com/auth/adwords"


def _create_credentials() -> google.auth.credentials.Credentials:
    """Returns Application Default Credentials with read-only scope."""
    (credentials, _) = google.auth.default(scopes=[_READ_ONLY_ADS_SCOPE])
    return credentials


def _get_developer_token() -> str:
    """Returns the developer token from the environment variable GOOGLE_ADS_DEVELOPER_TOKEN."""
    dev_token = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN")
    if dev_token is None:
        raise ValueError(
            "GOOGLE_ADS_DEVELOPER_TOKEN environment variable not set."
        )
    return dev_token


def get_googleads_client() -> GoogleAdsClient:
    # Use this line if you have a google-ads.yaml file
    # client = GoogleAdsClient.load_from_storage()
    client = GoogleAdsClient(
        credentials=_create_credentials(),
        developer_token=_get_developer_token(),
    )

    # add somethink to headers to record and add support for MCP efforts
    return client


googleads_client = get_googleads_client()


def format_output_value(value: Any) -> Any:
    if isinstance(value, proto.Enum):
        return value.name
    else:
        return value


def format_output_row(row: proto.Message, attributes):
    return {
        attr: format_output_value(get_nested_attr(row, attr))
        for attr in attributes
    }
