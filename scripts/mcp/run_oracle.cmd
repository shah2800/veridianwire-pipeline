@echo off
set "PATH=C:\Users\x\.local\bin;C:\Program Files\nodejs;C:\Users\x\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin;%PATH%"
set "OCI_CONFIG_PROFILE=DEFAULT"
set "OCI_CLI_AUTH=security_token"
set "FASTMCP_LOG_LEVEL=ERROR"
"C:\Users\x\.local\bin\uvx.exe" oracle.oci-api-mcp-server
