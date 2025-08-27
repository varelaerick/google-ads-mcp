from ads_mcp.coordinator import mcp

import ads_mcp.tools.search as search
import ads_mcp.tools.core as core


def run_server() -> None:    
    mcp.run()
    

if __name__ == "__main__":
    run_server()
