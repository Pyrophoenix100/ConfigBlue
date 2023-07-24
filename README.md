Description
-----------

ConfigBlue is a Cisco router configuration tool. It allows for fast configuration generation for multiple routers, supporting several basic features of the Cisco IOS platform. This tool currently only supports basic features of it's current supported feature set. This tool is currently very limited and mostly used for setting up Cisco routing labs very quickly. The interface is very easy to use and follows a hierarchical menu system. It also features some basic input validation that allows for quick typing without fear of a bad config.

Supported Features:

*   No IP Domain Lookup (Default)
*   Hostname
*   Enable Password
*   VTY Password
*   Interfaces
*   Console 
    *   Password
    *   Synchronous Logging
*   Routing
    *   RIPv2
    *   EIGRP
    *   OSPF
    *   BGP

Usage
-----

Download the entire repository and run `RouterConfig.py`. It will automatically place the configs in the `/configs/` directory. The configs are in text format and can be pasted into a clean router from user EXEC.
