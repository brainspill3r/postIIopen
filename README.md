# PostIIopen 🚀✨

![ci](https://github.com/brainspill3r/postIIopen/actions/workflows/ci.yml/badge.svg)

**A Python tool to convert Postman collections (JSON) to OpenAPI 3.0 definitions (YAML).**

## 🚀 USAGE

```
python3 postIIopen [input-file-path] [output-file-path]
```

### 🔍 Example

```
python3 postIIopen.py path/to/postman.json path/to/openapi.yml
```

## 😎 FEATURES

- **Conversion**: Transforms Postman collections into a basic OpenAPI 3.0 spec.
- **Server URL Extraction**: Automatically extracts the first absolute server URL from the Postman collection. If none is found, it falls back to a default.
- **CLI Tool**: A super simple command-line interface to perform the conversion.

## 📦 PREREQUISITES

- Python 3.7 or newer 🐍
- [PyYAML](https://pyyaml.org/)  
  Install via pip:

  ```
  pip install pyyaml
  ```

---

Have fun converting your Postman collections into awesome OpenAPI specs! 🎉
```

---
