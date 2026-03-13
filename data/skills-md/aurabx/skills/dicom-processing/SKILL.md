---
name: "DICOM Processing"
description: "Work with DICOM medical imaging files programmatically using pydicom, dcmtk, and related tools. Read, write, modify, and validate DICOM tags, pixel data, and metadata. Use when reading DICOM files, extracting metadata, modifying tags, working with pixel data, converting transfer syntaxes, validating DICOM conformance, or scripting bulk DICOM operations."
---

# DICOM Processing

## What This Skill Does

Generates correct code for reading, writing, and manipulating DICOM (Digital Imaging and Communications in Medicine) files. Covers the pydicom Python library (primary), DCMTK command-line tools, and the DICOM data model including tags, VRs, transfer syntaxes, and SOP classes.

## Prerequisites

- Python 3.8+ with pydicom (`pip install pydicom`)
- Optional: `pillow` or `numpy` for pixel data operations
- Optional: `pylibjpeg` + `pylibjpeg-libjpeg` for compressed transfer syntaxes
- Optional: DCMTK toolkit for command-line operations

```bash
# Core
pip install pydicom

# Pixel data handling
pip install pydicom[all]
# Or individually:
pip install numpy pillow pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg

# DCMTK (command-line tools)
# macOS
brew install dcmtk
# Ubuntu/Debian
apt-get install dcmtk
```

---

## Quick Start

### Read a DICOM File

```python
import pydicom

ds = pydicom.dcmread("image.dcm")

# Access common attributes
print(ds.PatientName)        # Patient's name
print(ds.StudyDate)          # Study date (YYYYMMDD)
print(ds.Modality)           # CT, MR, US, CR, etc.
print(ds.StudyInstanceUID)   # Unique study identifier
print(ds.SeriesInstanceUID)  # Unique series identifier
print(ds.SOPInstanceUID)     # Unique instance identifier
```

### Modify and Save

```python
ds = pydicom.dcmread("image.dcm")
ds.PatientName = "ANONYMOUS"
ds.PatientID = "ANON001"
ds.save_as("modified.dcm")
```

### Access Pixel Data

```python
ds = pydicom.dcmread("image.dcm")
pixel_array = ds.pixel_array  # Returns numpy ndarray
print(pixel_array.shape)      # e.g., (512, 512) for a single frame
print(pixel_array.dtype)      # e.g., int16
```

---

## DICOM Data Model

### Tags

Every DICOM attribute is identified by a (group, element) tag pair:

```python
from pydicom.tag import Tag

# Access by keyword (preferred)
ds.PatientName

# Access by tag number
ds[0x0010, 0x0010]  # Same as PatientName

# Access by Tag object
ds[Tag(0x0010, 0x0010)]

# Check if tag exists
if "PatientName" in ds:
    print(ds.PatientName)
```

### Common Tags Reference

| Tag | Keyword | VR | Description |
|-----|---------|-----|-------------|
| (0008,0020) | StudyDate | DA | Date the study started |
| (0008,0030) | StudyTime | TM | Time the study started |
| (0008,0050) | AccessionNumber | SH | RIS accession number |
| (0008,0060) | Modality | CS | CT, MR, US, CR, XA, etc. |
| (0008,0070) | Manufacturer | LO | Equipment manufacturer |
| (0008,103E) | SeriesDescription | LO | Description of the series |
| (0008,1030) | StudyDescription | LO | Description of the study |
| (0010,0010) | PatientName | PN | Patient's full name |
| (0010,0020) | PatientID | LO | Patient identifier |
| (0010,0030) | PatientBirthDate | DA | Patient date of birth |
| (0010,0040) | PatientSex | CS | M, F, or O |
| (0020,000D) | StudyInstanceUID | UI | Unique study identifier |
| (0020,000E) | SeriesInstanceUID | UI | Unique series identifier |
| (0008,0018) | SOPInstanceUID | UI | Unique instance identifier |
| (0008,0016) | SOPClassUID | UI | Type of DICOM object |
| (0028,0010) | Rows | US | Image height in pixels |
| (0028,0011) | Columns | US | Image width in pixels |
| (0028,0100) | BitsAllocated | US | Bits per pixel (8, 16) |
| (0028,0004) | PhotometricInterpretation | CS | MONOCHROME1, MONOCHROME2, RGB |
| (7FE0,0010) | PixelData | OB/OW | The actual pixel data |

### Value Representations (VRs)

VRs define the data type and format of a DICOM value:

| VR | Name | Python Type | Example |
|----|------|-------------|---------|
| CS | Code String | str | `"CT"`, `"MR"` |
| DA | Date | str | `"20250115"` (YYYYMMDD) |
| DS | Decimal String | DSfloat/str | `"1.5"` |
| IS | Integer String | IS/str | `"512"` |
| LO | Long String | str | Max 64 chars |
| PN | Person Name | PersonName | `"Smith^John"` |
| SH | Short String | str | Max 16 chars |
| TM | Time | str | `"143025.000"` (HHMMSS.FFFFFF) |
| UI | Unique Identifier | UID | `"1.2.840..."` |
| US | Unsigned Short | int | `512` |
| OB | Other Byte | bytes | Binary data |
| OW | Other Word | bytes | Binary data |
| SQ | Sequence | Sequence | List of datasets |

### Sequences

Sequences are nested datasets (like arrays of objects):

```python
# Read a sequence
if "ReferencedStudySequence" in ds:
    for item in ds.ReferencedStudySequence:
        print(item.ReferencedSOPClassUID)
        print(item.ReferencedSOPInstanceUID)

# Create a sequence
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence

item = Dataset()
item.ReferencedSOPClassUID = "1.2.840.10008.5.1.4.1.1.2"
item.ReferencedSOPInstanceUID = pydicom.uid.generate_uid()

ds.ReferencedStudySequence = Sequence([item])
```

---

## Working with Pixel Data

### Read Pixel Data as NumPy Array

```python
import pydicom
import numpy as np

ds = pydicom.dcmread("ct_image.dcm")
pixels = ds.pixel_array  # numpy ndarray

# Apply rescale slope/intercept for CT (Hounsfield units)
if hasattr(ds, "RescaleSlope") and hasattr(ds, "RescaleIntercept"):
    hu = pixels * ds.RescaleSlope + ds.RescaleIntercept
```

### Window/Level for Display

```python
def apply_window(pixels, window_center, window_width):
    """Apply window/level to pixel data for display."""
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    windowed = np.clip(pixels, img_min, img_max)
    windowed = ((windowed - img_min) / (img_max - img_min) * 255)
    return windowed.astype(np.uint8)

# Common CT windows
LUNG_WINDOW = (-600, 1500)      # center, width
BONE_WINDOW = (400, 1800)
SOFT_TISSUE = (40, 400)
BRAIN_WINDOW = (40, 80)

display = apply_window(hu, *SOFT_TISSUE)
```

### Save as PNG

```python
from PIL import Image

# For grayscale (CT, MR, CR)
img = Image.fromarray(display, mode="L")
img.save("output.png")

# For RGB (ultrasound, pathology)
if ds.PhotometricInterpretation == "RGB":
    img = Image.fromarray(pixels, mode="RGB")
    img.save("output.png")
```

### Multi-frame Images

```python
ds = pydicom.dcmread("multiframe.dcm")
pixels = ds.pixel_array  # Shape: (num_frames, rows, cols)

print(f"Frames: {ds.NumberOfFrames}")
print(f"Shape: {pixels.shape}")

# Access individual frames
frame_0 = pixels[0]
```

---

## Transfer Syntaxes

Transfer syntaxes define how DICOM data is encoded (byte order, compression):

```python
print(ds.file_meta.TransferSyntaxUID)
```

| UID | Name | Compression |
|-----|------|-------------|
| 1.2.840.10008.1.2 | Implicit VR Little Endian | None |
| 1.2.840.10008.1.2.1 | Explicit VR Little Endian | None |
| 1.2.840.10008.1.2.4.50 | JPEG Baseline | Lossy |
| 1.2.840.10008.1.2.4.70 | JPEG Lossless | Lossless |
| 1.2.840.10008.1.2.4.90 | JPEG 2000 Lossless | Lossless |
| 1.2.840.10008.1.2.4.91 | JPEG 2000 | Lossy |
| 1.2.840.10008.1.2.5 | RLE Lossless | Lossless |

### Decompressing Pixel Data

```python
# Install handlers for compressed transfer syntaxes
# pip install pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg

ds = pydicom.dcmread("compressed.dcm")
ds.decompress()  # Convert to uncompressed in-memory
pixels = ds.pixel_array
```

### Converting Transfer Syntax

```bash
# Using DCMTK
# Decompress to Explicit VR Little Endian
dcmconv +te input.dcm output.dcm

# Compress to JPEG 2000 Lossless
dcmcjp2k +e2 input.dcm output.dcm

# Compress to JPEG Lossless
dcmcjpls +el input.dcm output.dcm
```

---

## Creating DICOM Files

### Create a DICOM File from Scratch

```python
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid, ExplicitVRLittleEndian
from pydicom.sequence import Sequence
import numpy as np
import datetime

# Create file dataset
filename = "new_image.dcm"
file_meta = pydicom.Dataset()
file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.2"  # CT
file_meta.MediaStorageSOPInstanceUID = generate_uid()
file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\x00" * 128)

# Patient info
ds.PatientName = "Test^Patient"
ds.PatientID = "TEST001"
ds.PatientBirthDate = "19900101"
ds.PatientSex = "O"

# Study info
ds.StudyInstanceUID = generate_uid()
ds.StudyDate = datetime.date.today().strftime("%Y%m%d")
ds.StudyTime = datetime.datetime.now().strftime("%H%M%S")
ds.Modality = "CT"

# Series info
ds.SeriesInstanceUID = generate_uid()
ds.SeriesNumber = 1

# Instance info
ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.2"
ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
ds.InstanceNumber = 1

# Image info
ds.Rows = 512
ds.Columns = 512
ds.BitsAllocated = 16
ds.BitsStored = 16
ds.HighBit = 15
ds.PixelRepresentation = 1  # signed
ds.SamplesPerPixel = 1
ds.PhotometricInterpretation = "MONOCHROME2"

# Pixel data
pixel_data = np.zeros((512, 512), dtype=np.int16)
ds.PixelData = pixel_data.tobytes()

ds.save_as(filename)
```

---

## Bulk Operations

### Iterate DICOM Files in a Directory

```python
from pathlib import Path
import pydicom

def iter_dicom_files(directory: str):
    """Yield (path, dataset) for all DICOM files in a directory tree."""
    for path in Path(directory).rglob("*"):
        if path.is_file():
            try:
                ds = pydicom.dcmread(str(path), stop_before_pixels=True)
                yield path, ds
            except pydicom.errors.InvalidDicomError:
                continue

# Extract metadata from all files
for path, ds in iter_dicom_files("/data/studies"):
    print(f"{path}: {ds.PatientName} | {ds.Modality} | {ds.StudyDate}")
```

### Group Files by Study/Series

```python
from collections import defaultdict

studies = defaultdict(lambda: defaultdict(list))

for path, ds in iter_dicom_files("/data/incoming"):
    study_uid = ds.StudyInstanceUID
    series_uid = ds.SeriesInstanceUID
    studies[study_uid][series_uid].append(path)

for study_uid, series in studies.items():
    print(f"Study {study_uid}: {len(series)} series")
    for series_uid, files in series.items():
        print(f"  Series {series_uid}: {len(files)} instances")
```

### Read Metadata Only (Fast)

```python
# stop_before_pixels=True skips pixel data -- much faster for metadata-only operations
ds = pydicom.dcmread("large_image.dcm", stop_before_pixels=True)
```

### Extract Specific Tags

```python
# Read only specific tags (fastest for large datasets)
ds = pydicom.dcmread("image.dcm", specific_tags=[
    "PatientName", "PatientID", "StudyDate", "Modality",
    "StudyInstanceUID", "SeriesInstanceUID",
])
```

---

## DCMTK Command-Line Tools

### Common Commands

```bash
# Dump DICOM metadata
dcmdump image.dcm

# Dump specific tags
dcmdump +P "0010,0010" +P "0008,0060" image.dcm

# Modify tags
dcmodify -m "(0010,0010)=ANONYMOUS" image.dcm

# Convert transfer syntax
dcmconv +te input.dcm output.dcm    # To Explicit VR LE

# Validate DICOM conformance
dcmpschk image.dcm

# Send via C-STORE
storescu -v -aec REMOTE_AE host port image.dcm

# Query via C-FIND
findscu -v -aec REMOTE_AE host port -k "0008,0060=CT" -k "0010,0010=Smith*"

# Retrieve via C-MOVE
movescu -v -aec REMOTE_AE -aem MY_AE host port -k "0020,000D=1.2.3..."
```

---

## Gotchas

- **PatientName uses `^` as separator**: `"Family^Given^Middle^Prefix^Suffix"`. Use `str(ds.PatientName)` for display, `ds.PatientName.family_name` for components.
- **Dates are strings, not date objects**: `StudyDate` is `"20250115"`, not a Python date. Parse with `datetime.strptime(ds.StudyDate, "%Y%m%d")`.
- **UIDs must be globally unique**: Always use `pydicom.uid.generate_uid()` when creating new studies/series/instances. Never reuse UIDs.
- **Pixel data may be compressed**: Always handle the case where `ds.pixel_array` raises an error due to missing decompression handlers. Install `pylibjpeg` packages.
- **Private tags**: Vendor-specific data uses odd group numbers (e.g., `(0009,xxxx)`). Access with `ds[0x0009, 0x0010]`.
- **Encoding**: DICOM defaults to ISO-IR 100 (Latin-1). Check `SpecificCharacterSet` for non-Latin text. pydicom handles decoding automatically.
- **File vs dataset**: Use `pydicom.dcmread()` to read files. The returned `FileDataset` includes file meta information. For in-memory datasets, use `Dataset()` directly.
- **Modifying PixelData**: If you modify pixel data, update `Rows`, `Columns`, `BitsAllocated`, `BitsStored`, `HighBit`, `PixelRepresentation`, and `PhotometricInterpretation` to match.

---

## Resources

- [pydicom Documentation](https://pydicom.github.io/pydicom/stable/)
- [pydicom User Guide](https://pydicom.github.io/pydicom/stable/tutorials/dataset_basics.html)
- [DICOM Standard Browser](https://dicom.innolitics.com/ciods)
- [DCMTK Documentation](https://dicom.offis.de/dcmtk.php.en)
- [DICOM Standard (official)](https://www.dicomstandard.org/current)
