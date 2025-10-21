#!/usr/bin/env python

# Copyright 2025 Google LLC.
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

from typing import Any
import proto
import logging
import json
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v21.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)

from google.ads.googleads.util import get_nested_attr
import google.auth
from google.oauth2 import service_account
from ads_mcp.mcp_header_interceptor import MCPHeaderInterceptor
import os

GAQL_FILEPATH = "ads_mcp/gaql_resources.txt"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Read-only scope for Analytics Admin API and Analytics Data API.
_READ_ONLY_ADS_SCOPE = "https://www.googleapis.com/auth/adwords"


def _get_subject() -> str:
    """Returns the subject for impersonation from the environment variable GOOGLE_ADS_SUBJECT."""
    return os.environ.get("GOOGLE_ADS_SUBJECT")


def _create_credentials() -> google.auth.credentials.Credentials:
    """Returns credentials with optional subject delegation support."""
    subject = _get_subject()
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    
    if subject and credentials_path:
        logger.info(f"Subject specified: {subject}")
        
        try:
            # Check if it's a service account file
            with open(credentials_path, 'r') as f:
                creds_info = json.load(f)
            
            if creds_info.get('type') == 'service_account':
                logger.info("Using service account with subject delegation")
                # Service account credentials with subject delegation
                credentials = service_account.Credentials.from_service_account_file(
                    credentials_path,
                    scopes=[_READ_ONLY_ADS_SCOPE]
                )
                # Apply subject delegation
                delegated_credentials = credentials.with_subject(subject)
                logger.info(f"Successfully applied subject delegation for: {subject}")
                return delegated_credentials
            else:
                # OAuth credentials - subject parameter is logged but ignored
                logger.info(f"Subject '{subject}' specified but using OAuth credentials. Subject delegation requires service account credentials. Proceeding with OAuth.")
                
        except Exception as e:
            logger.warning(f"Error processing credentials file for subject delegation: {e}. Falling back to default authentication.")
    
    # Default behavior: no subject or fallback
    if subject:
        logger.info("Using default authentication (subject parameter ignored)")
    else:
        logger.info("Using default authentication (no subject specified)")
    
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


def _get_login_customer_id() -> str:
    """Returns login customer id, if set, from the environment variable GOOGLE_ADS_LOGIN_CUSTOMER_ID."""
    return os.environ.get("GOOGLE_ADS_LOGIN_CUSTOMER_ID")


def _get_googleads_client() -> GoogleAdsClient:
    # Use this line if you have a google-ads.yaml file
    # client = GoogleAdsClient.load_from_storage()
    client = GoogleAdsClient(
        credentials=_create_credentials(),
        developer_token=_get_developer_token(),
        login_customer_id=_get_login_customer_id()
    )

    return client


_googleads_client = _get_googleads_client()


def get_googleads_service(serviceName: str) -> GoogleAdsServiceClient:
    return _googleads_client.get_service(
        serviceName, interceptors=[MCPHeaderInterceptor()]
    )


def get_googleads_type(typeName: str):
    return _googleads_client.get_type(typeName)


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