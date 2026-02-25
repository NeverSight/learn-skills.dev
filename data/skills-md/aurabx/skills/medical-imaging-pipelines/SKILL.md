---
name: "Medical Imaging Pipelines"
description: "Build automated pipelines for medical imaging data: format conversion (DICOM to NIfTI, PNG, HDF5), batch processing, ML dataset preparation, research data export, and imaging ETL workflows. Use when converting DICOM to other formats, preparing imaging datasets for machine learning, building research data pipelines, batch processing medical images, extracting imaging features, or automating imaging workflows."
---

# Medical Imaging Pipelines

## What This Skill Does

Generates code for end-to-end medical imaging data pipelines: ingestion, format conversion, preprocessing, dataset preparation, and export. Covers the common path from raw DICOM files to ML-ready datasets, research exports, and automated processing workflows.

## Prerequisites

- Python 3.8+
- Core: `pydicom`, `numpy`
- Conversion: `SimpleITK` or `nibabel` (for NIfTI), `pillow` (for PNG/JPEG)
- ML prep: `scikit-image`, `scipy`
- Optional: `h5py` (HDF5), `pandas` (metadata), `tqdm` (progress bars)

```bash
# Full pipeline toolkit
pip install pydicom numpy SimpleITK nibabel pillow scikit-image scipy h5py pandas tqdm pylibjpeg pylibjpeg-libjpeg
```

---

## Quick Start: DICOM Directory to ML Dataset

```python
from pathlib import Path
import pydicom
import numpy as np
from PIL import Image

def dicom_dir_to_pngs(input_dir: str, output_dir: str):
    """Convert a directory of DICOM files to PNG images."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for dcm_file in sorted(input_path.rglob("*")):
        if dcm_file.is_dir():
            continue
        try:
            ds = pydicom.dcmread(str(dcm_file))
            pixels = ds.pixel_array.astype(float)

            # Normalize to 0-255
            if pixels.max() != pixels.min():
                pixels = (pixels - pixels.min()) / (pixels.max() - pixels.min()) * 255
            pixels = pixels.astype(np.uint8)

            img = Image.fromarray(pixels)
            img.save(output_path / f"{dcm_file.stem}.png")
        except Exception as e:
            print(f"Skipped {dcm_file.name}: {e}")

dicom_dir_to_pngs("/data/dicom_study", "/data/png_output")
```

---

## Format Conversion

### DICOM to NIfTI (Neuroimaging)

NIfTI is the standard format for neuroimaging research (brain MRI, fMRI). Use `SimpleITK` for robust conversion that preserves spatial metadata.

```python
import SimpleITK as sitk
from pathlib import Path

def dicom_series_to_nifti(dicom_dir: str, output_path: str):
    """Convert a DICOM series to a NIfTI file.

    Args:
        dicom_dir: Directory containing DICOM files for ONE series
        output_path: Output .nii.gz file path
    """
    reader = sitk.ImageSeriesReader()
    dicom_files = reader.GetGDCMSeriesFileNames(dicom_dir)

    if not dicom_files:
        raise ValueError(f"No DICOM series found in {dicom_dir}")

    reader.SetFileNames(dicom_files)
    reader.MetaDataDictionaryArrayUpdateOn()
    reader.LoadPrivateTagsOn()

    image = reader.Execute()

    # Preserve orientation and spacing
    sitk.WriteImage(image, output_path)
    print(f"Written: {output_path}")
    print(f"  Size: {image.GetSize()}")
    print(f"  Spacing: {image.GetSpacing()}")
    print(f"  Origin: {image.GetOrigin()}")
    print(f"  Direction: {image.GetDirection()}")


def dicom_dir_to_nifti_all_series(dicom_dir: str, output_dir: str):
    """Convert all series in a directory to separate NIfTI files."""
    reader = sitk.ImageSeriesReader()
    series_ids = reader.GetGDCMSeriesIDs(dicom_dir)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for idx, series_id in enumerate(series_ids):
        dicom_files = reader.GetGDCMSeriesFileNames(dicom_dir,
                                                     series_id)
        reader.SetFileNames(dicom_files)
        image = reader.Execute()

        nifti_path = output_path / f"series_{idx:03d}_{series_id[:8]}.nii.gz"
        sitk.WriteImage(image, str(nifti_path))
        print(f"Series {idx}: {len(dicom_files)} files -> {nifti_path.name}")
```

#### Alternative: nibabel + pydicom

```python
import nibabel as nib
import pydicom
import numpy as np
from pathlib import Path

def dicom_to_nifti_manual(dicom_dir: str, output_path: str):
    """Manual DICOM to NIfTI conversion with full control."""
    # Read and sort slices
    slices = []
    for f in Path(dicom_dir).glob("*"):
        try:
            ds = pydicom.dcmread(str(f))
            slices.append(ds)
        except:
            continue

    # Sort by ImagePositionPatient Z coordinate
    slices.sort(key=lambda s: float(s.ImagePositionPatient[2]))

    # Build 3D volume
    volume = np.stack([s.pixel_array for s in slices], axis=-1)

    # Apply rescale if CT
    if hasattr(slices[0], "RescaleSlope"):
        volume = volume * slices[0].RescaleSlope + slices[0].RescaleIntercept

    # Build affine matrix from DICOM headers
    ds = slices[0]
    pos = [float(x) for x in ds.ImagePositionPatient]
    orient = [float(x) for x in ds.ImageOrientationPatient]
    spacing = [float(x) for x in ds.PixelSpacing]

    # Calculate slice spacing from first two slices
    if len(slices) > 1:
        pos2 = [float(x) for x in slices[1].ImagePositionPatient]
        slice_spacing = np.sqrt(sum((a - b) ** 2 for a, b in zip(pos, pos2)))
    else:
        slice_spacing = float(getattr(ds, "SliceThickness", 1.0))

    # Row and column direction cosines
    row_cosine = np.array(orient[:3])
    col_cosine = np.array(orient[3:])
    slice_cosine = np.cross(row_cosine, col_cosine)

    # Build 4x4 affine
    affine = np.eye(4)
    affine[:3, 0] = row_cosine * spacing[1]
    affine[:3, 1] = col_cosine * spacing[0]
    affine[:3, 2] = slice_cosine * slice_spacing
    affine[:3, 3] = pos

    nifti_img = nib.Nifti1Image(volume.astype(np.float32), affine)
    nib.save(nifti_img, output_path)
```

### DICOM to PNG/JPEG (2D Images)

```python
import pydicom
import numpy as np
from PIL import Image
from pathlib import Path

def dicom_to_png(dicom_path: str, output_path: str,
                 window_center: float = None,
                 window_width: float = None):
    """Convert a single DICOM file to PNG with optional windowing."""
    ds = pydicom.dcmread(dicom_path)
    pixels = ds.pixel_array.astype(np.float64)

    # Apply rescale slope/intercept (CT Hounsfield units)
    slope = float(getattr(ds, "RescaleSlope", 1))
    intercept = float(getattr(ds, "RescaleIntercept", 0))
    pixels = pixels * slope + intercept

    # Apply window/level
    if window_center is None:
        window_center = float(getattr(ds, "WindowCenter",
                                       (pixels.max() + pixels.min()) / 2))
        if isinstance(window_center, pydicom.multival.MultiValue):
            window_center = float(window_center[0])
    if window_width is None:
        window_width = float(getattr(ds, "WindowWidth",
                                      pixels.max() - pixels.min()))
        if isinstance(window_width, pydicom.multival.MultiValue):
            window_width = float(window_width[0])

    img_min = window_center - window_width / 2
    img_max = window_center + window_width / 2
    pixels = np.clip(pixels, img_min, img_max)
    pixels = ((pixels - img_min) / (img_max - img_min) * 255).astype(np.uint8)

    # Handle photometric interpretation
    if getattr(ds, "PhotometricInterpretation", "") == "MONOCHROME1":
        pixels = 255 - pixels  # Invert

    img = Image.fromarray(pixels)
    img.save(output_path)
```

### DICOM to HDF5 (ML Datasets)

```python
import h5py
import pydicom
import numpy as np
from pathlib import Path
from tqdm import tqdm

def build_hdf5_dataset(dicom_dirs: dict[str, str], output_path: str,
                       include_metadata: bool = True):
    """
    Build an HDF5 dataset from DICOM directories.

    Args:
        dicom_dirs: Mapping of {label: dicom_directory_path}
                    e.g., {"train/positive": "/data/pos", "train/negative": "/data/neg"}
        output_path: Path for the output .h5 file
        include_metadata: Whether to store DICOM metadata alongside pixel data
    """
    with h5py.File(output_path, "w") as hf:
        for label, dicom_dir in dicom_dirs.items():
            group = hf.create_group(label)
            files = sorted(Path(dicom_dir).rglob("*.dcm"))

            # Determine shape from first file
            ds = pydicom.dcmread(str(files[0]))
            rows, cols = ds.Rows, ds.Columns

            # Pre-allocate dataset
            images = group.create_dataset(
                "images",
                shape=(len(files), rows, cols),
                dtype=np.float32,
                chunks=(1, rows, cols),
                compression="gzip",
                compression_opts=4,
            )

            if include_metadata:
                metadata_items = []

            for i, f in enumerate(tqdm(files, desc=label)):
                ds = pydicom.dcmread(str(f))
                pixels = ds.pixel_array.astype(np.float32)

                # Rescale
                slope = float(getattr(ds, "RescaleSlope", 1))
                intercept = float(getattr(ds, "RescaleIntercept", 0))
                pixels = pixels * slope + intercept

                images[i] = pixels

                if include_metadata:
                    metadata_items.append({
                        "file": f.name,
                        "patient_id": str(getattr(ds, "PatientID", "")),
                        "modality": str(getattr(ds, "Modality", "")),
                        "study_date": str(getattr(ds, "StudyDate", "")),
                        "spacing": [float(x) for x in getattr(ds, "PixelSpacing", [1, 1])],
                    })

            if include_metadata and metadata_items:
                import json
                group.attrs["metadata"] = json.dumps(metadata_items)

    print(f"Dataset saved: {output_path}")
    print(f"  Groups: {list(dicom_dirs.keys())}")
```

---

## Preprocessing

### Intensity Normalization

```python
def normalize_ct(volume: np.ndarray,
                 hu_min: float = -1000,
                 hu_max: float = 400) -> np.ndarray:
    """Clip and normalize CT Hounsfield units to [0, 1]."""
    volume = np.clip(volume, hu_min, hu_max)
    volume = (volume - hu_min) / (hu_max - hu_min)
    return volume.astype(np.float32)

def normalize_mri(volume: np.ndarray,
                  percentile_lower: float = 1,
                  percentile_upper: float = 99) -> np.ndarray:
    """Percentile-based normalization for MRI (handles intensity inhomogeneity)."""
    p_low = np.percentile(volume[volume > 0], percentile_lower)
    p_high = np.percentile(volume[volume > 0], percentile_upper)
    volume = np.clip(volume, p_low, p_high)
    volume = (volume - p_low) / (p_high - p_low)
    return volume.astype(np.float32)

def z_score_normalize(volume: np.ndarray,
                      mask: np.ndarray = None) -> np.ndarray:
    """Z-score normalization (zero mean, unit variance)."""
    if mask is not None:
        mean = volume[mask > 0].mean()
        std = volume[mask > 0].std()
    else:
        mean = volume.mean()
        std = volume.std()
    return ((volume - mean) / (std + 1e-8)).astype(np.float32)
```

### Resampling / Resize

```python
import SimpleITK as sitk

def resample_volume(image: sitk.Image,
                    new_spacing: tuple = (1.0, 1.0, 1.0),
                    interpolator=sitk.sitkLinear) -> sitk.Image:
    """Resample a 3D volume to isotropic spacing."""
    original_spacing = image.GetSpacing()
    original_size = image.GetSize()

    new_size = [
        int(round(osz * ospc / nspc))
        for osz, ospc, nspc in zip(original_size, original_spacing, new_spacing)
    ]

    resampler = sitk.ResampleImageFilter()
    resampler.SetOutputSpacing(new_spacing)
    resampler.SetSize(new_size)
    resampler.SetOutputDirection(image.GetDirection())
    resampler.SetOutputOrigin(image.GetOrigin())
    resampler.SetInterpolator(interpolator)
    resampler.SetDefaultPixelValue(0)

    return resampler.Execute(image)


def resize_2d(pixels: np.ndarray, target_size: tuple = (256, 256)) -> np.ndarray:
    """Resize a 2D image using PIL."""
    from PIL import Image
    img = Image.fromarray(pixels)
    img = img.resize(target_size, Image.Resampling.BILINEAR)
    return np.array(img)
```

### Cropping and Padding

```python
def center_crop_3d(volume: np.ndarray, crop_size: tuple) -> np.ndarray:
    """Center crop a 3D volume."""
    d, h, w = volume.shape
    cd, ch, cw = crop_size

    d_start = max(0, (d - cd) // 2)
    h_start = max(0, (h - ch) // 2)
    w_start = max(0, (w - cw) // 2)

    return volume[d_start:d_start+cd, h_start:h_start+ch, w_start:w_start+cw]


def pad_to_size(volume: np.ndarray, target_size: tuple,
                pad_value: float = 0) -> np.ndarray:
    """Pad a volume to a target size."""
    pad_widths = []
    for current, target in zip(volume.shape, target_size):
        total_pad = max(0, target - current)
        pad_before = total_pad // 2
        pad_after = total_pad - pad_before
        pad_widths.append((pad_before, pad_after))

    return np.pad(volume, pad_widths, mode="constant",
                  constant_values=pad_value)
```

---

## Metadata Extraction

### Build a Study Manifest

```python
import pandas as pd
import pydicom
from pathlib import Path
from tqdm import tqdm

def build_manifest(dicom_dir: str, output_csv: str = "manifest.csv") -> pd.DataFrame:
    """
    Scan a DICOM directory and build a metadata manifest.

    Returns a DataFrame with one row per DICOM file.
    """
    records = []
    dicom_path = Path(dicom_dir)

    for f in tqdm(list(dicom_path.rglob("*")), desc="Scanning"):
        if f.is_dir():
            continue
        try:
            ds = pydicom.dcmread(str(f), stop_before_pixels=True)
            records.append({
                "filepath": str(f.relative_to(dicom_path)),
                "patient_id": str(getattr(ds, "PatientID", "")),
                "patient_name": str(getattr(ds, "PatientName", "")),
                "study_uid": str(getattr(ds, "StudyInstanceUID", "")),
                "series_uid": str(getattr(ds, "SeriesInstanceUID", "")),
                "sop_uid": str(getattr(ds, "SOPInstanceUID", "")),
                "modality": str(getattr(ds, "Modality", "")),
                "study_date": str(getattr(ds, "StudyDate", "")),
                "study_description": str(getattr(ds, "StudyDescription", "")),
                "series_description": str(getattr(ds, "SeriesDescription", "")),
                "instance_number": int(getattr(ds, "InstanceNumber", 0)),
                "rows": int(getattr(ds, "Rows", 0)),
                "columns": int(getattr(ds, "Columns", 0)),
                "pixel_spacing": str(getattr(ds, "PixelSpacing", "")),
                "slice_thickness": str(getattr(ds, "SliceThickness", "")),
                "manufacturer": str(getattr(ds, "Manufacturer", "")),
            })
        except Exception:
            continue

    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    print(f"Manifest: {len(df)} files, {df['study_uid'].nunique()} studies, "
          f"{df['patient_id'].nunique()} patients")
    return df
```

### Dataset Statistics

```python
def dataset_statistics(manifest: pd.DataFrame):
    """Print summary statistics for a DICOM dataset."""
    print(f"Total files: {len(manifest)}")
    print(f"Patients: {manifest['patient_id'].nunique()}")
    print(f"Studies: {manifest['study_uid'].nunique()}")
    print(f"Series: {manifest['series_uid'].nunique()}")
    print(f"\nModality distribution:")
    print(manifest['modality'].value_counts().to_string())
    print(f"\nDate range: {manifest['study_date'].min()} - {manifest['study_date'].max()}")
    print(f"\nImage sizes:")
    print(f"  Rows: {manifest['rows'].min()}-{manifest['rows'].max()}")
    print(f"  Cols: {manifest['columns'].min()}-{manifest['columns'].max()}")
    print(f"\nManufacturers:")
    print(manifest['manufacturer'].value_counts().to_string())
```

---

## Complete Pipeline Example

### CT Research Pipeline

```python
"""
End-to-end pipeline: DICOM CT studies -> de-identified, normalized NIfTI volumes
"""
from pathlib import Path
import pydicom
import numpy as np
import SimpleITK as sitk
from tqdm import tqdm
import json


class CTResearchPipeline:
    """Pipeline for processing CT DICOM data for research."""

    def __init__(self, output_dir: str, target_spacing: tuple = (1.0, 1.0, 1.0),
                 hu_window: tuple = (-1000, 400)):
        self.output_dir = Path(output_dir)
        self.target_spacing = target_spacing
        self.hu_min, self.hu_max = hu_window
        self.manifest = []

        # Create output structure
        (self.output_dir / "volumes").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "metadata").mkdir(parents=True, exist_ok=True)

    def process_study(self, dicom_dir: str, subject_id: str):
        """Process a single DICOM study directory."""
        print(f"Processing {subject_id}...")

        # Step 1: Read DICOM series
        reader = sitk.ImageSeriesReader()
        series_ids = reader.GetGDCMSeriesIDs(dicom_dir)

        if not series_ids:
            print(f"  No DICOM series found in {dicom_dir}")
            return

        for series_idx, series_id in enumerate(series_ids):
            file_names = reader.GetGDCMSeriesFileNames(dicom_dir, series_id)
            reader.SetFileNames(file_names)
            reader.MetaDataDictionaryArrayUpdateOn()
            image = reader.Execute()

            # Step 2: Resample to target spacing
            image = self._resample(image)

            # Step 3: Convert to numpy for normalization
            volume = sitk.GetArrayFromImage(image)  # shape: (Z, Y, X)

            # Step 4: Normalize HU values
            volume = np.clip(volume, self.hu_min, self.hu_max)
            volume = ((volume - self.hu_min) /
                      (self.hu_max - self.hu_min)).astype(np.float32)

            # Step 5: Save as NIfTI
            output_image = sitk.GetImageFromArray(volume)
            output_image.CopyInformation(image)

            nifti_name = f"{subject_id}_series{series_idx:02d}.nii.gz"
            nifti_path = self.output_dir / "volumes" / nifti_name
            sitk.WriteImage(output_image, str(nifti_path))

            # Step 6: Save metadata
            metadata = self._extract_metadata(reader, file_names[0],
                                               subject_id, series_idx)
            metadata["output_file"] = nifti_name
            metadata["volume_shape"] = list(volume.shape)
            metadata["spacing"] = list(image.GetSpacing())

            meta_path = (self.output_dir / "metadata" /
                        f"{subject_id}_series{series_idx:02d}.json")
            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=2)

            self.manifest.append(metadata)
            print(f"  Series {series_idx}: {volume.shape} -> {nifti_name}")

    def _resample(self, image: sitk.Image) -> sitk.Image:
        original_spacing = image.GetSpacing()
        original_size = image.GetSize()
        new_size = [
            int(round(osz * ospc / nspc))
            for osz, ospc, nspc in zip(original_size, original_spacing,
                                        self.target_spacing)
        ]
        resampler = sitk.ResampleImageFilter()
        resampler.SetOutputSpacing(self.target_spacing)
        resampler.SetSize(new_size)
        resampler.SetOutputDirection(image.GetDirection())
        resampler.SetOutputOrigin(image.GetOrigin())
        resampler.SetInterpolator(sitk.sitkLinear)
        resampler.SetDefaultPixelValue(-1000)
        return resampler.Execute(image)

    def _extract_metadata(self, reader, first_file: str,
                          subject_id: str, series_idx: int) -> dict:
        ds = pydicom.dcmread(first_file, stop_before_pixels=True)
        return {
            "subject_id": subject_id,
            "series_index": series_idx,
            "modality": str(getattr(ds, "Modality", "")),
            "study_description": str(getattr(ds, "StudyDescription", "")),
            "series_description": str(getattr(ds, "SeriesDescription", "")),
            "manufacturer": str(getattr(ds, "Manufacturer", "")),
            "slice_thickness": float(getattr(ds, "SliceThickness", 0)),
            "kvp": float(getattr(ds, "KVP", 0)),
        }

    def save_manifest(self):
        manifest_path = self.output_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(self.manifest, f, indent=2)
        print(f"\nManifest saved: {manifest_path}")
        print(f"Total subjects: {len(set(m['subject_id'] for m in self.manifest))}")
        print(f"Total volumes: {len(self.manifest)}")


# Usage
pipeline = CTResearchPipeline(
    output_dir="/data/processed",
    target_spacing=(1.0, 1.0, 1.0),
    hu_window=(-1000, 400),
)

# Process each study
study_dirs = {
    "SUBJ-001": "/data/raw/patient_001",
    "SUBJ-002": "/data/raw/patient_002",
    "SUBJ-003": "/data/raw/patient_003",
}

for subject_id, dicom_dir in study_dirs.items():
    pipeline.process_study(dicom_dir, subject_id)

pipeline.save_manifest()
```

---

## PyTorch Dataset Integration

```python
import torch
from torch.utils.data import Dataset
import nibabel as nib
import numpy as np
import json
from pathlib import Path

class MedicalImageDataset(Dataset):
    """PyTorch dataset for processed medical imaging volumes."""

    def __init__(self, data_dir: str, transform=None,
                 target_key: str = None):
        self.data_dir = Path(data_dir)
        self.transform = transform

        # Load manifest
        with open(self.data_dir / "manifest.json") as f:
            self.manifest = json.load(f)

        # Optional: load labels
        self.target_key = target_key

    def __len__(self):
        return len(self.manifest)

    def __getitem__(self, idx):
        entry = self.manifest[idx]
        nifti_path = self.data_dir / "volumes" / entry["output_file"]

        # Load volume
        img = nib.load(str(nifti_path))
        volume = img.get_fdata().astype(np.float32)

        # Add channel dimension: (D, H, W) -> (1, D, H, W)
        volume = np.expand_dims(volume, axis=0)

        if self.transform:
            volume = self.transform(volume)

        sample = {
            "image": torch.from_numpy(volume),
            "subject_id": entry["subject_id"],
            "metadata": entry,
        }

        if self.target_key and self.target_key in entry:
            sample["label"] = entry[self.target_key]

        return sample


# Usage
dataset = MedicalImageDataset("/data/processed")
dataloader = torch.utils.data.DataLoader(
    dataset, batch_size=4, shuffle=True, num_workers=2,
)

for batch in dataloader:
    images = batch["image"]  # (B, 1, D, H, W)
    print(f"Batch shape: {images.shape}")
    break
```

---

## Gotchas

- **Series != Volume**: A DICOM study may contain multiple series (e.g., scout, axial, coronal, contrast phases). Each series is a separate volume. Always group by SeriesInstanceUID before building volumes.
- **Slice ordering matters**: Sort slices by `ImagePositionPatient[2]` or `InstanceNumber` before stacking into a volume. Unsorted slices produce garbled volumes.
- **Mixed series in one directory**: Clinical PACS exports often dump all series into a single flat directory. Group files by SeriesInstanceUID before processing.
- **Pixel spacing vs slice spacing**: `PixelSpacing` is in-plane (row, column). Slice spacing must be computed from `ImagePositionPatient` differences or `SpacingBetweenSlices` (less reliable).
- **RescaleSlope/Intercept**: CT images store raw detector values. Always apply `pixel * slope + intercept` to get Hounsfield units.
- **Variable image sizes**: Different studies may have different matrix sizes (512x512, 256x256, etc.). Resample or pad to a consistent size before batching.
- **Memory**: A single CT study can be 500MB+ in memory as float32. Process one study at a time and write to disk.
- **MONOCHROME1 vs MONOCHROME2**: MONOCHROME1 means "white = low values" (inverted). Flip before display or ML input.
- **Compressed transfer syntaxes**: Install `pylibjpeg` packages before processing JPEG-compressed DICOM files, or you'll get cryptic errors from `pixel_array`.

---

## Resources

- [SimpleITK Documentation](https://simpleitk.readthedocs.io/)
- [nibabel Documentation](https://nipy.org/nibabel/)
- [pydicom Pixel Data Guide](https://pydicom.github.io/pydicom/stable/guides/pixel_data/index.html)
- [MONAI (Medical Open Network for AI)](https://monai.io/) -- PyTorch framework for medical imaging ML
- [TorchIO](https://torchio.readthedocs.io/) -- Medical image transforms for PyTorch
- [Aurabox Research Suite](https://aurabox.cloud/products/research-suite) -- Automated de-identification and research data management
