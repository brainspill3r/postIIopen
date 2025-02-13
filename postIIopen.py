import json
import yaml
import argparse
from urllib.parse import urlparse

def get_url_path(url):
    """
    Extracts the path component from a URL.
    The URL can be a string or a dictionary as provided in a Postman collection.
    """
    if isinstance(url, str):
        parsed = urlparse(url)
        return parsed.path if parsed.path else "/"
    elif isinstance(url, dict):
        if "raw" in url:
            parsed = urlparse(url["raw"])
            return parsed.path if parsed.path else "/"
        elif "path" in url:
            # When path is a list (e.g. ["api", "v1", "users"])
            if isinstance(url["path"], list):
                path = "/" + "/".join(url["path"])
            else:
                path = url["path"]
                if not path.startswith("/"):
                    path = "/" + path
            return path
    return "/"

def extract_first_server(postman):
    """
    Attempts to extract the first absolute server URL from the Postman collection.
    Returns a string like "https://api.example.com" if found, otherwise None.
    """
    def recurse(items):
        for item in items:
            if "request" in item:
                url = item["request"].get("url")
                if url:
                    if isinstance(url, dict):
                        # Prefer the 'raw' field if it exists
                        if "raw" in url:
                            raw_url = url["raw"]
                            parsed = urlparse(raw_url)
                            if parsed.scheme and parsed.netloc:
                                return f"{parsed.scheme}://{parsed.netloc}"
                        # Otherwise, check if protocol and host are provided
                        if "protocol" in url and "host" in url:
                            protocol = url.get("protocol")
                            host = url.get("host")
                            if isinstance(host, list):
                                host = ".".join(host)
                            if protocol and host:
                                return f"{protocol}://{host}"
                    elif isinstance(url, str):
                        parsed = urlparse(url)
                        if parsed.scheme and parsed.netloc:
                            return f"{parsed.scheme}://{parsed.netloc}"
            if "item" in item:
                result = recurse(item["item"])
                if result:
                    return result
        return None

    items = postman.get("item", [])
    return recurse(items)

def convert_item(item, paths):
    """
    Converts a single Postman item (endpoint) into an OpenAPI operation and updates the paths.
    """
    request = item["request"]
    method = request.get("method", "GET").lower()
    url = request.get("url", "/")
    path = get_url_path(url)

    # Build the OpenAPI operation
    operation = {
        "summary": item.get("name", ""),
        "description": request.get("description", ""),
        "responses": {
            "default": {
                "description": "Default response"
            }
        }
    }

    # Handle query parameters if defined in the Postman URL
    if isinstance(url, dict) and "query" in url:
        parameters = []
        for query_param in url["query"]:
            parameters.append({
                "name": query_param.get("key"),
                "in": "query",
                "description": query_param.get("description", ""),
                # If a parameter is marked as disabled, we'll treat it as not required.
                "required": not query_param.get("disabled", False),
                "schema": {"type": "string"}
            })
        if parameters:
            operation["parameters"] = parameters

    # Ensure the path exists in the OpenAPI spec and add the operation
    if path not in paths:
        paths[path] = {}
    paths[path][method] = operation

def process_items(items, paths):
    """
    Recursively process a list of Postman items (which might be nested folders) to populate OpenAPI paths.
    """
    for item in items:
        if "item" in item:
            process_items(item["item"], paths)
        elif "request" in item:
            convert_item(item, paths)

def convert_postman_to_openapi(postman):
    """
    Converts a Postman collection into an OpenAPI 3.0 dictionary.
    """
    # Extract default server from Postman collection. If not found, use fallback.
    server_url = extract_first_server(postman)
    if not server_url:
        server_url = "http://localhost"
    
    openapi = {
        "openapi": "3.0.0",
        "info": {
            "title": postman.get("info", {}).get("name", "Converted API"),
            "description": postman.get("info", {}).get("description", ""),
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": server_url
            }
        ],
        "paths": {}
    }
    items = postman.get("item", [])
    process_items(items, openapi["paths"])
    return openapi

def main():
    parser = argparse.ArgumentParser(
        description="Convert a Postman collection (JSON) to an OpenAPI definition (YAML)"
    )
    parser.add_argument("input", help="Path to the Postman JSON file")
    parser.add_argument("output", help="Path to the output OpenAPI YAML file")
    args = parser.parse_args()

    # Load the Postman collection
    with open(args.input, "r") as f:
        postman = json.load(f)

    # Convert to OpenAPI spec
    openapi_spec = convert_postman_to_openapi(postman)

    # Write the OpenAPI spec to a YAML file
    with open(args.output, "w") as f:
        yaml.dump(openapi_spec, f, sort_keys=False)

if __name__ == "__main__":
    main()

