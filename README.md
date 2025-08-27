# Google Ads MCP Server (Experimental)

This repo contains the source code for running a local
[MCP](https://modelcontextprotocol.io) server that interacts with the
[Google Ads API](https://developers.google.com/google-ads/api).



## Tools

The server uses the
[Google Ads API](https://developers.google.com/google-ads/api/reference/rpc/v21/overview)
to provide several
[Tools](https://modelcontextprotocol.io/docs/concepts/tools) for use with LLMs.

### Tools available 

- `search`: Retrieves information about the Google Ads account.
- `list_accessible_customers`: Returns names of customers directly accessible
  by the user authenticating the call.

## Setup instructions

Setup involves the following steps:

1.  Configure Python.
1.  Configure Google Ads API Python client library.
1.  Configure Gemini.

### Configure Python

[Install pipx](https://pipx.pypa.io/stable/#install-pipx).

### Configure Google Ads API Python client library.

[Follow the instructions](https://developers.google.com/google-ads/api/docs/client-libs/python/)
to setup and configure the Google Ads API Python client library

If you have already done this and have a working google-ads.yaml , you can reuse this file!


### Configure Gemini

1.  Install [Gemini
    CLI](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/index.md)
    or [Gemini Code
    Assist](https://marketplace.visualstudio.com/items?itemName=Google.geminicodeassist)

1.  Create or edit the file at `~/.gemini/settings.json`, adding your server
    to the `mcpServers` list.

    ```json
    {
      "mcpServers": {
        "ads-mcp": {
          "command": "pipx",
          "args": [
            "run",
            "--spec",
            "git+https://github.com/googleads/google-ads-mcp.git",
            "google-ads-mcp"
          ]
        }
      }
    }
    ```



## Try it out :lab_coat:

Launch Gemini Code Assist or Gemini CLI and type `/mcp`. You should see
`ads-mcp` listed in the results.

Here are some sample prompts to get you started:

- Ask what the server can do:

  ```
  what can the ads-mcp server do?
  ```

## Contributing

Contributions welcome! See the [Contributing Guide](CONTRIBUTING.md).
