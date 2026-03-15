---
name: "DICOMweb Protocol"
description: "Build DICOMweb clients and integrations using WADO-RS (retrieve), STOW-RS (store), and QIDO-RS (query) protocols. Handles multipart MIME encoding, content negotiation, query parameters, and authentication. Use when building DICOMweb clients, querying a DICOMweb server, uploading DICOM via STOW-RS, retrieving imaging via WADO-RS, or integrating with any DICOMweb-compliant system including Aurabox, Orthanc, dcm4chee, or Google Cloud Healthcare API."
---

# DICOMweb Protocol

## What This Skill Does

Generates correct HTTP client code for the DICOMweb standard (WADO-RS, STOW-RS, QIDO-RS). Handles the parts that trip up developers: multipart MIME encoding, DICOM-specific content types, query parameter syntax, and bulk data retrieval. Works with any DICOMweb-compliant server.

## Prerequisites

- Python 3.8+ with `requests` (or `httpx` for async)
- Understanding of DICOM data model (studies, series, instances)
- A DICOMweb-compliant server endpoint

---

## Protocol Overview

DICOMweb provides three RESTful services for medical imaging:

| Service | Purpose | HTTP Methods | Path Pattern |
|---------|---------|-------------|--------------|
| **QIDO-RS** | Query (search) | GET | `/studies`, `/series`, `/instances` |
| **WADO-RS** | Retrieve (download) | GET | `/studies/{uid}`, `.../series/{uid}`, `.../instances/{uid}` |
| **STOW-RS** | Store (upload) | POST | `/studies`, `/studies/{uid}` |

### URL Structure

```
{base_url}/studies                                          # All studies
{base_url}/studies/{StudyInstanceUID}                       # One study
{base_url}/studies/{StudyInstanceUID}/series                # Series in study
{base_url}/studies/{StudyInstanceUID}/series/{SeriesInstanceUID}
{base_url}/studies/{StudyInstanceUID}/series/{SeriesInstanceUID}/instances
{base_url}/studies/{StudyInstanceUID}/series/{SeriesInstanceUID}/instances/{SOPInstanceUID}
```

---

## QIDO-RS (Query)

Search for studies, series, or instances by DICOM attributes.

### Basic Queries

```python
import requests

BASE_URL = "https://your-dicomweb-server.com/dicomweb"
HEADERS = {"Accept": "application/dicom+json"}
# Add auth headers as needed:
# HEADERS["Authorization"] = "Bearer {token}"

# Search for all CT studies
response = requests.get(
    f"{BASE_URL}/studies",
    headers=HEADERS,
    params={"ModalitiesInStudy": "CT"},
)
studies = response.json()

# Search for studies by patient name (wildcard supported)
response = requests.get(
    f"{BASE_URL}/studies",
    headers=HEADERS,
    params={"PatientName": "Smith*"},
)

# Search for studies by date range
response = requests.get(
    f"{BASE_URL}/studies",
    headers=HEADERS,
    params={"StudyDate": "20250101-20250131"},
)

# Search for series within a specific study
response = requests.get(
    f"{BASE_URL}/studies/{study_uid}/series",
    headers=HEADERS,
    params={"Modality": "CT"},
)
```

### Query Parameters

QIDO-RS uses DICOM tag keywords as query parameters:

| Parameter | Example | Description |
|-----------|---------|-------------|
| `PatientName` | `Smith*` | Wildcard search with `*` |
| `PatientID` | `12345` | Exact match |
| `StudyDate` | `20250115` | Single date |
| `StudyDate` | `20250101-20250131` | Date range |
| `ModalitiesInStudy` | `CT` | Filter by modality |
| `StudyInstanceUID` | `1.2.3...` | Exact UID match |
| `AccessionNumber` | `ACC001` | RIS accession number |
| `StudyDescription` | `*CHEST*` | Wildcard in description |
| `limit` | `25` | Max results per page |
| `offset` | `50` | Skip first N results |
| `includefield` | `all` | Return all fields (or specify tags) |

### Response Format (application/dicom+json)

```json
[
  {
    "00080020": { "vr": "DA", "Value": ["20250115"] },
    "00080060": { "vr": "CS", "Value": ["CT"] },
    "00080090": { "vr": "PN", "Value": [{ "Alphabetic": "Smith^John" }] },
    "0008103E": { "vr": "LO", "Value": ["CT CHEST W CONTRAST"] },
    "00100010": { "vr": "PN", "Value": [{ "Alphabetic": "Doe^Jane" }] },
    "00100020": { "vr": "LO", "Value": ["PAT001"] },
    "0020000D": { "vr": "UI", "Value": ["1.2.840.113619..."] }
  }
]
```

### Parsing DICOM JSON

```python
def parse_dicom_json_value(element: dict):
    """Extract the value from a DICOM JSON element."""
    if "Value" not in element:
        return None
    values = element["Value"]
    vr = element.get("vr", "")

    if vr == "PN":
        # Person Name has nested structure
        return values[0].get("Alphabetic", "") if values else ""
    elif len(values) == 1:
        return values[0]
    else:
        return values

def get_tag_value(result: dict, tag: str):
    """Get a tag value from a QIDO-RS result.

    Args:
        result: A single QIDO-RS result dict
        tag: Tag as 8-char hex string, e.g., '00100010' for PatientName
    """
    element = result.get(tag, {})
    return parse_dicom_json_value(element)

# Common tag hex codes
PATIENT_NAME = "00100010"
PATIENT_ID = "00100020"
STUDY_DATE = "00080020"
MODALITY = "00080060"
STUDY_UID = "0020000D"
SERIES_UID = "0020000E"
SOP_UID = "00080018"
STUDY_DESCRIPTION = "00081030"
SERIES_DESCRIPTION = "0008103E"
NUM_INSTANCES = "00201208"

# Usage
for study in studies:
    patient = get_tag_value(study, PATIENT_NAME)
    date = get_tag_value(study, STUDY_DATE)
    modality = get_tag_value(study, MODALITY)
    print(f"{patient} | {date} | {modality}")
```

### Pagination

```python
def paginate_qido(base_url: str, path: str, params: dict = None,
                  headers: dict = None, page_size: int = 50):
    """Paginate through QIDO-RS results."""
    params = params or {}
    params["limit"] = page_size
    offset = 0

    while True:
        params["offset"] = offset
        response = requests.get(f"{base_url}/{path}",
                                headers=headers, params=params)
        results = response.json()

        if not results:
            break

        yield from results
        offset += len(results)

        if len(results) < page_size:
            break

# Usage
for study in paginate_qido(BASE_URL, "studies",
                            params={"ModalitiesInStudy": "CT"},
                            headers=HEADERS):
    print(get_tag_value(study, STUDY_UID))
```

---

## WADO-RS (Retrieve)

Download DICOM instances, metadata, or rendered images.

### Retrieve Study Metadata

```python
# Get metadata for all instances in a study (no pixel data)
response = requests.get(
    f"{BASE_URL}/studies/{study_uid}/metadata",
    headers={"Accept": "application/dicom+json"},
)
metadata = response.json()  # List of instance metadata dicts
```

### Retrieve DICOM Instances

```python
import re


def retrieve_instance(base_url: str, study_uid: str, series_uid: str,
                      sop_uid: str, headers: dict = None) -> bytes:
    """Retrieve a single DICOM instance as bytes."""
    url = (f"{base_url}/studies/{study_uid}/series/{series_uid}"
           f"/instances/{sop_uid}")
    h = {**(headers or {}), "Accept": "application/dicom"}
    response = requests.get(url, headers=h)
    response.raise_for_status()
    return response.content


def retrieve_study_multipart(base_url: str, study_uid: str,
                             headers: dict = None) -> list[bytes]:
    """Retrieve all instances in a study as a multipart response."""
    url = f"{base_url}/studies/{study_uid}"
    h = {
        **(headers or {}),
        "Accept": 'multipart/related; type="application/dicom"',
    }
    response = requests.get(url, headers=h, stream=True)
    response.raise_for_status()

    # Parse multipart response
    content_type = response.headers["Content-Type"]
    return parse_multipart_dicom(response.content, content_type)


def parse_multipart_dicom(content: bytes, content_type: str) -> list[bytes]:
    """Parse a multipart/related response into individual DICOM parts."""
    # Extract boundary from content-type
    boundary_match = re.search(r'boundary="?([^";]+)"?', content_type)
    if not boundary_match:
        raise ValueError("No boundary found in Content-Type")

    boundary = boundary_match.group(1).encode()
    parts = content.split(b"--" + boundary)

    dicom_parts = []
    for part in parts:
        # Skip preamble and epilogue
        part = part.strip()
        if not part or part == b"--":
            continue

        # Find the blank line separating headers from body
        header_end = part.find(b"\r\n\r\n")
        if header_end == -1:
            header_end = part.find(b"\n\n")
            if header_end == -1:
                continue
            body = part[header_end + 2:]
        else:
            body = part[header_end + 4:]

        if body:
            dicom_parts.append(body)

    return dicom_parts
```

### Retrieve Rendered Images (PNG/JPEG)

```python
# Get a rendered PNG of an instance
response = requests.get(
    f"{BASE_URL}/studies/{study_uid}/series/{series_uid}"
    f"/instances/{sop_uid}/rendered",
    headers={"Accept": "image/png"},
    params={
        "window": "40,400",  # center,width (for CT)
    },
)

with open("output.png", "wb") as f:
    f.write(response.content)

# Get a rendered JPEG thumbnail
response = requests.get(
    f"{BASE_URL}/studies/{study_uid}/series/{series_uid}"
    f"/instances/{sop_uid}/rendered",
    headers={"Accept": "image/jpeg"},
    params={
        "viewport": "256,256",   # max width, height
        "quality": "80",
    },
)
```

### Retrieve Specific Frames

```python
# Retrieve frame 1 of a multi-frame instance (1-indexed)
response = requests.get(
    f"{BASE_URL}/studies/{study_uid}/series/{series_uid}"
    f"/instances/{sop_uid}/frames/1",
    headers={"Accept": "application/dicom"},
)
```

---

## STOW-RS (Store)

Upload DICOM instances to a DICOMweb server.

### Upload DICOM Files

```python
from pathlib import Path
import uuid

def stow_rs_upload(base_url: str, dicom_files: list[str],
                   study_uid: str = None, headers: dict = None) -> dict:
    """
    Upload DICOM files via STOW-RS.

    Args:
        base_url: DICOMweb base URL
        dicom_files: List of paths to DICOM files
        study_uid: Optional StudyInstanceUID (appended to URL)
        headers: Optional headers (e.g., auth)
    """
    boundary = f"boundary-{uuid.uuid4().hex}"

    # Build URL
    url = f"{base_url}/studies"
    if study_uid:
        url = f"{url}/{study_uid}"

    # Build multipart body
    body = b""
    for filepath in dicom_files:
        data = Path(filepath).read_bytes()
        body += f"--{boundary}\r\n".encode()
        body += b"Content-Type: application/dicom\r\n"
        body += b"\r\n"
        body += data
        body += b"\r\n"
    body += f"--{boundary}--\r\n".encode()

    # Set headers
    h = {
        **(headers or {}),
        "Content-Type": (
            f'multipart/related; type="application/dicom"; '
            f"boundary={boundary}"
        ),
        "Accept": "application/dicom+json",
    }

    response = requests.post(url, headers=h, data=body)
    response.raise_for_status()

    return response.json() if response.content else {}


# Usage
result = stow_rs_upload(
    base_url="https://your-server.com/dicomweb",
    dicom_files=["image1.dcm", "image2.dcm", "image3.dcm"],
    headers={"Authorization": "Bearer {token}"},
)
```

### STOW-RS Response

A successful STOW-RS response includes a list of stored instances:

```json
{
  "00081190": {
    "vr": "UR",
    "Value": ["https://server.com/dicomweb/studies/1.2.3..."]
  },
  "00081198": {
    "vr": "SQ",
    "Value": []
  },
  "00081199": {
    "vr": "SQ",
    "Value": [
      {
        "00081150": { "vr": "UI", "Value": ["1.2.840.10008.5.1.4.1.1.2"] },
        "00081155": { "vr": "UI", "Value": ["1.2.3.4.5..."] },
        "00081190": { "vr": "UR", "Value": ["https://server.com/..."] }
      }
    ]
  }
}
```

| Tag | Meaning |
|-----|---------|
| `00081190` | Retrieve URL |
| `00081198` | Failed SOP Sequence (empty = all succeeded) |
| `00081199` | Referenced SOP Sequence (successfully stored instances) |

### Batch Uploads

```python
def stow_rs_batch(base_url: str, dicom_files: list[str],
                  batch_size: int = 50, headers: dict = None):
    """Upload DICOM files in batches to avoid request size limits."""
    for i in range(0, len(dicom_files), batch_size):
        batch = dicom_files[i:i + batch_size]
        print(f"Uploading batch {i // batch_size + 1} "
              f"({len(batch)} files)...")
        result = stow_rs_upload(base_url, batch, headers=headers)
        failed = result.get("00081198", {}).get("Value", [])
        if failed:
            print(f"  WARNING: {len(failed)} files failed")
        else:
            print(f"  OK: {len(batch)} files stored")
```

### Upload DICOM JSON + Bulk Data

STOW-RS also supports uploading DICOM JSON with bulk data URIs instead of raw DICOM files. This is less common but useful for programmatic instance creation:

```python
import json

def stow_rs_json(base_url: str, dicom_json: list[dict],
                 headers: dict = None) -> dict:
    """Upload instances as DICOM JSON (no binary DICOM files needed)."""
    boundary = f"boundary-{uuid.uuid4().hex}"
    url = f"{base_url}/studies"

    body = f"--{boundary}\r\n".encode()
    body += b"Content-Type: application/dicom+json\r\n\r\n"
    body += json.dumps(dicom_json).encode()
    body += b"\r\n"
    body += f"--{boundary}--\r\n".encode()

    h = {
        **(headers or {}),
        "Content-Type": (
            f'multipart/related; type="application/dicom+json"; '
            f"boundary={boundary}"
        ),
        "Accept": "application/dicom+json",
    }

    response = requests.post(url, headers=h, data=body)
    response.raise_for_status()
    return response.json() if response.content else {}
```

---

## Complete DICOMweb Client

```python
import requests
from pathlib import Path
from typing import Optional
import uuid
import json


class DICOMwebClient:
    """Client for DICOMweb QIDO-RS, WADO-RS, and STOW-RS."""

    def __init__(self, base_url: str, auth_token: str = None,
                 api_key: str = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if auth_token:
            self.session.headers["Authorization"] = f"Bearer {auth_token}"
        elif api_key:
            self.session.headers["Authorization"] = f"Bearer {api_key}"

    # --- QIDO-RS ---

    def search_studies(self, **params) -> list[dict]:
        """Search for studies. Pass DICOM keywords as keyword args."""
        return self._qido("studies", params)

    def search_series(self, study_uid: str = None, **params) -> list[dict]:
        path = f"studies/{study_uid}/series" if study_uid else "series"
        return self._qido(path, params)

    def search_instances(self, study_uid: str = None,
                         series_uid: str = None, **params) -> list[dict]:
        if study_uid and series_uid:
            path = f"studies/{study_uid}/series/{series_uid}/instances"
        elif study_uid:
            path = f"studies/{study_uid}/instances"
        else:
            path = "instances"
        return self._qido(path, params)

    def _qido(self, path: str, params: dict) -> list[dict]:
        response = self.session.get(
            f"{self.base_url}/{path}",
            headers={"Accept": "application/dicom+json"},
            params=params,
        )
        response.raise_for_status()
        return response.json() if response.content else []

    # --- WADO-RS ---

    def retrieve_metadata(self, study_uid: str,
                          series_uid: str = None,
                          sop_uid: str = None) -> list[dict]:
        """Retrieve instance metadata (no pixel data)."""
        path = self._build_path(study_uid, series_uid, sop_uid)
        response = self.session.get(
            f"{self.base_url}/{path}/metadata",
            headers={"Accept": "application/dicom+json"},
        )
        response.raise_for_status()
        return response.json()

    def retrieve_instance(self, study_uid: str, series_uid: str,
                          sop_uid: str) -> bytes:
        """Retrieve a single DICOM instance as bytes."""
        path = self._build_path(study_uid, series_uid, sop_uid)
        response = self.session.get(
            f"{self.base_url}/{path}",
            headers={"Accept": "application/dicom"},
        )
        response.raise_for_status()
        return response.content

    def retrieve_rendered(self, study_uid: str, series_uid: str,
                          sop_uid: str, media_type: str = "image/png",
                          window: str = None,
                          viewport: str = None) -> bytes:
        """Retrieve a rendered image (PNG/JPEG)."""
        path = self._build_path(study_uid, series_uid, sop_uid)
        params = {}
        if window:
            params["window"] = window
        if viewport:
            params["viewport"] = viewport
        response = self.session.get(
            f"{self.base_url}/{path}/rendered",
            headers={"Accept": media_type},
            params=params,
        )
        response.raise_for_status()
        return response.content

    # --- STOW-RS ---

    def store(self, dicom_files: list[str],
              study_uid: str = None) -> dict:
        """Upload DICOM files via STOW-RS."""
        boundary = f"boundary-{uuid.uuid4().hex}"
        url = f"{self.base_url}/studies"
        if study_uid:
            url = f"{url}/{study_uid}"

        body = b""
        for filepath in dicom_files:
            data = Path(filepath).read_bytes()
            body += f"--{boundary}\r\n".encode()
            body += b"Content-Type: application/dicom\r\n\r\n"
            body += data
            body += b"\r\n"
        body += f"--{boundary}--\r\n".encode()

        response = self.session.post(
            url,
            headers={
                "Content-Type": (
                    f'multipart/related; type="application/dicom"; '
                    f"boundary={boundary}"
                ),
                "Accept": "application/dicom+json",
            },
            data=body,
        )
        response.raise_for_status()
        return response.json() if response.content else {}

    # --- Helpers ---

    def _build_path(self, study_uid: str, series_uid: str = None,
                    sop_uid: str = None) -> str:
        path = f"studies/{study_uid}"
        if series_uid:
            path = f"{path}/series/{series_uid}"
        if sop_uid:
            path = f"{path}/instances/{sop_uid}"
        return path


# Usage
client = DICOMwebClient(
    base_url="https://your-server.com/dicomweb",
    auth_token="your-token",
)

# Search
studies = client.search_studies(PatientName="Smith*", ModalitiesInStudy="CT")

# Retrieve metadata
metadata = client.retrieve_metadata(study_uid="1.2.3...")

# Download a rendered image
png = client.retrieve_rendered(
    study_uid="1.2.3...",
    series_uid="1.2.3...",
    sop_uid="1.2.3...",
    window="40,400",
)
Path("output.png").write_bytes(png)

# Upload
result = client.store(["image1.dcm", "image2.dcm"])
```

---

## Server-Specific Notes

### Aurabox

- DICOMweb endpoint is generated per-organisation in Organisation Settings
- Currently supports STOW-RS (store). QIDO-RS/WADO-RS availability varies.
- Authentication via API key (Bearer token)
- Status: Pre-release

### Orthanc

- Enable DICOMweb plugin: `"Plugins": ["libOrthancDicomWeb.so"]`
- Base URL: `http://localhost:8042/dicom-web`
- Authentication: HTTP Basic (default `orthanc:orthanc`)

### dcm4chee-arc

- Base URL: `http://localhost:8080/dcm4chee-arc/aets/DCM4CHEE/rs`
- Full QIDO-RS, WADO-RS, STOW-RS support

### Google Cloud Healthcare API

- Base URL: `https://healthcare.googleapis.com/v1/projects/{project}/locations/{location}/datasets/{dataset}/dicomStores/{store}/dicomWeb`
- Authentication: Google OAuth 2.0

---

## Content-Type Reference

| Operation | Request Accept/Content-Type | Response Content-Type |
|-----------|---------------------------|----------------------|
| QIDO-RS | `Accept: application/dicom+json` | `application/dicom+json` |
| WADO-RS (metadata) | `Accept: application/dicom+json` | `application/dicom+json` |
| WADO-RS (instance) | `Accept: application/dicom` | `application/dicom` or `multipart/related` |
| WADO-RS (rendered) | `Accept: image/png` or `image/jpeg` | `image/png` or `image/jpeg` |
| STOW-RS (DICOM) | `Content-Type: multipart/related; type="application/dicom"` | `application/dicom+json` |
| STOW-RS (JSON) | `Content-Type: multipart/related; type="application/dicom+json"` | `application/dicom+json` |

---

## Gotchas

- **Content-Type for STOW-RS must include `type=` parameter**: `multipart/related; type="application/dicom"; boundary=xxx`. Missing the `type` parameter causes many servers to reject the request.
- **DICOM JSON uses tag hex codes, not keywords**: `"00100010"` not `"PatientName"`. Use a lookup table or the DICOM standard browser.
- **Person Names have nested structure**: In DICOM JSON, PN values are `{"Alphabetic": "Family^Given"}`, not plain strings.
- **Multipart boundaries**: The boundary string must not appear in the DICOM binary data. Use a UUID-based boundary.
- **Binary data in WADO-RS responses**: Retrieving a full study returns a multipart response that must be parsed. Individual instance retrieval is simpler.
- **Query wildcards**: QIDO-RS supports `*` as wildcard (not `%` or `?`). Case sensitivity varies by server.
- **Date ranges use `-`**: `StudyDate=20250101-20250131`, not `StudyDate>=20250101&StudyDate<=20250131`.
- **Pagination is not standardized**: Some servers use `limit`/`offset`, others use `Link` headers. Check your server's documentation.
- **Large uploads**: Break large studies into batches (50-100 instances per STOW-RS request) to avoid timeouts and memory issues.

---

## Resources

- [DICOMweb Standard (PS3.18)](https://dicom.nema.org/medical/dicom/current/output/chtml/part18/PS3.18.html)
- [DICOM Standard Browser (Innolitics)](https://dicom.innolitics.com/ciods) -- tag lookup
- [DICOMweb by Example (OHIF)](https://v3-docs.ohif.org/configuration/datasources/dicom-web/)
- [Orthanc DICOMweb Plugin](https://orthanc.uclouvain.be/book/plugins/dicomweb.html)
- [Google Cloud Healthcare DICOMweb](https://cloud.google.com/healthcare-api/docs/how-tos/dicomweb)
