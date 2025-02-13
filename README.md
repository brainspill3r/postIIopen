![ci](https://github.com/brainspill3r/postIIopen/actions/workflows/ci.yml/badge.svg)

###Usage

USAGE:
    postIIopen [input-file-path] [output-file-path]

Example;
    python postIIopen.py path/to/postman.json path/to/openapi.yml


A Python tool to convert Postman collections (JSON) to OpenAPI 3.0 definitions (YAML).

## Features

- **Conversion**: Transforms Postman collections into a basic OpenAPI 3.0 spec.
- **Server URL Extraction**: Automatically extracts the first absolute server URL from the Postman collection. If none is found, it falls back to a default.
- **CLI Tool**: Simple command-line interface to perform the conversion.

## Prerequisites

- Python 3.7 or newer
- [PyYAML](https://pyyaml.org/)  
  Install via pip:
  ```bash
  pip install pyyaml
