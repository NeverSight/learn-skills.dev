---
name: ClaudeEEG
description: Expert EEG/MEG analysis, BCI development, and neuroscience signal processing — from raw recordings to production-grade models. Covers theory, preprocessing pipelines, ML/DL modeling, real-time classification, statistical analysis, and data ingestion.
trigger: TRIGGER when the user's request involves EEG, MEG, electrophysiology, brain-computer interfaces, ICA, ERPs, epochs, artifact removal, EEGLAB, MNE-Python, braindecode, neural decoding, oscillations, frequency bands, power spectral density, source localization, motor imagery, P300, SSVEP, neurofeedback, or any brain-data analysis task.
---

# ClaudeEEG

> A second brain for automated EEG analysis — from messy recordings to production-grade models.

---

## Overview

Load this skill whenever the user's request involves EEG data, neuroscience signal processing, BCI pipelines, or any brain-data analysis task. This document is structured as a _living reference_: read the relevant section(s) for each task and reason from first principles before generating code or recommendations. Always match the tool to the scientific question, not just user familiarity.

**Skill trigger keywords:** EEG, MEG, electrophysiology, brain-computer interface, BCI, ICA, ERP, epochs, artifact removal, EEGLAB, MNE, braindecode, NeuroPype, neural decoding, oscillations, frequency bands, power spectral density, source localization, motor imagery, P300, SSVEP, neurofeedback, neuro.

For detailed code examples, see the **/scripts** subfolder and for detailed documentation, see the **/references** subfolder.

---

## 1. EEG THEORY FOUNDATIONS

Understanding these principles is non-negotiable — they directly inform every preprocessing and modeling decision.

### 1.1 What EEG Actually Measures

EEG records the summed postsynaptic potentials of large pyramidal neuron populations in the neocortex, measured at the scalp surface. Key implications:

- **Volume conduction**: Signals are spatially smeared by the skull, scalp, and CSF before reaching electrodes. A source in one region appears spread across many channels. This is why raw channel signals cannot be naively treated as spatially independent.
- **Signal amplitude**: Typically 10–100 µV on the scalp. Amplitudes are inversely related to frequency — slow waves are larger, fast waves are smaller.
- **Temporal resolution**: Millisecond-precision, making EEG ideal for studying rapid neural dynamics (ERPs, oscillatory bursts). Spatial resolution, however, is poor (centimeter-scale at best).
- **EEG reflects network dynamics, not individual neuron activity.** Gamma oscillations (30–80 Hz), for example, can reflect synchronous firing across distributed populations — not just local activity.

### 1.2 Frequency Bands — Science, Not Just Labels

Frequency band boundaries vary in the literature (see Sapien Labs 2020 review on this inconsistency). Use these as biological priors, not hard cutoffs:

|Band|Range (common)|Functional correlates|Key caveats|
|---|---|---|---|
|**Delta**|0.5–4 Hz|Deep sleep, motivational processing, correlates with P300 dopamine reward; abnormal in awake adults|Highly susceptible to movement/EMG artifacts at low frequencies|
|**Theta**|4–8 Hz|Memory encoding (hippocampal), spatial navigation, working memory (theta-gamma coupling), emotional valence|Normal in drowsiness and children; theta-gamma nesting = ~4–7 items in working memory|
|**Alpha**|8–13 Hz|Inhibition of irrelevant cortical areas, relaxed wakefulness, attentional gating; posterior dominant rhythm (PDR) in healthy adults|Alpha suppression (ERD) occurs on eyes opening or task engagement; individual alpha frequency (IAF) varies and should be computed per-subject|
|**Beta**|13–30 Hz|Active thinking, motor planning, sensorimotor rhythm (SMR ~12–15 Hz); ERSP during motor execution|Heavily contaminated by muscle artifact, especially frontally|
|**Gamma**|30–80 Hz|Feature binding, perceptual integration, attentional focus, high-level cognition|Virtually impossible to isolate cleanly on scalp EEG without extreme care — muscle artifacts occupy 20–300 Hz and overlap gamma entirely|
|**High-gamma / HFO**|>80 Hz|Epileptic high-frequency oscillations; accessible mainly via intracranial EEG|Scalp gamma should be interpreted with extreme skepticism|

**Critical gamma warning:** The muscle artifact frequency range (20–300 Hz) fully overlaps gamma. Any gamma findings on scalp EEG without rigorous EMG rejection should be treated as artifact-contaminated. AMICA + ICLabel + manual inspection is the minimum bar.

**Band inconsistency:** Studies define "theta" with start points anywhere from 2.5–6.5 Hz. Always report your exact frequency windows. Never assume a paper's "theta" matches yours.

### 1.3 Cross-Frequency Coupling (CFC)

Nested oscillations are functionally meaningful, not just spectral curiosities:

- **Theta-gamma coupling**: Each theta cycle (~125 ms) contains ~4–7 gamma sub-cycles, each representing one item in working memory. This is the mechanistic basis for the 7±2 working memory limit.
- **Delta-theta coupling**: Delta phase organizes theta bursts — relevant in sleep and deep cognitive states.
- **Phase-Amplitude Coupling (PAC)**: The phase of a slow oscillation modulates the amplitude of a faster one. Measure with modulation index (MI) or mean vector length. MNE has `mne.connectivity` tools for this.
- **Beta-gamma PAC in basal ganglia**: Relevant in Parkinson's research and motor BCI.

### 1.4 Event-Related Potentials (ERPs) — Core Components

ERPs are voltage deflections time-locked to stimuli, extracted by trial averaging (which cancels non-phase-locked noise):

|Component|Latency|Scalp distribution|Cognitive correlate|
|---|---|---|---|
|N100 (N1)|~100 ms|Frontocentral|Sensory processing, auditory cortex activation|
|P200 (P2)|~200 ms|Frontocentral|Attentional modulation|
|N200 (N2)|~200 ms|Frontocentral|Conflict detection, inhibition (No-Go tasks)|
|P300 (P3b)|~300–600 ms|Parietal (Pz)|Context updating, target detection; core of P300-BCI|
|N400|~400 ms|Centro-parietal|Semantic incongruity|
|LRP|~150 ms before response|Contralateral motor|Lateralized readiness potential — motor planning|
|MMN|~150–250 ms|Frontocentral|Mismatch negativity — automatic deviance detection|

**Baseline correction** is essential: subtract mean voltage of a pre-stimulus window (typically –200 to 0 ms). This removes DC offsets. The choice of baseline period affects ERP shape significantly.

### 1.5 Event-Related Desynchronization/Synchronization (ERD/ERS)

Not phase-locked power changes around events:

- **ERD** (power decrease): Alpha/beta decrease during motor execution or preparation. Contralateral to the moved limb.
- **ERS** (power increase): Beta rebound post-movement — reflects cortical "idling."
- Measure with ERSP (event-related spectral perturbation) — time-frequency power relative to baseline.
- ERD/ERS are the core signals for **motor imagery BCI**.

### 1.6 Electrode Systems and Montages

- **10–20 system**: Standard 19-channel clinical montage. Channel names encode location (F=frontal, C=central, P=parietal, O=occipital, T=temporal; z=midline, odd=left, even=right).
- **10–10 and 10–5 systems**: Denser montages for high-density research EEG (64, 128, 256 channels).
- **Reference electrode matters enormously**: All EEG is a voltage difference between the active electrode and a reference. Common choices:
    - _Linked mastoids_ (A1+A2): Reduces ear artifacts but biases toward temporal signals.
    - _Average reference (CAR)_: Subtracts mean of all electrodes; good when channels cover full scalp, problematic with sparse montages or many bad channels.
    - _REST (Reference Electrode Standardization Technique)_: Approximates an "infinity" reference using a forward model; increasingly recommended for source analysis.
    - _Laplacian (CSD)_: Current source density — emphasizes local activity, reduces volume conduction. Ideal for high-density, spatially fine-grained analysis.

---

## 2. THE GOLD-STANDARD PREPROCESSING PIPELINE

Follow this order. Deviating from it requires scientific justification.

### Phase 0: Data Inspection and Documentation

Before touching the data:

1. Check sampling rate, number of channels, recording duration, event codes.
2. Visualize raw traces — look for dead channels, saturation, excessive drift.
3. Document electrode impedances if available (target <5 kΩ for gel, <50 kΩ for dry electrodes).
4. Record all parameters in a processing log (channel count, filter settings, epochs dropped).

```python
import mne
raw = mne.io.read_raw_fif('data.fif', preload=True)
print(raw.info)
raw.plot(duration=20, n_channels=32)
raw.compute_psd(fmax=80).plot()
```

### Phase 1: Channel-Level Cleaning

**Step 1.1 — Bad channel identification and removal**

Bad channels exhibit: flat signal, excessive noise (high-frequency bursts), >4 SD deviation from mean channel power. Mark before any filtering.

```python
# MNE approach
from mne.preprocessing import find_bad_channels_maxwell
# Or manual:
raw.info['bads'] = ['Fp1', 'AF7']  # flagged visually or algorithmically

# EEGLAB equivalent: pop_rejchan() with kurtosis/probability threshold
```

**Step 1.2 — Line noise removal**

Choose based on context:

- **Notch filter (50 or 60 Hz)**: Simple, but introduces ringing and distorts nearby frequencies. Avoid if analysis is near 50/60 Hz.
- **Zapline / DSS-based methods**: Preferred. Removes line noise without spectral distortion using data-driven denoising source separation. Available via `meegkit` in Python.
- **Frequency-domain interpolation**: Alternative for stationary line noise.

```python
# Notch (use cautiously)
raw.notch_filter(freqs=[50, 100])

# Zapline via meegkit (preferred for high-quality data)
from meegkit import dss
```

### Phase 2: Filtering

**Critical rule:** Filter _before_ epoching to avoid edge artifacts in epochs. But fit ICA on _filtered_ data and apply to _minimally filtered_ data (see below).

**High-pass filter (drift removal)**

- Standard: 0.5–1 Hz for most analyses.
- ERP analyses requiring slow components (P300 body, CNV): use 0.1 Hz.
- For ICA fitting: use 1–2 Hz (ICA decomposition quality degrades with slow drift).
- **Do not use 0.1 Hz for ICA** — this is the "dual dataset" trick.

**Low-pass filter**

- Anti-aliasing: always apply at half the Nyquist frequency before downsampling.
- Analysis-specific: 40 Hz suffices for ERP; 100+ Hz for gamma/HFO.

**Filter type matters:**

- **FIR (recommended)**: Linear phase, predictable response. Use Hamming windowed sinc (MNE default). Specify length explicitly — longer = sharper rolloff = more temporal smearing.
- **IIR**: Faster, but introduces phase distortion. Avoid for ERP timing analyses; acceptable for online/real-time.

```python
# MNE FIR filtering
raw.filter(l_freq=1.0, h_freq=40.0, method='fir', fir_window='hamming')

# For ICA fitting dataset (keep separate from analysis dataset):
raw_for_ica = raw.copy().filter(1.0, 40.0)
```

### Phase 3: Downsampling

Always apply low-pass filter _first_, then downsample. Target: 2–4× your highest frequency of interest. 256 Hz is standard for ERP; 512 Hz for gamma.

```python
raw.resample(sfreq=256)
```

### Phase 4: Re-referencing

Do this _after_ bad channel removal and _before_ ICA:

```python
# Average reference
raw.set_eeg_reference('average', projection=True)

# REST reference (requires forward model)
# mne.set_eeg_reference(raw, 'REST', ...)
```

### Phase 5: Artifact Removal — The Core Challenge

This is where most analysis quality is won or lost.

#### 5.1 Artifact Source Separator (ASR) — For High-Motion Data

Artifact Subspace Reconstruction removes large transient artifacts (head movements, electrode pops) _before_ ICA. Use when:

- Mobile EEG / naturalistic paradigms.
- Moderate-to-high motion artifacts.
- Running EEGLAB pipelines.

Evidence: ASR before ICA (ASRICA) outperforms ICA alone or ASR after ICA for mobile EEG. The 2024 "skateboarding" study (Callan et al., Frontiers Neuroergonomics) demonstrates this definitively.

ASR is available in EEGLAB as `clean_rawdata`. In Python, use `mne_icalabel` ecosystem or `pyasr`.

#### 5.2 ICA — The Core Tool

ICA decomposes multi-channel EEG into statistically independent components (ICs). Artifacts (eye blinks, heartbeat, muscle) are typically captured in a small number of ICs, which can be removed.

**Fundamental requirements:**

- Data must be filtered ≥1 Hz before ICA.
- Remove gross artifacts (ASR or manual rejection) _before_ ICA — noisy samples degrade decomposition.
- Sufficient data: aim for ≥20 × n_channels² samples.
- Number of ICs ≤ rank of data (typically n_channels after bad channel interpolation).

**Dual-dataset approach (canonical best practice):**

1. Create Dataset A: high-pass at 1–2 Hz, clean of gross artifacts → fit ICA here.
2. Create Dataset B: high-pass at 0.1 Hz (preserves slow components) → apply ICA weights from A. This preserves slow ERPs while benefiting from clean ICA decomposition.

```python
# MNE ICA pipeline
from mne.preprocessing import ICA

ica = ICA(n_components=25, method='infomax', fit_params={'extended': True}, random_state=42)
ica.fit(raw_for_ica)

# Auto-label components
from mne_icalabel import label_components
ic_labels = label_components(raw_for_ica, ica, method='iclabel')

# Exclude non-brain components automatically
exclude_idx = [i for i, label in enumerate(ic_labels['labels'])
               if label not in ['brain', 'other'] and ic_labels['y_pred_proba'][i] > 0.8]
ica.exclude = exclude_idx
ica.apply(raw)  # apply to analysis dataset
```

**ICA algorithms:**

- **Extended Infomax** (MNE default): Handles both sub- and super-Gaussian sources. Reliable.
- **FastICA**: Fast, good for quick exploration.
- **AMICA**: Best decomposition quality, especially for mobile EEG. Slower. EEGLAB/standalone.
- **SOBI**: Second-order statistics; handles non-stationary data well.

**IC classification tools:**

- **ICLabel** (EEGLAB + MNE): CNN trained on thousands of manually labeled ICs. Classifies: brain, eye, muscle, heart, channel noise, line noise, other. Use 'lite' variant for muscle ICs.
- **MARA** (EEGLAB): Linear discriminant classifier, older but still used.
- **AutoReject** (MNE): Epoch-level rejection, not IC-level — complementary.

**Manual IC inspection checklist:**

- Topographic map: focal scalp distribution = brain; bilateral frontal = eye; lateral temporal = muscle; single channel = noise.
- Time course: periodic = heartbeat (ICA001 often); square waves = eye; high-freq bursts = muscle.
- Power spectrum: 1/f slope = brain; flat/high-freq = muscle; 60 Hz peak = line noise.

**Important 2024 finding:** For deep learning decoders, ICA artifact removal may not improve (and sometimes hurts) classification performance compared to raw data (Kang et al., J. Neural Eng. 2024). This does not apply to ERP or spectral analyses where SNR is the bottleneck. Adjust your pipeline based on the downstream task.

#### 5.3 Epoch-Level Artifact Rejection

After ICA, remaining artifacts in individual epochs should be rejected:

```python
from autoreject import AutoReject
ar = AutoReject(random_state=42)
epochs_clean, reject_log = ar.fit_transform(epochs, return_log=True)
```

Or threshold-based:

```python
reject = dict(eeg=150e-6)  # 150 µV threshold
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, reject=reject)
```

### Phase 6: Epoching

```python
events, event_id = mne.events_from_annotations(raw)
epochs = mne.Epochs(raw, events, event_id={'target': 1, 'nontarget': 2},
                    tmin=-0.2, tmax=0.8,
                    baseline=(-0.2, 0),  # pre-stimulus baseline
                    preload=True)
```

**Baseline correction:** Always use a pre-stimulus window. The baseline period should not contain the stimulus response. For very slow components, longer baselines introduce regression-to-mean artifacts.

### Phase 7: Bad Channel Interpolation

Interpolate bad channels _after_ the rest of preprocessing but _before_ re-referencing or group analysis. Use spherical spline interpolation:

```python
raw.interpolate_bads(reset_bads=True)
```

---

## 3. LIBRARY REFERENCE GUIDE

### 3.1 MNE-Python — The Python Standard

**When to use:** Any Python-based EEG/MEG pipeline. Best-in-class for preprocessing, ERP, time-frequency, and source localization.

**Core objects:**

- `Raw`: Continuous data. `raw.get_data()` returns (n_channels, n_times) array.
- `Epochs`: Event-locked segmented data. Shape: (n_epochs, n_channels, n_times).
- `Evoked`: Averaged epochs. Shape: (n_channels, n_times).
- `Info`: Metadata dict — sampling rate, channel names, montage.

**Key submodules:**

```
mne.io              # reading raw data (EDF, BrainVision, EDF+, FIF, SET, CNT, etc.)
mne.preprocessing   # ICA, SSP, filtering, Maxwell filtering
mne.epochs          # Epochs class
mne.time_frequency  # Morlet TFR, multitaper PSD, Hilbert
mne.connectivity    # coherence, PLV, WPLI
mne.beamformer      # LCMV, DICS source localization
mne.minimum_norm    # MNE, dSPM, sLORETA inverse solutions
mne.stats           # permutation cluster tests, FDR correction
mne.viz             # topomap, raw browser, evoked plots
```

**Common pitfalls:**

- `preload=True` required before most in-place operations.
- `events` array must be (n_events, 3) with columns [sample, prev_event_value, event_id].
- `apply_proj()` must be called explicitly after `set_eeg_reference('average', projection=True)`.
- Filtering order: filter → downsample → epoch, not epoch → filter.

**Reading various formats:**

```python
mne.io.read_raw_edf('file.edf')       # EDF/EDF+
mne.io.read_raw_brainvision('file.vhdr')  # BrainVision
mne.io.read_raw_eeglab('file.set')   # EEGLAB .set
mne.io.read_raw_cnt('file.cnt')      # Neuroscan
mne.io.read_raw_egi('file.mff')      # EGI/Geodesic
```

### 3.2 EEGLAB — The MATLAB Reference Standard

**When to use:** MATLAB environments, legacy pipelines, AMICA ICA, STUDY group analysis, ICLabel, LIMO statistics. Many published pipelines remain EEGLAB-based.

**Core pipeline in EEGLAB:**

```matlab
% Load
EEG = pop_loadset('filename.set');
EEG = eeg_checkset(EEG);

% Channel locations
EEG = pop_chanedit(EEG, 'lookup', 'standard-10-5-cap385.elp');

% Remove bad channels (threshold + correlation methods)
EEG = pop_rejchan(EEG, 'elec', 1:EEG.nbchan, 'threshold', 5, 'measure', 'kurt');

% Filter
EEG = pop_eegfiltnew(EEG, 'locutoff', 1, 'hicutoff', 40);

% Artifact Subspace Reconstruction (clean_rawdata plugin)
EEG = clean_rawdata(EEG, 5, [0.25 0.75], 0.85, 4, 20, 0.25);

% ICA (Extended Infomax)
EEG = pop_runica(EEG, 'icatype', 'runica', 'extended', 1);

% ICLabel auto-reject
EEG = pop_iclabel(EEG, 'default');
EEG = pop_icflag(EEG, [NaN NaN; 0.9 1; 0.9 1; NaN NaN; NaN NaN; NaN NaN; NaN NaN]);
EEG = pop_subcomp(EEG, [], 0);

% Epoch
EEG = pop_epoch(EEG, {'target'}, [-0.2 0.8]);
EEG = pop_rmbase(EEG, [-200 0]);
```

**EEGLAB plugins worth knowing:**

- `clean_rawdata`: ASR-based cleaning.
- `ICLabel`: IC classification.
- `LIMO EEG`: Linear models for EEG (hierarchical models across subjects).
- `ERPLAB`: ERP-specific tools.
- `DIPFIT`: Dipole fitting for ICA source localization.
- `AMICA`: Multi-model ICA, highest quality decomposition.

### 3.3 SciPy — Signal Processing Backbone

SciPy's `signal` submodule underpins much of what MNE/EEGLAB wrap. Know this for custom work:

```python
from scipy import signal

# Bandpass filter (IIR — use with caution for phase-sensitive analysis)
b, a = signal.butter(4, [8, 13], btype='bandpass', fs=256)
filtered = signal.filtfilt(b, a, data)  # zero-phase via filtfilt

# Power spectral density
freqs, psd = signal.welch(data, fs=256, nperseg=256*2)

# Short-time Fourier transform
freqs, times, Sxx = signal.spectrogram(data, fs=256, nperseg=256)

# Hilbert transform (analytic signal for instantaneous phase/amplitude)
analytic = signal.hilbert(filtered_data)
instantaneous_amplitude = np.abs(analytic)
instantaneous_phase = np.angle(analytic)

# Coherence
freqs, coh = signal.coherence(x, y, fs=256, nperseg=256)
```

**Key SciPy functions for EEG:**

|Function|Use case|
|---|---|
|`signal.butter` / `signal.sosfilt`|IIR bandpass/notch filtering|
|`signal.firwin`|FIR filter design|
|`signal.welch`|Stable PSD via Welch method|
|`signal.spectrogram`|Time-frequency (STFT)|
|`signal.hilbert`|Instantaneous amplitude/phase|
|`signal.coherence`|Linear frequency-domain connectivity|
|`signal.find_peaks`|Peak detection in ERP/PSD|
|`stats.ttest_rel`, `stats.wilcoxon`|Group-level stats|
|`stats.spearmanr`, `stats.pearsonr`|Correlation of EEG features with behavior|

### 3.4 Scikit-learn — Machine Learning for EEG

**When to use:** Feature-based classification (SVM, LDA, random forests), cross-validation, hyperparameter tuning, dimensionality reduction. The bridge between EEG features and traditional ML.

**Standard EEG classification pipeline:**

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import StratifiedKFold, cross_val_score
from mne.decoding import CSP, Vectorizer

# Common Spatial Patterns (CSP) for motor imagery
pipeline = Pipeline([
    ('csp', CSP(n_components=6, log=True)),
    ('scaler', StandardScaler()),
    ('clf', LinearDiscriminantAnalysis())
])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipeline, X, y, cv=cv, scoring='accuracy')
print(f"Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
```

**EEG-specific sklearn wrappers in MNE:**

```python
from mne.decoding import (
    CSP,           # Common Spatial Patterns (motor imagery)
    SPoC,          # Source Power Comodulation (regression)
    Vectorizer,    # Epoch to feature vector
    UnsupervisedSpatialFilter,  # PCA/ICA on epochs
    GeneralizingEstimator,      # Temporal generalization
    SlidingEstimator,           # Decoding at each time point
)
```

**Cross-validation rules for EEG (critical):**

- Always use **subject-stratified** splits when training on one subject.
- For cross-subject generalization: leave-one-subject-out (LOSO) CV.
- **Never mix train/test data across the temporal boundary** — EEG data is autocorrelated, so random splits inflate accuracy.
- Use `StratifiedKFold` not `KFold` when classes are imbalanced.
- Report both within-session and cross-session performance.

**Common features for EEG ML:**

```python
# Band power features (most common baseline)
from mne.time_frequency import psd_welch
psds, freqs = psd_welch(epochs, fmin=1, fmax=40, n_fft=256)
# Select band: e.g., alpha (8-13 Hz)
alpha_mask = (freqs >= 8) & (freqs <= 13)
alpha_power = psds[:, :, alpha_mask].mean(axis=-1)  # shape: (n_epochs, n_channels)

# Covariance matrices (for Riemannian geometry methods — pyRiemann)
from pyriemann.estimation import Covariances
from pyriemann.classification import MDM
cov = Covariances(estimator='lwf').fit_transform(X)  # X: (n_epochs, n_channels, n_times)
```

**Riemannian geometry methods** (pyRiemann library) — increasingly the state-of-the-art for EEG classification, especially motor imagery:

```python
from pyriemann.classification import MDM  # Minimum Distance to Mean
from pyriemann.tangentspace import TangentSpace
# Better than CSP+LDA for cross-subject generalization
```

### 3.5 Braindecode — Deep Learning for EEG

**When to use:** When you need end-to-end deep learning on raw EEG; motor imagery, sleep staging, seizure detection, BCI decoding with large datasets.

**Installation:**

```
pip install braindecode
```

**Key architectures available:**

|Model|Architecture|Best for|
|---|---|---|
|`EEGNet`|Compact depthwise separable CNN|Low-data, BCI, general decoding|
|`ShallowConvNet`|Shallow bandpower CNN|Motor imagery, interpretable|
|`DeepConvNet`|Deeper residual CNN|Large datasets|
|`EEGSimpleConv`|Minimal 1D CNN|Fast inference, motor imagery|
|`ATCNet`|Attention-CNN|Temporal attention|
|`Labram`|ViT-based Foundation Model|Transfer learning, cross-dataset|
|`BIOT`|Contrastive Foundation Model|Multi-modal biosignals|
|`SignalJEPA`|JEPA self-supervised|Cross-dataset transfer|

**Basic braindecode pipeline:**

```python
from braindecode.datasets import MOABBDataset
from braindecode.preprocessing import preprocess, Preprocessor, create_windows_from_events
from braindecode.models import EEGNet
from braindecode.training import CroppedLoss
import torch
from torch import nn

# Load MOABB dataset
dataset = MOABBDataset(dataset_name='BNCI2014001', subject_ids=[1])

# Preprocess
preprocessors = [
    Preprocessor('pick_types', eeg=True, meg=False, stim=False),
    Preprocessor(lambda data, factor: np.multiply(data, factor), factor=1e6),  # V -> µV
    Preprocessor('filter', l_freq=4., h_freq=38.),
    Preprocessor('resample', sfreq=250)
]
preprocess(dataset, preprocessors)

# Create windows
windows_dataset = create_windows_from_events(
    dataset, trial_start_offset_samples=0, trial_stop_offset_samples=0,
    preload=True)

# Model
model = EEGNet(
    n_chans=22,
    n_outputs=4,
    n_times=1000,
    F1=8, D=2, F2=16,
    kernel_length=64,
    drop_prob=0.5
)

# Training uses braindecode's EEGClassifier (sklearn-compatible)
from braindecode import EEGClassifier
from skorch.callbacks import EarlyStopping, LRScheduler

clf = EEGClassifier(
    model,
    criterion=nn.CrossEntropyLoss,
    optimizer=torch.optim.Adam,
    train_split=None,
    optimizer__lr=0.001,
    batch_size=64,
    max_epochs=100,
    callbacks=['accuracy', EarlyStopping(patience=10)]
)
clf.fit(windows_dataset, y=None)
```

**Loading Foundation Models from HuggingFace:**

```python
from braindecode.models import Labram

# Load pretrained Labram (Large Brain Model)
model = Labram.from_pretrained("braindecode/Labram-Braindecode")
# Fine-tune by replacing classification head
model.head = nn.Linear(model.head.in_features, n_classes)
```

**Foundation models currently in braindecode:**

- **Labram** (LaBraM, ICLR 2024): Transformer trained on massive EEG datasets. Neural tokenizer + decoder modes. Best for transfer when labeled data is scarce.
- **BIOT**: Contrastive biosignal foundation model, handles EEG/ECG/others. Trained on TUH Abnormal (400K samples) + Sleep Heart Health Study (5M samples).
- **SignalJEPA**: JEPA-based cross-dataset transfer, attention over channels.

**Braindecode data augmentation:**

```python
from braindecode.augmentation import (
    SignFlip,      # Randomly flip amplitude signs
    FTSurrogate,   # Frequency-transform surrogate
    ChannelsDropout, # Zero out random channels
    GaussianNoise, # Add noise
    SmoothTimeMask, # Mask time windows
)
```

### 3.6 NeuroPype — Real-Time and Deployment Pipelines

Two distinct tools share this name — clarify with the user which they mean:

**NeuroPype (Intheon/Syntrogi) — Commercial real-time platform:**

- Visual pipeline designer connecting processing "nodes."
- Interfaces with Lab Streaming Layer (LSL) for hardware-agnostic real-time streaming.
- Hundreds of nodes: filtering, artifact removal, spectral analysis, connectivity, ML classification, neurofeedback.
- Deep learning support (EEGNet etc.) as of 2023 release.
- Deploy to NeuroScale cloud API.
- Use for: closed-loop neurofeedback, real-time BCI, production deployment, multi-device streaming.

**NeuroPype (Pasca et al., open-source academic) — Python connectivity pipeline:**

- Built on Nipype + MNE-Python.
- Focus: multi-thread MEG/EEG connectivity analysis (PLI, coherence, graph theory metrics).
- GitHub: `annapasca/neuropype`.
- Use for: batch source-level connectivity analyses, graph theory, academic research pipelines.

---

## 4. STATISTICAL ANALYSIS REFERENCE

### 4.1 What Statistical Test for What EEG Question

|Question|Test|Tool|
|---|---|---|
|Are two ERP conditions different at a time point?|Paired t-test (parametric) or Wilcoxon (non-parametric)|`scipy.stats`, `mne.stats`|
|Are ERPs different across whole epoch (mass univariate)?|Cluster permutation test|`mne.stats.permutation_cluster_test`|
|Is band power different across 2+ conditions?|Repeated-measures ANOVA (log-transform power first)|`pingouin`, `scipy.stats`|
|Does a feature predict behavior?|Pearson/Spearman r, linear regression|`scipy.stats`, `sklearn`|
|Cross-subject: is decoding > chance?|One-sample t-test vs. 0.5, permutation test|`mne.stats`|
|Multiple comparisons over channels × time?|Cluster permutation or FDR/Bonferroni correction|`mne.stats.fdr_correction`|
|Complex multi-factor design?|GLM / LIMO (Linear Model EEG)|EEGLAB LIMO plugin, `pingouin`|

**Critical:** Always **log-transform spectral power** before parametric tests (PSD is approximately log-normally distributed).

### 4.2 Cluster Permutation Testing — The EEG Standard

This is the recommended approach for mass univariate testing across channels × time (or channels × frequency × time) because it controls familywise error rate without sacrificing as much power as strict Bonferroni:

```python
import mne

# Compare two conditions across subjects
T_obs, clusters, cluster_p_values, H0 = mne.stats.permutation_cluster_test(
    [condition1_data, condition2_data],
    n_permutations=1000,
    threshold=None,  # uses F-distribution threshold
    tail=0,
    n_jobs=4,
    seed=42
)

# Significant clusters
good_clusters = [c for c, p in zip(clusters, cluster_p_values) if p < 0.05]
```

### 4.3 ERP Analysis Best Practices

```python
# ERP computation
evoked_target = epochs['target'].average()
evoked_nontarget = epochs['nontarget'].average()

# Difference wave
diff = mne.combine_evoked([evoked_target, evoked_nontarget], weights=[1, -1])

# Component quantification: mean amplitude in time window
times = evoked_target.times
p300_window = (times >= 0.3) & (times <= 0.5)
p300_amplitude = evoked_target.data[:, p300_window].mean(axis=1)  # per channel

# Peak latency
peak_time = times[evoked_target.data[channel_idx, :].argmax()]
```

**ERP pitfalls to avoid:**

- Baseline period overlapping with stimulus effects.
- Insufficient trials for stable average (target ≥30 trials per condition, ideally ≥60).
- Not accounting for individual differences in peak latency (latency jitter smears group ERPs).
- Cherry-picking channels post-hoc — define ROIs a priori.

### 4.4 Spectral Analysis

```python
# Welch PSD on epochs
from mne.time_frequency import psd_array_welch

psds, freqs = psd_array_welch(
    epochs.get_data(),
    sfreq=epochs.info['sfreq'],
    fmin=1, fmax=40,
    n_fft=int(epochs.info['sfreq'] * 2),  # 2-second windows
    n_overlap=int(epochs.info['sfreq']),   # 50% overlap
    window='hamming'
)

# Morlet wavelets for time-frequency (better temporal resolution)
from mne.time_frequency import tfr_morlet

freqs = np.logspace(np.log10(4), np.log10(40), 30)
n_cycles = freqs / 2.0  # frequency-adaptive cycles
power = tfr_morlet(epochs, freqs=freqs, n_cycles=n_cycles,
                   decim=3, return_itc=True, average=True)
power.plot(['C3'], baseline=(-0.2, 0), mode='logratio')
```

**Time-frequency tradeoff:** More frequency resolution → less temporal resolution. Morlet wavelets with frequency-adaptive `n_cycles` (commonly freqs/2) balance this. Multitaper methods (DPSS) give more stable spectral estimates at the cost of temporal precision.

### 4.5 Connectivity Analysis

Functional connectivity in EEG comes with a major confound: **volume conduction**. Two electrodes can show high coherence purely because they're picking up the same source, not because the regions are connected. Use imaginary-part-based metrics to mitigate this:

|Metric|Robust to volume conduction?|Notes|
|---|---|---|
|Pearson correlation|No|Most inflated|
|Coherence|No|Volume conduction creates spurious coherence|
|Imaginary Coherence|Yes|Uses only the imaginary part of cross-spectrum|
|PLV (Phase Locking Value)|No|Inflated by shared source|
|wPLI (weighted PLI)|Yes|Recommended for scalp EEG|
|Granger Causality|Partially|Directional; assumes linearity|
|Transfer Entropy|Yes|Non-linear; requires much data|

```python
from mne_connectivity import spectral_connectivity_epochs

# Compute wPLI connectivity
conn = spectral_connectivity_epochs(
    epochs, method='wpli', mode='fourier',
    fmin=8, fmax=13, faverage=True
)
```

---

## 5. VISUALIZATION REFERENCE

### 5.1 Standard EEG Visualizations

```python
# Raw signal browser
raw.plot(duration=10, n_channels=32, scalings='auto')

# PSD
raw.compute_psd(fmax=60).plot()

# Topomap (spatial distribution)
evoked.plot_topomap(times=[0.1, 0.2, 0.3, 0.4], ch_type='eeg')

# ERP butterfly plot
evoked.plot(spatial_colors=True, time_unit='ms')

# Joint plot (waveform + topomaps)
evoked.plot_joint(picks='eeg')

# ICA component properties
ica.plot_components()
ica.plot_properties(raw, picks=[0, 1, 2])

# Time-frequency
power.plot_topo(baseline=(-0.5, 0), mode='logratio')
power.plot_joint(baseline=(-0.5, 0), mode='mean')

# Epochs image (trial × time)
epochs.plot_image(picks=['Cz'])
```

### 5.2 Publication-Quality Figures with MNE + Matplotlib

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# ERP with confidence interval (standard error across subjects)
mne.viz.plot_compare_evokeds(
    {'Target': evoked_list_target, 'Non-target': evoked_list_nontarget},
    picks='Pz',
    ci=True,  # bootstrapped confidence intervals
    axes=axes[0]
)

# Topomap at P300 peak
evoked_target.plot_topomap(times=0.4, axes=axes[1], show=False)
plt.tight_layout()
plt.savefig('erp_results.pdf', dpi=300, bbox_inches='tight')
```

### 5.3 Source Space Visualization

```python
# Source estimate on fsaverage brain
stc = mne.minimum_norm.apply_inverse(evoked, inverse_operator, lambda2=1./9., method='dSPM')
brain = stc.plot(subject='fsaverage', hemi='both', subjects_dir=subjects_dir,
                 time_viewer=True, colormap='hot')
```

---

## 6. TASK-SPECIFIC PIPELINES

### 6.1 Motor Imagery BCI

Key signals: contralateral alpha/beta ERD (8–13 Hz, 13–30 Hz) at C3/C4.

```
Raw → Filter (1–40 Hz) → ASR → ICA → Epoch (3–6 s windows)
→ CSP → LDA/SVM   [classical]
   OR
→ EEGNet / ShallowConvNet  [end-to-end DL]
   OR
→ Covariance → Riemannian MDM  [geometry-based, best cross-subject]
```

**Dataset:** BCI Competition IV 2a/2b (BNCI2014001/BNCI2014002 in MOABB). Use MOABB for standardized benchmarking.

### 6.2 P300 / ERP-Based BCI

Key signal: P300 at 300–600 ms, maximal at Pz, elicited by rare targets.

```
Raw → Filter (0.1–30 Hz) → ICA → Epoch (−200 to 800 ms) → Baseline
→ LDA on downsampled epoch  [Farwell & Donchin classic]
   OR
→ xDAWN spatial filter → LDA  [better SNR]
   OR
→ EEGNet / DeepConvNet  [end-to-end]
```

### 6.3 SSVEP BCI

Key signal: steady-state response at stimulus frequency and harmonics, over occipital channels (Oz, O1, O2).

```
Raw → Notch → Bandpass around target freqs → Epoch (1–4 s)
→ FFT → Peak at stimulus frequency → CCA or TRCA detection
```

### 6.4 Sleep Stage Classification

```
Raw (EOG + EEG + EMG) → Filter (0.3–35 Hz) → 30-second epochs
→ Feature extraction (delta power, spindle detection, EMG amplitude)
→ Random Forest / LSTM / U-Time DL model
→ AASM staging (W/N1/N2/N3/REM)
```

**Key channels:** C3-M2 / C4-M1 for EEG; ROC-A1 / LOC-A2 for EOG.

### 6.5 Epilepsy Seizure Detection

```
Continuous EEG → Sliding window (2–10 s, 50% overlap)
→ Filter (1–70 Hz) → Line noise removal
→ Features: spike rate, HFO count, entropy, band power ratios
→ Binary classifier (SVM/Random Forest/CNN)
→ Post-processing: reject isolated detections, merge neighboring windows
```

**Important:** Clinical EEG for epilepsy requires 10–20 system montage, and annotations by certified epileptologists for ground truth. Do not deploy without clinical validation.

### 6.6 Resting-State EEG / Connectivity

```
Raw → Filter (1–45 Hz) → ICA → Re-reference (average or REST) → 2-minute clean segments
→ Source localization (beamformer / MNE inverse)
→ Source-level connectivity (wPLI, imaginary coherence)
→ Graph theory metrics (clustering coefficient, path length, modularity)
```

---

## 7. CROSS-SUBJECT GENERALIZATION AND TRANSFER LEARNING

This is the central challenge in EEG-based ML: models trained on one subject almost always perform poorly on others due to non-stationarity and inter-individual variability.

**Strategies (in order of increasing sophistication):**

1. **Baseline correction and normalization**: Log-transform PSD, z-score features per subject. Reduces individual mean shifts.
    
2. **Domain adaptation**: Align covariance matrices across subjects in Riemannian space (Euclidean Alignment, pyRiemann's `RPA`).
    
3. **Leave-one-subject-out (LOSO) CV**: The honest cross-subject evaluation metric. If you don't do this, your "generalizable" model is overfit.
    
4. **Foundation model fine-tuning**: Use Labram or BIOT as feature extractors; fine-tune only the head on target subject. Requires very little per-subject data.
    
5. **MOABB benchmarking**: Use the Mother of All BCI Benchmarks to compare your approach against published results on standardized datasets.
    

```python
import moabb
from moabb.datasets import BNCI2014001
from moabb.paradigms import MotorImagery
from moabb.evaluations import CrossSessionEvaluation
from moabb.pipelines import make_pipeline

dataset = BNCI2014001()
paradigm = MotorImagery()
evaluation = CrossSessionEvaluation(paradigm=paradigm, datasets=[dataset])
results = evaluation.process({'my_pipeline': pipeline})
```

---

## 8. COMMON MISTAKES AND HOW TO AVOID THEM

|Mistake|Consequence|Fix|
|---|---|---|
|Filtering after epoching|Edge artifacts in epochs|Filter continuous data first|
|Using 0.1 Hz HP for ICA|Slow drift degrades ICA|Use 1 Hz for ICA fitting; apply to 0.1 Hz dataset|
|Ignoring volume conduction in connectivity|Spurious coherence|Use wPLI, imaginary coherence|
|Gamma as brain signal without careful cleaning|Reporting muscle artifact as cognition|AMICA + ICLabel + manual inspection|
|Random CV splits on EEG|Autocorrelation inflates accuracy|Use trial-stratified, time-ordered splits|
|Averaging epochs without rejection|Artifacts dominate|Always inspect/reject bad epochs|
|Not log-transforming power before t-tests|Violated normality|log10(power) before stats|
|Ignoring individual alpha frequency (IAF)|Misclassifying alpha/beta|Compute per-subject IAF from resting-state PSD|
|Not matching sampling rates across subjects|Pipeline failure|Resample to common sfreq before group analysis|
|p-hacking across all channels/times/frequencies|False positives|Pre-register ROIs; use cluster permutation tests|

---

## 9. DATA FORMAT REFERENCE

|Format|Extension|Read with|
|---|---|---|
|EDF / EDF+|`.edf`|`mne.io.read_raw_edf`|
|BrainVision|`.vhdr/.vmrk/.eeg`|`mne.io.read_raw_brainvision`|
|EEGLAB|`.set/.fdt`|`mne.io.read_raw_eeglab`|
|Neuroscan|`.cnt`|`mne.io.read_raw_cnt`|
|EGI/Geodesic|`.mff/.raw`|`mne.io.read_raw_egi`|
|MNE native|`.fif`|`mne.io.read_raw_fif`|
|HDF5 (braindecode)|`.h5`|`braindecode` dataset loaders|
|BIDS|directory|`mne_bids.read_raw_bids`|

**BIDS for EEG:** Use `mne-bids` to convert to Brain Imaging Data Structure. Required for reproducible, shareable research pipelines.

---

## 10. ENVIRONMENT SETUP

```bash
# Core EEG Python stack
pip install mne mne-icalabel autoreject braindecode pyriemann moabb mne-connectivity mne-bids

# Signal processing
pip install scipy numpy matplotlib seaborn

# ML
pip install scikit-learn torch torchvision

# Optional but recommended
pip install meegkit        # Zapline, ASR, DSS denoising
pip install antropy        # Entropy measures (sample entropy, permutation entropy)
pip install pywavelets     # Wavelet transforms
pip install fooof           # Fitting oscillations & one over f (parameterize PSD)
pip install pingouin       # Clean stats API
```

**Recommended FOOOF for PSD parameterization:**

```python
from fooof import FOOOF

fm = FOOOF(peak_width_limits=[1, 6], aperiodic_mode='fixed')
fm.fit(freqs, psd_1d, freq_range=[1, 40])
# Separates aperiodic (1/f) component from oscillatory peaks
# Much better than raw band power for cross-subject comparison
```

---

## 11. QUICK DECISION TREE

```
User asks about EEG →
  ├── "preprocess / clean data"
  │     → Apply Phase 0–7 pipeline (Section 2)
  │     → Match filter settings to analysis type
  │     → Use ASR if mobile; use dual-dataset ICA always
  │
  ├── "classify / decode / BCI"
  │     → Check dataset size:
  │         < 500 trials: CSP+LDA or Riemannian MDM
  │         500–5000: EEGNet or ShallowConvNet
  │         > 5000 or cross-subject: Labram fine-tuning or BIOT
  │     → Use MOABB for benchmarking
  │     → Use LOSO CV for cross-subject
  │
  ├── "ERP analysis"
  │     → Section 4.3: define time windows a priori
  │     → Use cluster permutation tests for mass univariate
  │     → Minimum 30 trials per condition
  │
  ├── "spectral / oscillations"
  │     → Use FOOOF to separate 1/f from oscillations
  │     → Log-transform before stats
  │     → Define bands with IAF where possible
  │
  ├── "connectivity"
  │     → Use wPLI or imaginary coherence (volume conduction!)
  │     → Source-level > sensor-level connectivity
  │
  ├── "real-time / neurofeedback"
  │     → NeuroPype (Intheon) + LSL
  │     → IIR filters acceptable for real-time
  │
  └── "foundation models / transfer learning"
        → Braindecode: Labram, BIOT, SignalJEPA
        → Load from HuggingFace Hub
        → Replace head; fine-tune on target data
```

---

## 12. ML/DL MODELING — ADVANCED GUIDE FOR EEG

This section covers everything Claude needs to reason correctly about machine learning and deep learning for EEG, with special depth on **continuous/real-time inference** (seizure detection, state recognition, speech decoding) — the class of problems where Claude historically makes the most errors.

---

### 12.1 The Core Mental Model: Offline vs. Online vs. Real-Time

Before writing a single line of model code, classify the problem:

|Mode|Definition|Key constraints|Typical use cases|
|---|---|---|---|
|**Offline batch**|All data available; train and evaluate after collection|No latency; can use full context (bidirectional)|Research ERP studies, sleep staging from recordings|
|**Online (pseudo-real-time)**|Data arrives in chunks; inference runs on each chunk|Low-but-flexible latency; no future data|Neurofeedback sessions, post-hoc BCI decoding|
|**Strict real-time**|Continuous stream; must classify within a hard latency budget|**Causal only** — absolutely no future data; inference must finish before next window arrives|Seizure alarms, BCI device control, speech decoding|

**The single most common Claude error:** Using bidirectional architectures (BiLSTM, full attention over the whole sequence, acausal filters) in a system described as "real-time." These models look at _future samples to classify current ones_ — they cannot run in real-time. Always match architecture to mode.

---

### 12.2 The Sliding Window — Foundation of Continuous EEG Inference

All continuous EEG ML systems revolve around sliding windows. Get this right before anything else.

**Window parameters and their implications:**

```
window_size_sec = 2.0        # How much signal to classify at once
step_size_sec   = 0.5        # How often a new decision is made (= latency)
overlap         = 1 - (step_size_sec / window_size_sec) = 0.75 (75%)
```

- **Window size ↑** → more temporal context, better frequency resolution (minimum: 1/f_min seconds), higher latency, higher computational cost.
- **Step size ↓** → more frequent decisions, lower per-decision latency, higher total compute.
- **50% overlap** is the standard for seizure detection (widely validated). **75% overlap** for smoother state tracking.
- **Rule of thumb:** Window must be ≥ 2× / f_lowest_band to capture one full cycle. For 0.5 Hz delta: 4 s minimum. For 4 Hz theta: 0.5 s minimum.

**Canonical sliding window implementation for real-time:**

```python
import numpy as np
from collections import deque

class SlidingWindowBuffer:
    """
    Causal circular buffer for real-time EEG inference.
    New samples enter from the right; oldest leave from the left.
    """
    def __init__(self, n_channels: int, window_samples: int, step_samples: int, sfreq: float):
        self.window_samples = window_samples
        self.step_samples = step_samples
        self.sfreq = sfreq
        self.buffer = np.zeros((n_channels, window_samples), dtype=np.float32)
        self.samples_since_last_inference = 0

    def push(self, new_samples: np.ndarray) -> np.ndarray | None:
        """
        Push (n_channels, n_new_samples) into buffer.
        Returns a (n_channels, window_samples) window when step is complete, else None.
        """
        n_new = new_samples.shape[1]
        # Shift buffer left, append new samples on right
        self.buffer = np.roll(self.buffer, -n_new, axis=1)
        self.buffer[:, -n_new:] = new_samples
        self.samples_since_last_inference += n_new

        if self.samples_since_last_inference >= self.step_samples:
            self.samples_since_last_inference = 0
            return self.buffer.copy()  # Return snapshot — never return a view
        return None
```

**Critical detail:** Always `.copy()` when returning from the buffer. Returning a view means the data will be mutated by subsequent pushes while your inference thread is still reading it.

---

### 12.3 Architecture Selection for Real-Time EEG

#### Causal-Only Architectures (Real-Time Safe ✅)

|Architecture|How|Real-time?|Best for|
|---|---|---|---|
|1D-CNN (causal padding)|`padding='causal'` in PyTorch/Keras|✅|Fast, stateless, feature extraction|
|TCN (Temporal Convolutional Network)|Dilated causal convolutions|✅|Long-range temporal context with fixed memory|
|Unidirectional LSTM/GRU|Forward-only, stateful|✅|Stateful sequential modeling, variable-length|
|EEGNet|Depthwise separable CNN, causal|✅|Compact BCI baseline|
|Transformer with causal mask|`torch.nn.MultiheadAttention` with causal mask|✅|Large models with attention; more memory|

#### Architectures That Break Real-Time ❌

|Architecture|Why it fails real-time|
|---|---|
|BiLSTM / BiGRU|Reads future samples — cannot run until full sequence is available|
|Standard Transformer (no mask)|Attends to all tokens including future ones|
|Acausal FIR filters (`filtfilt`)|Zero-phase filtering uses future data|
|Batch normalization (inference on single windows)|Statistics computed over batch — unstable for single-sample inference|

**Fix for batch norm in real-time:** Replace with `LayerNorm` or use `InstanceNorm`. Or switch to `RunningBatchNorm` with exponentially decaying statistics.

#### TCN — The Best Real-Time Architecture for EEG

A Temporal Convolutional Network with exponentially increasing dilation achieves enormous receptive fields with small parameter counts — critical for seizure detection where context windows of 30+ seconds matter.

```python
import torch
import torch.nn as nn

class CausalConv1d(nn.Module):
    """Causal 1D convolution — zero-pads only on the left."""
    def __init__(self, in_ch, out_ch, kernel_size, dilation):
        super().__init__()
        self.padding = (kernel_size - 1) * dilation
        self.conv = nn.Conv1d(in_ch, out_ch, kernel_size, dilation=dilation)

    def forward(self, x):
        x = nn.functional.pad(x, (self.padding, 0))  # left-pad only
        return self.conv(x)

class TCNBlock(nn.Module):
    def __init__(self, n_ch, kernel_size, dilation, dropout=0.2):
        super().__init__()
        self.net = nn.Sequential(
            CausalConv1d(n_ch, n_ch, kernel_size, dilation),
            nn.LayerNorm([n_ch, 1]),  # channel-wise; recompute shape in practice
            nn.ReLU(),
            nn.Dropout(dropout),
            CausalConv1d(n_ch, n_ch, kernel_size, dilation),
            nn.LayerNorm([n_ch, 1]),
            nn.ReLU(),
            nn.Dropout(dropout),
        )
        self.residual = nn.Conv1d(n_ch, n_ch, 1) if True else nn.Identity()

    def forward(self, x):
        return nn.functional.relu(self.net(x) + self.residual(x))

class EEG_TCN(nn.Module):
    """
    Causal TCN for continuous EEG classification.
    Receptive field = 1 + 2 * (kernel_size-1) * sum(dilations)
    """
    def __init__(self, n_channels=22, n_classes=2, n_filters=64,
                 kernel_size=3, n_levels=8, dropout=0.2):
        super().__init__()
        dilations = [2**i for i in range(n_levels)]  # [1,2,4,8,16,32,64,128]
        receptive_field = 1 + 2*(kernel_size-1)*sum(dilations)
        print(f"TCN receptive field: {receptive_field} samples")

        self.input_proj = nn.Conv1d(n_channels, n_filters, 1)
        self.tcn_blocks = nn.ModuleList([
            TCNBlock(n_filters, kernel_size, d, dropout) for d in dilations
        ])
        self.classifier = nn.Conv1d(n_filters, n_classes, 1)  # per-sample output

    def forward(self, x):  # x: (batch, n_channels, n_times)
        x = self.input_proj(x)
        for block in self.tcn_blocks:
            x = block(x)
        return self.classifier(x)  # (batch, n_classes, n_times)
```

**Stateful LSTM for streaming:**

```python
class StatefulEEGLSTM(nn.Module):
    """
    LSTM that maintains hidden state across inference calls —
    essential for continuous streaming where context spans multiple windows.
    """
    def __init__(self, n_channels, hidden_size=128, n_layers=2, n_classes=2):
        super().__init__()
        self.lstm = nn.LSTM(n_channels, hidden_size, n_layers, batch_first=True)
        self.classifier = nn.Linear(hidden_size, n_classes)
        self.hidden = None  # Maintained across forward() calls

    def reset_state(self, batch_size=1, device='cpu'):
        """Call at the start of each recording session, NOT each window."""
        self.hidden = (
            torch.zeros(self.lstm.num_layers, batch_size, self.lstm.hidden_size).to(device),
            torch.zeros(self.lstm.num_layers, batch_size, self.lstm.hidden_size).to(device)
        )

    def forward(self, x):  # x: (1, n_times, n_channels)
        out, self.hidden = self.lstm(x, self.hidden)
        # Detach hidden to prevent BPTT across entire recording
        self.hidden = (self.hidden[0].detach(), self.hidden[1].detach())
        return self.classifier(out)
```

**Key insight:** `self.hidden.detach()` prevents gradients from flowing back across the entire recording history during training. Without this, memory explodes.

---

### 12.4 Data Leakage — The #1 Source of Inflated Accuracy

Data leakage is endemic in published EEG literature. Claude must detect and prevent it. There are five distinct leakage failure modes:

#### Leakage Type 1: Temporal Overlap Between Train and Test

When sliding windows overlap and you split randomly, adjacent windows from the same recording appear in both train and test.

```python
# ❌ WRONG — adjacent overlapping windows end up in both splits
from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split(windows, test_size=0.2, random_state=42)

# ✅ CORRECT — split by recording segment, not by window
n_segments = len(recordings)
train_recs = recordings[:int(0.8*n_segments)]
test_recs  = recordings[int(0.8*n_segments):]
X_train = extract_windows(train_recs)
X_test  = extract_windows(test_recs)
```

#### Leakage Type 2: Subject Leakage in Cross-Subject Evaluation

When data from the same subject appears in both train and test, you measure subject-specific memorization, not generalization.

```python
# ✅ Leave-One-Subject-Out CV
from sklearn.model_selection import LeaveOneGroupOut
logo = LeaveOneGroupOut()
for train_idx, test_idx in logo.split(X, y, groups=subject_ids):
    model.fit(X[train_idx], y[train_idx])
    score = model.score(X[test_idx], y[test_idx])
```

#### Leakage Type 3: Normalization Fitted on All Data

Fitting a scaler on the full dataset before splitting leaks test statistics into training.

```python
# ❌ WRONG
scaler = StandardScaler().fit(X_all)   # sees test data
X_train_scaled = scaler.transform(X_train)

# ✅ CORRECT
scaler = StandardScaler().fit(X_train)  # fit only on train
X_train_scaled = scaler.transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ✅ In sklearn Pipeline (handles this automatically)
pipe = Pipeline([('scaler', StandardScaler()), ('clf', SVC())])
cross_val_score(pipe, X, y, cv=cv)
```

#### Leakage Type 4: ICA or Preprocessing Fitted on All Data

If you fit ICA, ASR, or compute normalization statistics on the full recording (including test segments), you leak signal structure.

```python
# ✅ CORRECT: preprocess each subject independently; within each subject,
# fit ICA only on training epochs before evaluating on test epochs.
```

#### Leakage Type 5: Seizure/Event Window Boundary Leakage

In seizure detection, a window containing samples from both ictal and interictal periods gets labeled ambiguously. If you label it as "ictal" it inflates sensitivity; if "interictal" it inflates specificity.

```python
# ✅ Correct: add a buffer of at least window_size around seizure boundaries
BUFFER_SEC = window_size_sec * 2
seizure_start = annotation.onset
seizure_end   = annotation.onset + annotation.duration

# Exclude any window that overlaps with buffer zone
def label_window(window_start_sec, window_end_sec, seizure_intervals, buffer):
    for s_start, s_end in seizure_intervals:
        # Exclude ambiguous peri-ictal windows entirely
        if window_end_sec > (s_start - buffer) and window_start_sec < (s_end + buffer):
            return None  # Drop this window
    # ... standard labeling
```

---

### 12.5 Class Imbalance — The Seizure / Rare Event Problem

Seizures are rare (typically 0.1–5% of continuous EEG). A model predicting "normal" 100% of the time achieves 99% accuracy — this is a completely useless model. **Accuracy is not a valid metric for imbalanced EEG data.**

**Always report:**

- **Sensitivity** (recall for positive class): fraction of seizures caught.
- **Specificity**: fraction of normal segments correctly labeled.
- **F1 score** (or macro-F1 for multi-class).
- **AUC-ROC** and **AUC-PR** (precision-recall; more informative than ROC for severe imbalance).
- **False Positive Rate** (FPR) in clinical units: false alarms per hour, not percentage.

**Strategies for class imbalance:**

```python
# 1. Weighted loss function (simplest; often sufficient)
n_neg = (y == 0).sum()
n_pos = (y == 1).sum()
pos_weight = torch.tensor([n_neg / n_pos])
criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

# 2. Oversampling with SMOTE (for feature-based models)
from imblearn.over_sampling import SMOTE
X_res, y_res = SMOTE(random_state=42).fit_resample(X, y)

# 3. Temporal oversampling: use higher overlap on seizure windows
# Normal windows: 50% overlap. Seizure windows: 90% overlap.

# 4. Focal loss (focuses training on hard examples)
class FocalLoss(nn.Module):
    def __init__(self, alpha=0.25, gamma=2.0):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
    def forward(self, logits, targets):
        bce = nn.functional.binary_cross_entropy_with_logits(logits, targets, reduction='none')
        pt = torch.exp(-bce)
        return (self.alpha * (1-pt)**self.gamma * bce).mean()

# 5. Threshold calibration at inference
# Don't use 0.5 as decision threshold — tune on validation set
# to balance sensitivity vs. specificity for clinical requirements
```

---

### 12.6 Post-Processing for Continuous Classification

Raw per-window predictions from a model are noisy. Post-processing is essential in any deployed continuous classifier — without it, a single noisy window triggers a false alarm.

```python
from scipy.ndimage import uniform_filter1d

class ContinuousDecisionSmoother:
    """
    Smoothes per-window probability outputs into stable decisions.
    All operations are causal (no future context).
    """
    def __init__(self, smooth_window: int = 5, onset_threshold: float = 0.7,
                 offset_threshold: float = 0.3, min_duration_windows: int = 3):
        self.smooth_window = smooth_window
        self.onset_threshold = onset_threshold
        self.offset_threshold = offset_threshold
        self.min_duration_windows = min_duration_windows
        self.prob_history = deque(maxlen=smooth_window)
        self.in_event = False
        self.event_duration = 0

    def update(self, prob: float) -> dict:
        self.prob_history.append(prob)
        smoothed = np.mean(self.prob_history)

        if not self.in_event and smoothed >= self.onset_threshold:
            self.in_event = True
            self.event_duration = 1
            return {'state': 'onset', 'prob': smoothed}

        elif self.in_event:
            self.event_duration += 1
            if smoothed < self.offset_threshold:
                # Only confirm offset if minimum duration was met
                valid = self.event_duration >= self.min_duration_windows
                self.in_event = False
                return {'state': 'offset', 'prob': smoothed, 'valid': valid}
            return {'state': 'ictal', 'prob': smoothed}

        return {'state': 'interictal', 'prob': smoothed}
```

**Onset/offset asymmetric thresholds** (onset > offset, e.g., 0.7/0.3) prevent rapid flickering between states — a model that classifies seizure→normal→seizure in three consecutive windows is almost certainly detecting noise.

**Minimum duration filter:** Require N consecutive positive windows before firing an alarm. Calibrate N based on clinical tolerance for false alarm latency.

---

### 12.7 Building the Full Real-Time Pipeline — End to End

This is the architecture Claude should produce when asked to implement continuous EEG classification:

```python
import threading
import queue
import numpy as np
import torch

class RealTimeEEGClassifier:
    """
    Production-grade continuous EEG classifier.
    Separation of concerns: acquisition, preprocessing, inference, output.
    """
    def __init__(self, model_path: str, config: dict):
        self.config = config
        self.sfreq = config['sfreq']
        self.n_channels = config['n_channels']
        window_samples = int(config['window_sec'] * self.sfreq)
        step_samples   = int(config['step_sec']   * self.sfreq)

        # Causal preprocessing state
        from scipy.signal import sosfilt_zi, butter
        sos = butter(4, [config['lfreq'], config['hfreq']],
                     btype='bandpass', fs=self.sfreq, output='sos')
        self.sos = sos
        # One zi per channel — causal IIR preserves state across windows
        self.filter_zi = np.stack(
            [sosfilt_zi(sos) for _ in range(self.n_channels)]
        )  # shape: (n_channels, n_stages, 2)

        # Buffer
        self.buffer = SlidingWindowBuffer(self.n_channels, window_samples, step_samples, self.sfreq)

        # Model
        self.model = torch.jit.load(model_path).eval()  # TorchScript for deployment

        # Online normalization (running mean/std, causal)
        self.running_mean = np.zeros(self.n_channels)
        self.running_std  = np.ones(self.n_channels)
        self.n_samples_seen = 0
        self.warmup_samples = int(30 * self.sfreq)  # 30 s warmup before classifying

        # Smoother
        self.smoother = ContinuousDecisionSmoother(**config['smoother'])

        # Thread-safe queues
        self.data_queue   = queue.Queue(maxsize=100)  # raw chunks
        self.result_queue = queue.Queue()             # decisions

        self._running = False

    def push_data(self, chunk: np.ndarray):
        """Called by acquisition thread. chunk: (n_channels, n_new_samples)."""
        if self._running:
            self.data_queue.put_nowait(chunk)

    def _preprocess_chunk(self, chunk: np.ndarray) -> np.ndarray:
        from scipy.signal import sosfilt
        out = np.zeros_like(chunk)
        for ch in range(self.n_channels):
            filtered, self.filter_zi[ch] = sosfilt(
                self.sos, chunk[ch], zi=self.filter_zi[ch]
            )
            out[ch] = filtered

        # Online z-score normalization (Welford's algorithm)
        n = chunk.shape[1]
        self.n_samples_seen += n
        delta = out - self.running_mean[:, None]
        self.running_mean += delta.sum(axis=1) / self.n_samples_seen
        self.running_std = np.sqrt(
            ((self.running_std**2 * (self.n_samples_seen - n)) +
             ((out - self.running_mean[:, None])**2).sum(axis=1)) / self.n_samples_seen
        )
        out = (out - self.running_mean[:, None]) / (self.running_std[:, None] + 1e-8)
        return out

    def _inference_loop(self):
        while self._running:
            try:
                chunk = self.data_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            preprocessed = self._preprocess_chunk(chunk)
            window = self.buffer.push(preprocessed)

            if window is not None and self.n_samples_seen > self.warmup_samples:
                tensor = torch.from_numpy(window[None]).float()  # (1, n_ch, n_t)
                with torch.no_grad():
                    logit = self.model(tensor)
                    prob = torch.sigmoid(logit).item()

                decision = self.smoother.update(prob)
                self.result_queue.put(decision)

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._inference_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()
```

**Key design principles encoded above:**

1. **Stateful causal IIR filter** with `sosfilt` + `zi` (initial conditions). The filter state carries over across chunks — never reset between windows or you get transient artifacts at every window boundary.
2. **Online normalization** via Welford's algorithm (causal, no future data). A 30-second warmup prevents classifying during unstable statistics initialization.
3. **Warmup gate:** don't classify until normalization statistics are stable.
4. **Thread separation:** acquisition thread → data queue → inference thread → result queue. Never block the acquisition thread with inference compute.
5. **TorchScript** (`torch.jit.load`) for production inference — eliminates Python overhead and enables deployment on embedded devices.

---

### 12.8 Training Strategies for Real-Time EEG Models

#### Data Organization for Continuous Models

```python
from torch.utils.data import Dataset

class ContinuousEEGDataset(Dataset):
    """
    Generates sliding windows from continuous recordings.
    Critical: windows are sorted by time within each recording.
    """
    def __init__(self, recordings: list[dict], window_sec: float,
                 step_sec: float, sfreq: float, transforms=None):
        self.windows = []
        self.labels  = []
        self.recording_ids = []  # for LOSO CV

        window_samples = int(window_sec * sfreq)
        step_samples   = int(step_sec   * sfreq)

        for rec in recordings:
            data   = rec['data']    # (n_channels, n_samples)
            labels = rec['labels']  # (n_samples,) — sample-level labels

            for start in range(0, data.shape[1] - window_samples + 1, step_samples):
                end = start + window_samples
                window_data  = data[:, start:end]
                window_label = labels[start:end]

                # Majority vote for window label
                # OR: require >80% of samples to be positive to label positive
                pos_frac = window_label.mean()
                if pos_frac > 0.8:
                    label = 1
                elif pos_frac < 0.2:
                    label = 0
                else:
                    continue  # Drop ambiguous boundary windows

                self.windows.append(window_data)
                self.labels.append(label)
                self.recording_ids.append(rec['subject_id'])

        self.windows = np.array(self.windows, dtype=np.float32)
        self.labels  = np.array(self.labels,  dtype=np.int64)

    def __len__(self): return len(self.labels)
    def __getitem__(self, idx):
        return torch.from_numpy(self.windows[idx]), self.labels[idx]
```

#### Training Loop with Gradient Clipping (Essential for RNNs)

```python
import torch
from torch.cuda.amp import GradScaler, autocast

def train_epoch(model, loader, optimizer, criterion, device, max_grad_norm=1.0):
    model.train()
    scaler = GradScaler()  # Mixed precision — halves memory, ~2× speed on modern GPUs

    total_loss = 0
    for X, y in loader:
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()

        with autocast():
            logits = model(X)
            # For per-sample TCN output, use the last timestep
            if logits.dim() == 3:
                logits = logits[:, :, -1]  # (batch, n_classes)
            loss = criterion(logits.squeeze(), y.float())

        scaler.scale(loss).backward()
        # Gradient clipping prevents exploding gradients in RNNs and deep TCNs
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
        scaler.step(optimizer)
        scaler.update()
        total_loss += loss.item()

    return total_loss / len(loader)
```

#### Learning Rate Scheduling

```python
from torch.optim.lr_scheduler import OneCycleLR, CosineAnnealingLR

# OneCycleLR: warms up then anneals — best for EEG with noisy gradients
scheduler = OneCycleLR(
    optimizer, max_lr=1e-3,
    steps_per_epoch=len(train_loader),
    epochs=100,
    pct_start=0.1  # 10% of training is warmup
)

# Or cosine annealing with warm restarts for longer training
scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
    optimizer, T_0=10, T_mult=2
)
```

---

### 12.9 Evaluation — What to Compute and Report

Never report a single number for EEG models. Always provide:

```python
from sklearn.metrics import (
    classification_report, roc_auc_score, average_precision_score,
    confusion_matrix, f1_score
)
import numpy as np

def evaluate_eeg_model(y_true, y_pred_prob, threshold=0.5, sfreq=256, step_sec=0.5):
    y_pred = (y_pred_prob >= threshold).astype(int)

    # Standard metrics
    print(classification_report(y_true, y_pred, digits=4))
    print(f"AUC-ROC: {roc_auc_score(y_true, y_pred_prob):.4f}")
    print(f"AUC-PR:  {average_precision_score(y_true, y_pred_prob):.4f}")

    # Clinical metrics for continuous detection
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    total_hours = len(y_true) * step_sec / 3600
    fpr_per_hour = fp / total_hours

    print(f"Sensitivity:        {sensitivity:.4f}")
    print(f"Specificity:        {specificity:.4f}")
    print(f"False Positives/hr: {fpr_per_hour:.2f}")

    # Threshold sweep to find clinical operating point
    thresholds = np.linspace(0.1, 0.9, 50)
    for thr in thresholds:
        yp = (y_pred_prob >= thr).astype(int)
        if yp.sum() == 0: continue
        sens = (yp[y_true==1]).mean()
        fpr  = (yp[y_true==0]).mean() * (3600 / step_sec)  # FP per hour
        print(f"thr={thr:.2f}: sens={sens:.3f}, FP/hr={fpr:.1f}")
```

---

### 12.10 Model Deployment — Checklist

When a user asks to deploy an EEG model, work through this checklist:

**Before training:**

- [ ] Defined train/validation/test splits with no leakage (temporal or subject).
- [ ] Chosen correct metric (not accuracy for imbalanced data).
- [ ] Verified architecture is causal if real-time is required.
- [ ] Normalization strategy is causal (fitted only on train; or online for streaming).

**Model optimization for deployment:**

```python
# 1. Export to TorchScript (required for C++/mobile deployment)
scripted = torch.jit.script(model)
scripted.save('eeg_model.pt')

# 2. Quantization (INT8 — 4× smaller, ~2× faster, minimal accuracy loss)
quantized = torch.quantization.quantize_dynamic(
    model, {nn.Linear, nn.LSTM}, dtype=torch.qint8
)

# 3. ONNX export (for cross-framework deployment)
dummy = torch.randn(1, n_channels, window_samples)
torch.onnx.export(model, dummy, 'eeg_model.onnx',
                  input_names=['eeg'], output_names=['logit'],
                  dynamic_axes={'eeg': {0: 'batch', 2: 'time'}})
```

**Runtime checks:**

- [ ] Inference latency measured on target hardware < step_size_sec.
- [ ] Memory usage profiled (filter states, hidden states, model weights).
- [ ] Warmup logic prevents classification during first N seconds.
- [ ] Thread safety verified if acquisition and inference run in parallel.
- [ ] Alarm deduplication prevents rapid re-firing after offset.

---

### 12.11 Task-Specific ML/DL Recipes

#### Seizure Detection (Continuous)

```
Architecture: TCN or CNN-LSTM with causal masking
Window: 2 s, 50% overlap (1 Hz decision rate)
Features OR raw: both work; raw EEG → CNN is now competitive
Loss: weighted BCE or focal loss (seizure imbalance ~1:50 to 1:500)
Post-processing: dual-threshold smoother + min-duration filter (≥3 windows)
Evaluation: sensitivity, FP/hr (not accuracy)
Dataset: CHB-MIT (scalp), TUH EEG Seizure Corpus (large scale)
Key paper: GAT-TCN for spatial+temporal; ring-buffer GRU for wearables
```

#### Mental State Recognition / Cognitive Load (Continuous)

```
Architecture: EEGNet, ShallowConvNet, or Riemannian MDM
Window: 1–4 s (cognitive states evolve slowly)
Features: alpha/beta band power per channel, frontal theta, FAA (frontal alpha asymmetry)
Normalization: per-session z-score (session-level baseline)
Post-processing: exponential moving average over predictions (α=0.1)
Leakage risk: session drift — retrain or recalibrate per session
```

#### Motor Imagery BCI (Pseudo-Real-Time)

```
Architecture: CSP+LDA (classical), EEGNet (DL), pyRiemann MDM (Riemannian)
Window: 3–4 s (full movement imagination window)
Signal: contralateral C3/C4 alpha/beta ERD
CV: session-stratified; report cross-session too
Latency: can tolerate 500 ms–1 s post-trial decision
```

#### Sleep Staging (Offline)

```
Architecture: CNN-LSTM or U-Net on 30-s epochs; DeepSleepNet, U-Sleep
Bidirectional OK: offline analysis, full night available
Channels: C3-M2 EEG + EOG + chin EMG
Labels: AASM 5-stage (W/N1/N2/N3/REM)
Class imbalance: N1 is rare; use macro-F1
Dataset: Sleep-EDF, SHHS, MESA
```

#### Speech Decoding / Brain-to-Text (Advanced)

```
Architecture: Transformer encoder (causal for real-time) or Conformer
Input: high-gamma (70–150 Hz) envelope if ECoG; band power if EEG
Window: 50–100 ms (phoneme timescale)
Key challenge: extreme low SNR on scalp — ECoG dramatically outperforms EEG
Post-processing: language model (beam search) on top of per-frame predictions
Latency: typically 500–800 ms end-to-end acceptable
```

---

### 12.12 Dos and Don'ts — Master Reference

**Architecture dos and don'ts:**

|✅ DO|❌ DON'T|
|---|---|
|Use causal padding (`padding='causal'`) for real-time CNNs|Use `torch.nn.functional.pad` with right-padding in causal models|
|Use `LayerNorm` or `GroupNorm` at inference time|Use `BatchNorm` with single-sample inference (statistics collapse)|
|Detach LSTM hidden state between windows during training|Allow BPTT to flow back through entire recording history|
|Use `sosfilt` + `zi` for causal stateful IIR filtering|Use `filtfilt` in any real-time context (zero-phase = future data)|
|Export to TorchScript or ONNX for production|Run raw Python model objects in production|
|Use `torch.no_grad()` during inference|Run inference without disabling gradient computation|

**Data and evaluation dos and don'ts:**

|✅ DO|❌ DON'T|
|---|---|
|Fit scaler/normalizer only on training data|Fit scaler on full dataset before splitting|
|Split by recording or subject, not by window index|Random shuffle then split sliding windows|
|Add a buffer zone around ictal boundaries|Label boundary windows as clean ictal or clean interictal|
|Report sensitivity, specificity, AUC-PR, and FP/hr|Report accuracy alone for imbalanced EEG tasks|
|Use LOSO CV for cross-subject claims|Use within-subject CV then claim cross-subject generalization|
|Tune decision threshold on validation set|Use 0.5 as default threshold for imbalanced detection|
|Log-transform spectral power before statistical tests|Run t-tests on raw PSD values (not Gaussian)|

**Real-time pipeline dos and don'ts:**

|✅ DO|❌ DON'T|
|---|---|
|Maintain filter state (`zi`) across chunks|Re-initialize filter state at each new window|
|Apply warmup before starting inference|Classify the first few seconds while normalization is unstable|
|Use a circular/ring buffer for streaming data|Concatenate growing arrays (memory leak)|
|Separate acquisition and inference threads with a queue|Run acquisition and inference synchronously (blocks data collection)|
|Implement minimum event duration to suppress brief false positives|Fire alarms on every window that crosses threshold|
|Use asymmetric onset/offset thresholds (hysteresis)|Use single threshold for both event start and end|

---

### 12.13 Datasets Reference for EEG ML

|Dataset|Task|Subjects|Public|Link|
|---|---|---|---|---|
|CHB-MIT Scalp EEG|Seizure detection|23|Yes|PhysioNet|
|TUH EEG Seizure Corpus|Seizure (large scale)|~1000+|Requires request|TUH|
|BCI Competition IV 2a/2b|Motor imagery|9|Yes|BNCI Horizon|
|PhysioNet Motor Imagery|Motor imagery|109|Yes|PhysioNet|
|Sleep-EDF|Sleep staging|197|Yes|PhysioNet|
|DEAP|Emotion recognition|32|Yes|deap-dataset.com|
|SEED|Emotion recognition|15|Yes|BCMI lab|
|MOABB (collection)|BCI benchmarks|Various|Yes|moabb.neurotechx.com|

---

## 13. SIGNAL EVALUATION CHECKLISTS — WHAT CLAUDE SHOULD LOOK FOR

This section is Claude's **perceptual and diagnostic checklist**: a structured set of features, red flags, and evaluation criteria to examine at every stage of EEG analysis. Use this when inspecting raw data, interpreting visualizations, auditing a user's pipeline, or deciding whether output is trustworthy. Go through the relevant subsection(s) before drawing conclusions or generating analysis code.

---

### 13.1 Raw Signal Quality — First-Pass Inspection

When viewing or generating a raw trace plot, evaluate systematically:

**Amplitude (expected: 10–100 µV peak-to-peak for healthy scalp EEG)**

- **Too flat (<1–2 µV):** Broken electrode, disconnected lead, amplifier offset, or software clipping at zero. Mark as bad immediately.
- **Saturation / hard clipping (square tops at fixed ceiling):** Amplifier overload. Cannot recover — mark bad, remove before ICA.
- **Single channel 5–10× neighbors:** Loose electrode contacting skin, EMG source, or hair under pad. Likely bad.
- **All channels uniformly too large:** Wrong unit conversion (e.g., data is in V not µV). Check `raw.info['chs'][0]['cal']`.

**Visual texture — what good EEG looks like vs. doesn't:**

|Pattern|Interpretation|Action|
|---|---|---|
|Layered oscillations, ~10 Hz sinusoid at Oz with eyes closed|Healthy alpha rhythm|✅ Normal|
|Slow drift, all channels shifting the same direction over seconds|Sweat artifact, electrode instability, or DC drift|High-pass filter; check impedances|
|Square-wave ~1 Hz pulses at Fp1/Fp2, bilaterally synchronous|Eye blinks (EOG)|ICA — expected artifact, recoverable|
|Slow lateral alternation Fp1 vs Fp2|Horizontal saccades|ICA|
|High-frequency bursts >30 Hz, maximal at temporal channels|EMG / muscle|ICA + ASR; worst at frontotemporal|
|Periodic slow wave every 1–2 s, visible in all channels|Heartbeat (ECG artifact via electrode near pulse)|ICA — look for ICA001 with QRS shape|
|50 Hz or 60 Hz sinusoid superimposed everywhere|Power line noise|Zapline or notch filter|
|Isolated channels with random intermittent jumps|Electrode pops / impedance spikes|ASR or epoch rejection|
|All channels moving in perfect synchrony with large amplitude|Motion artifact (head movement)|ASR before ICA; mark segments|
|Signal disappears and reappears suddenly|Cable disconnection during recording|Annotate as BAD; never epoch across|

**Impedance sanity check questions to ask the user:**

- Were impedances checked before recording? (Target: <5 kΩ gel, <50 kΩ dry, <20 kΩ active electrodes)
- Was conductive gel used? Dry EEG expects noisier signals, lower SNR — adjust expectations accordingly.
- Was the reference electrode connected? A disconnected reference contaminates every single channel.

---

### 13.2 Artifact Identification — Good Noise vs. Bad Noise

EEG is inherently noisy. Not all noise is bad. Claude must distinguish:

**"Good" noise (physiological, recover-able or acceptable):**

- Eye blinks and saccades: Large, stereotyped, limited to frontal channels → removable by ICA cleanly
- Cardiac artifact: Periodic QRS-shaped in all channels → removable by ICA
- Alpha rhythm when not task-relevant: Not artifact, it's signal — do not over-reject
- High-frequency neural oscillations (gamma in clean ECoG): Actual signal in intracranial recordings

**"Bad" noise (non-physiological or unrecoverable):**

- Continuous EMG throughout recording: Cannot be separated from gamma band signal. If task is gamma analysis, data may be unusable
- Electrode pop artifacts (spike + rail): Instantaneous — corrupt adjacent samples; ASR and epoch rejection
- Movement artifact during mobile EEG: Can overwhelm ICA if not addressed with ASR first
- Clipped/saturated samples: Digital information is destroyed, cannot be recovered
- RF interference (radio frequency, e.g., WiFi, phone): Appears as high-frequency periodic noise above 100 Hz; notch or DSS filter
- Clock drift artifacts in multiplexed systems: Appear as step functions at regular intervals

**How to decide whether an IC is artifact or brain:**

Run through this checklist for every IC under review:

1. **Topographic map** — brain ICs have smooth, focal distributions matching known anatomy (e.g., occipital for alpha, central for motor, frontal for executive). Artifacts:
    
    - Bilateral frontal symmetric blob → eye (blink)
    - Left-right asymmetric frontal dipole → horizontal saccade
    - Lateral temporal fringe / scattered → muscle
    - Single channel isolated → electrode noise
    - Homogeneous over whole scalp → reference or global artifact
2. **Time course** — brain ICs look like filtered EEG. Artifacts:
    
    - Sharp deflection every ~1 s with consistent shape → blink
    - Tall narrow spike every ~0.8 s → heartbeat QRS
    - Irregular high-frequency bursts → muscle
    - Step-function offset → electrode pop
3. **Power spectrum** — brain ICs follow 1/f slope with optional peaks at oscillation frequencies. Artifacts:
    
    - Flat or rising spectrum (more power at high freq) → muscle
    - Sharp peak at 50/60 Hz → line noise
    - Uniform white noise → electrode/channel noise
    - 1/f but with wrong topography → probably artifact
4. **ICLabel score** — use it, but do not trust it blindly. Muscle ICs in particular are frequently mislabeled as "brain" when the signal is spatially complex. Always visually inspect any IC with >20% probability of brain that also has a suspicious topography.
    

---

### 13.3 Filtering — What to Check After Filtering

After applying any filter, confirm the following:

**Check 1: No edge artifacts in epochs**

- Filter → epoch (correct order). If you see large transients at epoch boundaries, you epoched first.
- Confirm: `epochs.plot(events=True)` — first and last 50 ms of epoch should look clean, not ringing.

**Check 2: PSD shape is correct**

- High-pass filtered data should have near-zero power below cutoff.
- Low-pass filtered data should show a hard rolloff.
- Notch-filtered data should show a narrow dip at 50/60 Hz without broad spectral distortion.
- Run `raw.compute_psd(fmax=80).plot()` before and after — compare visually.

**Check 3: No filter-induced phase distortion in ERPs (if using IIR)**

- `filtfilt` gives zero-phase (fine for offline ERP), but uses future data (illegal for real-time).
- `lfilter` / `sosfilt` gives causal phase delay. If using for ERPs, validate that component latencies are consistent with literature.
- FIR filters (MNE default) have constant group delay — predictable and correctable.

**Check 4: 1 Hz high-pass does not distort slow ERPs**

- A 1 Hz high-pass will distort sustained potentials (CNV, P300 slow wave, readiness potential). Visualize the full epoch shape before and after. If late components are clipped or inverted, switch to 0.1 Hz.

**Check 5: Downsampling anti-aliasing**

- If you see aliased frequency content after downsampling (unexpected high-frequency peaks), you forgot the low-pass before resampling. Always: `raw.filter(0, new_sfreq/2) → raw.resample(new_sfreq)`.

---

### 13.4 PSD (Power Spectral Density) — What to Look For

The PSD is the single most informative single-channel diagnostic plot. Evaluate:

**Shape of the PSD:**

- Healthy resting EEG: smooth 1/f slope (log-log approximately linear from 1–40 Hz) with a clear alpha peak (~10 Hz). The slope should be roughly –2 on a log-log plot.
- If the slope is completely flat or positive: excessive muscle artifact, line noise, or data quality problem.
- If there is no alpha peak: subject had eyes open during "resting" recording, or alpha is suppressed by pathology, drowsiness, or artifact.

**Peaks to identify and interpret:**

|Feature|Interpretation|
|---|---|
|Peak at 10 Hz (± individual variation)|Alpha rhythm — eyes closed, posterior channels|
|Peak at 50 or 60 Hz|Power line noise — apply Zapline or notch|
|Peak at 50 + 100 + 150 Hz (harmonics)|Severe line noise|
|Broad plateau 20–100 Hz|Muscle artifact — check EMG, inspect temporals|
|Peak at ~1 Hz|Respiratory artifact or electrode drift|
|Peak matching stimulus frequency (SSVEP)|Correct: steady-state visual evoked potential|
|No 1/f drop — spectrum is flat|White noise floor — recording quality issue or bad channel|

**FOOOF (specparam) interpretation:** After fitting FOOOF to the PSD, check:

- Aperiodic exponent: ~2 for healthy adults at rest. Values >3 suggest pathological slow activity; values near 0 suggest artifact dominance.
- Oscillatory peaks: report center frequency, bandwidth, and power. Do NOT use fixed band boundaries if FOOOF peak center shifts substantially.
- R² of fit: should be >0.95 for clean data. Low R² = model misfit = unusual spectral shape worth examining manually.

**Group-level PSD comparison:**

- Always log-transform PSD before computing group averages or running statistics (PSD is log-normally distributed).
- When comparing groups, check for systematic amplitude differences that might reflect recording differences (electrode impedance, amplifier gain) rather than neural differences.

---

### 13.5 Spectrograms and Time-Frequency Representations — What to Look For

**Which TFR method to use:**

|Method|Temporal resolution|Frequency resolution|Best for|
|---|---|---|---|
|Short-Time Fourier Transform (STFT)|Fixed|Fixed|Quick overview, equal resolution across freqs|
|Morlet wavelets|High at high freq, low at low freq|Low at high freq, high at low freq|ERD/ERS, event-related oscillations|
|Multitaper (DPSS)|Medium|High, stable|Stable spectral estimates, resting-state|
|Hilbert + bandpass|High|Determined by filter|Instantaneous amplitude/phase in narrow band|

**What to look for in a spectrogram:**

- **Event-related desynchronization (ERD):** Blue band (power decrease) in alpha/beta starting shortly before or at movement onset, contralateral to moving limb. If it appears bilaterally or ipsilaterally only, check your event codes or consider cross-activation.
- **Event-related synchronization (ERS):** Red band (power increase) in beta after movement offset — the beta rebound. Absence is informative (suppressed in disease, fatigue).
- **Gamma bursts:** Very short (<200 ms) transient increases above 40 Hz, time-locked to sensory stimulus. If sustained, likely muscle.
- **Drift in baseline:** If the entire spectrogram shifts in power over the recording, there is non-stationarity — electrode settling, fatigue, or attention changes. Consider detrending or dividing into sub-epochs.
- **Spurious spectral leakage:** Sharp peaks that appear at frequencies not expected physiologically. Apply windowing (Hann, Hamming) before FFT.

**Sanity checks for Morlet TFR:**

- Ensure `n_cycles` is frequency-adaptive (e.g., `freqs/2`) — do NOT use a single fixed `n_cycles` for all frequencies.
- Check that low-frequency components (<6 Hz) have sufficient temporal length; a 4 Hz wavelet with 2 cycles is only 500 ms long — shorter than many paradigm epochs.
- Edge effects corrupt the first and last `n_cycles / (2 * freq)` seconds. Crop these before baseline correction or averaging.

---

### 13.6 Source Localization — Evaluating Validity

Source localization adds a forward model and inverse solution to EEG. Before trusting results:

**Pre-localization checks:**

- Is the montage correct? Wrong electrode positions = fundamentally wrong forward model. Always visually confirm the 3D electrode layout matches the physical cap.
- Is the reference appropriate? Average reference is standard for source localization; linked mastoids biases the forward model.
- Were bad channels interpolated? Missing channels create holes in the spatial distribution that corrupt inverse solutions.
- How many channels? Reliable source localization requires ≥64 channels. 19-channel (10-20) clinical EEG produces very poor spatial resolution — treat source estimates skeptically.

**Dipole fitting / DIPFIT (for ICA components):**

- Residual variance (RV) of dipole fit should be <15% to claim a plausible single-dipole source.
- Dipoles landing outside the brain volume (in the skull or air) indicate either artifact ICs or poor forward model.
- Bilateral symmetric dipole pairs for a single IC suggest the component is a difference between hemispheres, not a single source.

**Minimum norm / beamformer results:**

- Compare activation topographies with the original evoked topomaps — they should match. Large discrepancies suggest head model errors or insufficient SNR.
- Check localization of known signals first (e.g., primary visual cortex for flash VEP, primary somatosensory cortex for median nerve SEP). If these are wrong, your head model or MRI co-registration is off.
- Beamformers (LCMV, DICS) suppress correlated sources — they will show artificially low activity in brain regions that co-activate together. Do not use beamforming for studying correlated brain networks.

**Evaluating source-level connectivity:**

- Source leakage remains even after localization — use imaginary coherence or orthogonalized power envelope correlation (PEC) for source-level connectivity.
- Activation in deep sources (thalamus, hippocampus) from scalp EEG is not reliable — EEG is insensitive to radially-oriented or deep sources.

---

### 13.7 ERP Quality — Trial-by-Trial and Averaged Evaluation

**Before averaging — trial-level inspection:**

For each epoch/trial, check:

- Is the pre-stimulus baseline flat? Sustained activity before the baseline window invalidates the subtraction.
- Are there within-trial artifacts that survived ICA + epoch rejection? Use `epochs.plot(events=True)` and visually scroll.
- Is trial count sufficient? Rule of thumb: ≥30 trials per condition minimum, ≥60 preferred. For components with high SNR (P300) 20–30 may suffice; for low-SNR components (MMN, LRP), 80+ trials recommended.
- Is trial distribution balanced across the session? If half your trials are in the first 5 minutes and half in the last 5, fatigue or adaptation effects will bias condition means.

**Epoch-image inspection (essential for ERP quality):**

```
epochs.plot_image(picks=['Pz'])
```

Each row is one trial, sorted by time. Look for:

- Horizontal stripes of artifact (single-trial bad epochs survived rejection)
- Vertical structures (consistent ERP — good sign)
- Diagonal drift (linear trend across the session — detrend or use robust baseline)
- Random noise with no structure (poor SNR — need more trials)

**After averaging — evoked quality check:**

- Butterfly plot: check that the ERP waveform has the expected polarity and topography at canonical components (N1 negative at frontocentral, P300 positive at parietal).
- If all channels look identical with no spatial structure: reference problem.
- If the ERP flips sign unexpectedly: check event code polarity (target vs. non-target swapped? trigger timing off?).
- Baseline mean should be near zero (zero mean by definition after baseline correction). If not, baseline window is inappropriate.

**Latency and amplitude quantification:**

- Mean amplitude in time window: more robust than peak amplitude for broad components (P300, N400).
- Peak amplitude + peak latency: better for sharp, well-defined components (N1, P1).
- Always report the quantification method. "P300 amplitude" is meaningless without specifying whether it is peak, mean window, or area.
- Latency jitter across subjects smears group ERPs — consider individual peak latency detection before group averaging.

**Evoked potential vs. induced activity distinction:**

- **Evoked (phase-locked):** Captured by simple trial averaging. Represents activity phase-locked to stimulus onset.
- **Induced (non-phase-locked):** Cancels out in averaging; requires single-trial TFR then average of power. If you are looking for gamma or alpha changes that are not time-locked in phase, you MUST use induced power, not ERP averaging.

**Checking ERP reliability:**

- Split-half reliability: average odd vs. even trials → compute correlation. Should be >0.85 for reliable components.
- Subaverage stability: plot averages of N/4, N/2, 3N/4, N trials. If waveform shape is still changing at full N, you need more trials.

---

### 13.8 Connectivity — Evaluating Trustworthiness

Connectivity analysis is the most artifact-prone type of EEG analysis. Before reporting any connectivity result:

**Volume conduction check (mandatory):**

- Does connectivity drop off with electrode distance? If strong connectivity is uniform across all electrode pairs regardless of distance, it is volume conduction, not genuine coupling.
- Are the most strongly connected pairs always nearest neighbors? Strong short-range connectivity with weaker long-range connectivity may reflect volume conduction dominating.
- Use imaginary coherence or wPLI rather than standard coherence or PLV. If results change dramatically when switching to imaginary measures, your original results were volume-conduction-inflated.

**Stationarity assumption:**

- Most connectivity measures assume stationary statistics. Check whether the signal has trends, drifts, or event-related amplitude changes that violate stationarity.
- For task-related connectivity, use short epochs and subtract a matched baseline (pre-stimulus) connectivity estimate.

**Evaluating coherence plots:**

- Peak coherence at noise frequencies (50/60 Hz, harmonics) → line noise dominates. Clean first.
- Coherence = 1.0 between two channels at all frequencies → you are computing coherence with itself, or channels are bridged (connected by excess conductive gel).
- Coherence declining to zero at very low frequencies (<0.5 Hz) → high-pass filter removed the signal. Expected.

**Source-level vs. sensor-level connectivity:**

- Always note which level you are computing at. Sensor-level connectivity is inflated by volume conduction. Source-level connectivity requires a valid forward model and inverse solution, but is the scientifically correct target.
- For source-level, use orthogonalized power envelope correlation (PEC) which explicitly removes zero-lag (instantaneous) coupling that could reflect leakage.

---

## 14. EEG ANALYSIS DOS AND DON'TS — MASTER REFERENCE

This section consolidates all dos and don'ts across the entire SKILL into one scannable reference. Consult before writing any pipeline.

### 14.1 Data Collection and Setup

|✅ DO|❌ DON'T|
|---|---|
|Check impedances before every recording|Start recording without impedance verification|
|Record electrode layout (cap model, montage file) in metadata|Assume the montage is correct because it was set last week|
|Note any known issues (noisy channel, subject movement) in a log|Ignore session notes — you will forget|
|Confirm trigger/event codes are firing correctly with a test run|Assume triggers are working and discover they weren't after collection|
|Record sampling rate, reference electrode, hardware amplifier gain|Lose hardware metadata — it affects all downstream unit conversions|
|Ask the user about their hardware before recommending any pipeline|Give generic pipeline advice without knowing if it's dry, gel, mobile, or clinical EEG|

### 14.2 Preprocessing

|✅ DO|❌ DON'T|
|---|---|
|Inspect raw data visually before any processing|Process blindly without a first-pass look|
|Filter → downsample → epoch (in this order)|Epoch → filter (causes edge artifacts in every epoch)|
|Fit ICA on 1 Hz high-passed data; apply to 0.1 Hz data|Fit ICA on unfiltered or very low high-pass data|
|Run ASR before ICA for mobile/high-motion data|Run ICA on data still containing motion artifacts|
|Interpolate bad channels after cleaning, before re-referencing|Interpolate before ICA (inflates ICA component count)|
|Keep a reject log of which channels/epochs were removed|Remove data silently with no documentation|
|Use Zapline or DSS for line noise rather than notch when possible|Notch-filter data intended for analysis near 50/60 Hz|
|Verify filter settings produce expected spectral shape|Apply filters and trust them without checking the PSD|
|Use spherical spline interpolation for bad channels|Use nearest-neighbor interpolation (spatial smoothing artifact)|
|Apply average reference after bad channel interpolation|Apply average reference with missing channels (biases reference)|

### 14.3 Artifact Handling

|✅ DO|❌ DON'T|
|---|---|
|Visually inspect every ICA component before excluding|Auto-exclude components based on ICLabel alone without inspection|
|Use dual-threshold rejection for IC exclusion (probability >0.8)|Exclude everything not labeled "brain" — over-rejection|
|Keep a record of how many ICs were removed per subject|Remove ICs without documentation|
|Treat gamma-band results with extreme skepticism unless ECoG|Report scalp gamma findings as neural without rigorous EMG rejection|
|Use AutoReject or threshold rejection for residual epoch artifacts|Assume ICA solved all artifacts|
|Reject the epoch if artifact is so large ICA cannot recover it|Keep all data regardless of quality to maximize trial count|
|Check reject log for systematic session-level biases|Ignore which epochs were rejected (they might cluster in one condition)|

### 14.4 Spectral and TFR Analysis

|✅ DO|❌ DON'T|
|---|---|
|Log-transform PSD before any statistical test|Run t-tests or ANOVA on raw power values (not normally distributed)|
|Use FOOOF to separate 1/f from oscillatory peaks|Use fixed frequency bands without checking for individual variation|
|Compute individual alpha frequency (IAF) per subject|Assume 8–13 Hz alpha band applies to all subjects|
|Use frequency-adaptive n_cycles for Morlet wavelets|Use fixed n_cycles = 7 for all frequencies|
|Crop TFR edge effects before baseline correction|Use the full epoch including edges where wavelets have not converged|
|Apply Hann or Hamming window before FFT|Take raw FFT without windowing (spectral leakage)|
|Use multitaper for stable PSD estimates of long segments|Use single periodogram for noisy PSD estimates|

### 14.5 Connectivity Analysis

|✅ DO|❌ DON'T|
|---|---|
|Use wPLI or imaginary coherence for sensor-level connectivity|Use standard coherence or PLV at sensor level (volume conduction)|
|Check whether connectivity pattern is distance-dependent|Report uniform connectivity without distance sanity check|
|Compute baseline-corrected connectivity for task epochs|Report absolute connectivity without baseline|
|Work toward source-level connectivity for any publishable result|Stop at sensor-level and ignore volume conduction confounds|
|Use non-parametric permutation statistics for connectivity|Use parametric t-tests on connectivity values (not normally distributed)|

### 14.6 ERP and Evoked Potential Analysis

|✅ DO|❌ DON'T|
|---|---|
|Define time windows and channels of interest a priori|Select channels and windows post-hoc based on largest effect|
|Use cluster permutation tests for mass univariate ERP comparison|Use uncorrected t-test at every time point (massive multiple comparisons)|
|Inspect epoch images (trial × time) before averaging|Average without checking for trial-level structure|
|Use mean amplitude in window for broad components|Use peak amplitude for broad components (sensitive to noise)|
|Report trial count per condition per subject|Report group ERP without noting how many trials contributed|
|Check split-half reliability of ERP components|Report ERP components that may not be reliably estimable|
|Apply baseline correction relative to pre-stimulus window|Forget baseline correction or use an inappropriate window|

### 14.7 Machine Learning and Modeling

|✅ DO|❌ DON'T|
|---|---|
|Split by subject or recording segment, not by window index|Random-shuffle sliding windows then split train/test|
|Use LOSO CV for cross-subject generalization claims|Use within-subject CV and claim cross-subject results|
|Fit all normalizers only on training data|Fit scaler on full dataset before splitting|
|Report sensitivity, specificity, and AUC-PR for imbalanced tasks|Report accuracy alone for rare-event detection|
|Use causal architectures and filters for real-time systems|Use bidirectional RNNs or `filtfilt` in real-time pipelines|
|Add buffer zones around event boundaries to avoid label leakage|Label boundary windows as clean positive or negative|
|Report confidence intervals and across-fold variability|Report a single mean accuracy without variance|

---

## 15. DATA INGESTION GUIDE — MULTIMODAL, MESSY, AND BEHAVIORAL DATA

This section addresses the messy reality of real EEG research: data arrives in multiple formats from multiple devices, with misaligned timestamps, poorly labeled CSV files, and behavioral records that need to be mapped onto brain signals.

---

### 15.1 The Ingestion Mindset

Before writing any ingestion code, Claude should ask:

1. **What devices were used?** Each device has its own clock, sampling rate, format, and timestamp convention. They drift.
2. **How was synchronization implemented?** Hardware trigger (gold standard), LSL, software timestamps (unreliable), or none at all?
3. **What is the ground truth timestamp?** TTL trigger pulses into the EEG amplifier are the most reliable. Behavioral software timestamps are second. System clocks across devices are worst.
4. **What is the label schema?** How are trials, subjects, sessions, and conditions identified? Is there a codebook?
5. **What is the expected sample count?** Duration × sampling rate. If the file has ±0.1% fewer samples, there was a dropped packet. This matters for synchronization.

---

### 15.2 Messy CSV Files — Ingestion Strategy

EEG-adjacent data often arrives as CSV from behavioral software, sensor logs, or custom hardware. These files are frequently malformed.

**Common CSV problems and fixes:**

```python
import pandas as pd
import numpy as np

# Problem 1: Unknown delimiter or mixed delimiters
df = pd.read_csv('data.csv', sep=None, engine='python')  # auto-detect delimiter

# Problem 2: Multiple header rows or comment lines
df = pd.read_csv('data.csv', skiprows=3, comment='#')

# Problem 3: Mixed dtypes in numeric columns (e.g., "N/A", "MISSING", "---")
df = pd.read_csv('data.csv', na_values=['N/A', 'MISSING', '---', 'nan', ''])

# Problem 4: Timestamp columns in non-standard format
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S.%f',
                                  utc=True)  # always specify UTC if possible

# Problem 5: Column names have spaces, mixed case, special characters
df.columns = (df.columns
              .str.strip()
              .str.lower()
              .str.replace(' ', '_')
              .str.replace(r'[^a-z0-9_]', '', regex=True))

# Problem 6: Duplicate rows (e.g., logging software wrote each row twice)
df = df.drop_duplicates()

# Problem 7: Data from multiple files with different column schemas
dfs = []
for path in file_paths:
    tmp = pd.read_csv(path)
    tmp['source_file'] = path.name  # track origin
    dfs.append(tmp)
df = pd.concat(dfs, ignore_index=True, sort=False)

# Problem 8: Numeric columns stored as strings with thousands separators
df['reaction_time_ms'] = (df['reaction_time_ms']
                           .str.replace(',', '')
                           .astype(float))

# Problem 9: Mixed encoding (common with MATLAB-exported CSV)
df = pd.read_csv('data.csv', encoding='latin-1')  # try if utf-8 fails

# Problem 10: Values in wrong units (ms vs s, V vs µV)
# Always normalize to SI units internally, convert only for display
if df['eeg_amplitude'].abs().max() < 0.01:
    df['eeg_amplitude_uv'] = df['eeg_amplitude'] * 1e6  # V → µV
```

**Validation after loading:**

```python
def validate_eeg_csv(df: pd.DataFrame, expected_sfreq: float) -> dict:
    report = {}

    # Check for expected columns
    required = ['timestamp', 'channel', 'amplitude']
    report['missing_cols'] = [c for c in required if c not in df.columns]

    # Check for duplicates
    report['n_duplicates'] = df.duplicated().sum()

    # Check sampling regularity
    if 'timestamp' in df.columns:
        diffs = df['timestamp'].diff().dropna()
        expected_dt = 1.0 / expected_sfreq
        jitter = (diffs - expected_dt).abs()
        report['max_jitter_ms'] = jitter.max() * 1000
        report['dropped_samples'] = (jitter > expected_dt * 1.5).sum()

    # Check amplitude range
    if 'amplitude' in df.columns:
        report['amp_min'] = df['amplitude'].min()
        report['amp_max'] = df['amplitude'].max()
        report['n_nan'] = df['amplitude'].isna().sum()
        report['n_clipped'] = ((df['amplitude'].abs() > 3000e-6) |
                                (df['amplitude'].abs() < 1e-9)).sum()

    return report
```

---

### 15.3 Multi-Modal Data — Device Inventory and Clock Alignment

When multiple devices are recording simultaneously (EEG + eye tracker, EEG + motion capture, EEG + fNIRS, etc.), each device runs on its own clock. These clocks drift relative to each other, sometimes by tens of milliseconds over a one-hour session.

**Step 1: Build a device inventory table**

For every device, document before starting ingestion:

```python
DEVICE_REGISTRY = {
    'eeg': {
        'device': 'BrainProducts actiCHamp',
        'sfreq': 500,                          # Hz
        'n_channels': 64,
        'timestamp_source': 'hardware_trigger', # most reliable
        'format': 'BrainVision .vhdr',
        'trigger_channel': 'STI 014',
        'clock_drift_ppm': 50,                 # typical crystal oscillator
    },
    'eyetracker': {
        'device': 'Tobii Pro Fusion',
        'sfreq': 120,
        'timestamp_source': 'software_utc',
        'format': 'CSV',
        'clock_drift_ppm': 200,
    },
    'mocap': {
        'device': 'OptiTrack Motive',
        'sfreq': 120,
        'timestamp_source': 'software_utc',
        'format': 'CSV',
        'clock_drift_ppm': 200,
    },
}
```

**Step 2: Identify synchronization events**

The best synchronization strategy uses a common hardware event visible in all streams:

- A TTL pulse sent simultaneously to EEG trigger channel AND other device
- An LED flash visible to eye tracker AND recorded as EEG trigger
- A LSL outlet that stamps all streams with the same marker

```python
def find_sync_events(eeg_raw, behavioral_df, eeg_trigger_id: int,
                     behav_trigger_col: str) -> pd.DataFrame:
    """
    Returns a DataFrame of matched sync event pairs.
    eeg_raw: MNE Raw object with trigger channel
    behavioral_df: DataFrame with behavioral timestamps
    """
    # EEG sync events (in samples → convert to seconds)
    events, _ = mne.events_from_annotations(eeg_raw)
    eeg_sync = events[events[:, 2] == eeg_trigger_id]
    eeg_times_sec = eeg_sync[:, 0] / eeg_raw.info['sfreq']

    # Behavioral sync events
    behav_sync = behavioral_df[behavioral_df[behav_trigger_col].notna()].copy()
    behav_times_sec = behav_sync['timestamp'].values

    # Match by order (assumes same number of events and no missed triggers)
    n = min(len(eeg_times_sec), len(behav_times_sec))
    sync_df = pd.DataFrame({
        'eeg_time_sec':   eeg_times_sec[:n],
        'behav_time_sec': behav_times_sec[:n],
        'offset_sec':     behav_times_sec[:n] - eeg_times_sec[:n],
    })

    # Check for trigger timing consistency (offset should be near-constant)
    offset_std = sync_df['offset_sec'].std()
    if offset_std > 0.005:  # >5 ms jitter
        print(f"WARNING: Sync offset std = {offset_std*1000:.1f} ms — possible missed triggers")

    return sync_df
```

**Step 3: Compute and apply clock drift correction**

If you have multiple sync events across the session, fit a linear clock drift model:

```python
from scipy import stats

def compute_clock_drift(sync_df: pd.DataFrame) -> tuple[float, float]:
    """
    Linear regression: behavioral_time = slope * eeg_time + intercept
    slope ≈ 1.0 (perfect sync), deviations indicate clock drift.
    """
    slope, intercept, r, p, se = stats.linregress(
        sync_df['eeg_time_sec'], sync_df['behav_time_sec']
    )
    drift_ppm = (slope - 1.0) * 1e6
    print(f"Clock drift: {drift_ppm:.1f} ppm | R²={r**2:.4f}")
    print(f"Over 1 hour: {drift_ppm * 3600 / 1000:.1f} ms cumulative drift")
    return slope, intercept

def align_behavioral_to_eeg(behav_times: np.ndarray,
                              slope: float, intercept: float) -> np.ndarray:
    """Convert behavioral timestamps to EEG timebase."""
    return (behav_times - intercept) / slope
```

---

### 15.4 Subject-Level Alignment — Batch Processing Across Sessions

In multi-subject studies, every subject has a different data folder, possibly different channel counts, recording lengths, or missing sessions. The ingestion layer must be robust to this.

```python
from pathlib import Path
import json
import logging

logger = logging.getLogger('eeg_ingest')

class SubjectIngestor:
    """
    Loads, validates, and aligns all data for one subject.
    Designed to be called in a loop across all subjects.
    """
    REQUIRED_FILES = ['eeg', 'behavioral', 'events']

    def __init__(self, subject_id: str, data_root: Path, config: dict):
        self.sid = subject_id
        self.root = data_root / subject_id
        self.config = config
        self.issues = []   # collects non-fatal warnings
        self.fatal = False

    def load(self) -> dict | None:
        result = {}

        # 1. Check expected files exist
        for ftype in self.REQUIRED_FILES:
            pattern = self.config['file_patterns'][ftype].format(sid=self.sid)
            matches = list(self.root.glob(pattern))
            if not matches:
                self.issues.append(f"MISSING: {ftype} file ({pattern})")
                if ftype == 'eeg':
                    self.fatal = True  # can't proceed without EEG
            else:
                result[ftype + '_path'] = matches[0]
                if len(matches) > 1:
                    self.issues.append(f"MULTIPLE matches for {ftype}: {matches}")

        if self.fatal:
            logger.error(f"[{self.sid}] Fatal issue: {self.issues}")
            return None

        # 2. Load EEG
        try:
            raw = mne.io.read_raw(str(result['eeg_path']), preload=False)
            result['raw'] = raw
            result['sfreq'] = raw.info['sfreq']
            result['n_channels'] = len(raw.ch_names)
            result['duration_sec'] = raw.times[-1]
        except Exception as e:
            logger.error(f"[{self.sid}] EEG load failed: {e}")
            return None

        # 3. Load behavioral
        try:
            behav = pd.read_csv(result['behavioral_path'])
            behav = self._clean_behavioral(behav)
            result['behavioral'] = behav
        except Exception as e:
            self.issues.append(f"Behavioral load failed: {e}")
            result['behavioral'] = None

        # 4. Validate channel count
        expected_channels = self.config['expected_n_channels']
        if result['n_channels'] != expected_channels:
            self.issues.append(
                f"Channel count mismatch: got {result['n_channels']}, "
                f"expected {expected_channels}"
            )

        # 5. Log summary
        logger.info(f"[{self.sid}] Loaded: {result['n_channels']}ch, "
                    f"{result['duration_sec']:.1f}s, "
                    f"{len(result.get('behavioral', []))} trials")
        if self.issues:
            logger.warning(f"[{self.sid}] Issues: {self.issues}")

        result['subject_id'] = self.sid
        result['issues'] = self.issues
        return result

    def _clean_behavioral(self, df: pd.DataFrame) -> pd.DataFrame:
        # Standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        # Parse timestamps
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
        return df


def batch_ingest(subject_ids: list[str], data_root: Path,
                 config: dict) -> tuple[list[dict], pd.DataFrame]:
    """Returns (valid_data_list, quality_report_df)."""
    all_data = []
    report_rows = []

    for sid in subject_ids:
        ingestor = SubjectIngestor(sid, data_root, config)
        data = ingestor.load()

        report_rows.append({
            'subject_id': sid,
            'loaded': data is not None,
            'fatal': ingestor.fatal,
            'n_issues': len(ingestor.issues),
            'issues': '; '.join(ingestor.issues),
            'n_channels': data['n_channels'] if data else None,
            'duration_sec': data['duration_sec'] if data else None,
        })

        if data is not None:
            all_data.append(data)

    report = pd.DataFrame(report_rows)
    print(f"\nIngestion summary: {report['loaded'].sum()}/{len(subject_ids)} subjects loaded")
    print(report[report['n_issues'] > 0][['subject_id', 'issues']])
    return all_data, report
```

---

### 15.5 Aligning Behavioral Data to EEG — Trial-by-Trial

The most common alignment task: a behavioral CSV has one row per trial with response times and conditions; the EEG has trigger codes marking trial onsets. They must be merged.

```python
def align_trials(epochs: mne.Epochs, behavioral_df: pd.DataFrame,
                 trial_id_col: str = 'trial_number') -> pd.DataFrame:
    """
    Aligns behavioral trial data to EEG epochs.
    Returns a merged DataFrame with one row per trial.
    """
    # Extract epoch metadata
    epoch_meta = pd.DataFrame({
        'trial_number': np.arange(len(epochs)),
        'event_id':     [e[2] for e in epochs.events],
        'event_sample': [e[0] for e in epochs.events],
        'event_time_sec': epochs.events[:, 0] / epochs.info['sfreq'],
    })

    # Behavioral must have a trial number column
    if trial_id_col not in behavioral_df.columns:
        raise ValueError(f"'{trial_id_col}' column not found in behavioral data. "
                         f"Available: {list(behavioral_df.columns)}")

    # Merge on trial number
    merged = epoch_meta.merge(behavioral_df, on=trial_id_col, how='left')

    # Sanity checks
    n_unmatched = merged[behavioral_df.columns[0]].isna().sum()
    if n_unmatched > 0:
        print(f"WARNING: {n_unmatched} epochs have no behavioral match")

    n_duplicate_trials = behavioral_df[trial_id_col].duplicated().sum()
    if n_duplicate_trials > 0:
        print(f"WARNING: {n_duplicate_trials} duplicate trial IDs in behavioral data")

    return merged


# Usage: sort epochs by a behavioral variable (reaction time)
trial_data = align_trials(epochs, behavioral_df)
rt_order = trial_data.sort_values('reaction_time_ms').index.values
epochs_sorted = epochs[rt_order]
```

---

### 15.6 Aligning Continuous External Signals — Hand Trajectories, Kinematics, Eye Tracking

When external signals (hand position, eye gaze, EMG, respiration) are recorded alongside EEG, the goal is a common time axis so you can correlate brain signals with behavior sample-by-sample.

**The general procedure:**

```python
import numpy as np
from scipy import interpolate, signal as sp_signal

def align_continuous_signal(external_times: np.ndarray,
                              external_data: np.ndarray,
                              eeg_times: np.ndarray,
                              method: str = 'linear') -> np.ndarray:
    """
    Resamples an external continuous signal to the EEG time axis.

    Parameters
    ----------
    external_times : (N,) array of external device timestamps in EEG timebase
                     (after clock drift correction via align_behavioral_to_eeg)
    external_data  : (N, n_features) or (N,) array of external signal values
    eeg_times      : (T,) array of EEG sample times (raw.times)
    method         : 'linear', 'cubic', or 'nearest'

    Returns
    -------
    (T, n_features) array resampled to EEG timebase
    """
    if external_data.ndim == 1:
        external_data = external_data[:, None]

    n_features = external_data.shape[1]
    resampled = np.zeros((len(eeg_times), n_features))

    for feat in range(n_features):
        # Remove NaN before interpolation
        valid = ~np.isnan(external_data[:, feat])
        if valid.sum() < 2:
            resampled[:, feat] = np.nan
            continue

        f_interp = interpolate.interp1d(
            external_times[valid],
            external_data[valid, feat],
            kind=method,
            bounds_error=False,
            fill_value=np.nan  # extrapolation → NaN, not garbage values
        )
        resampled[:, feat] = f_interp(eeg_times)

    return resampled.squeeze()


# Full example: hand trajectory aligned to EEG
# 1. Load motion capture data
mocap_df = pd.read_csv('hand_trajectory.csv')
mocap_times_raw = mocap_df['timestamp_sec'].values  # in mocap clock
mocap_xyz = mocap_df[['x', 'y', 'z']].values        # (N, 3) in mm

# 2. Convert mocap timestamps to EEG timebase
slope, intercept = compute_clock_drift(sync_df)
mocap_times_eeg = align_behavioral_to_eeg(mocap_times_raw, slope, intercept)

# 3. Resample to EEG sample rate
eeg_times = raw.times
hand_xyz_resampled = align_continuous_signal(
    mocap_times_eeg, mocap_xyz, eeg_times, method='cubic'
)  # shape: (n_eeg_samples, 3)

# 4. Compute velocity (first derivative, smoothed)
hand_velocity = np.gradient(hand_xyz_resampled, 1/raw.info['sfreq'], axis=0)
hand_speed = np.linalg.norm(hand_velocity, axis=1)

# 5. Create MNE-compatible misc channel from external signal
info_misc = mne.create_info(['hand_x', 'hand_y', 'hand_z', 'hand_speed'],
                              sfreq=raw.info['sfreq'], ch_types='misc')
external_raw = mne.io.RawArray(
    np.vstack([hand_xyz_resampled.T, hand_speed[None]]),
    info_misc
)
raw_combined = raw.add_channels([external_raw], force_update_info=True)
```

**After alignment, validate with a synchrony check:**

```python
# Plot EEG signal and external signal together on same time axis
fig, axes = plt.subplots(2, 1, figsize=(15, 6), sharex=True)
axes[0].plot(eeg_times, raw.get_data(picks='Cz')[0] * 1e6)
axes[0].set_ylabel('EEG Cz (µV)')
axes[1].plot(eeg_times, hand_speed)
axes[1].set_ylabel('Hand speed (mm/s)')
axes[1].set_xlabel('Time (s)')

# Draw event markers on both panels
for ev_time in event_times_sec:
    for ax in axes:
        ax.axvline(ev_time, color='r', alpha=0.4, linewidth=0.8)
plt.tight_layout()
```

---

### 15.7 Multimodal Feature Matrix Construction

After alignment, the next step is typically constructing a feature matrix that combines EEG features with external signals for modeling.

```python
def build_multimodal_feature_matrix(
    epochs: mne.Epochs,
    trial_data: pd.DataFrame,
    external_epochs: np.ndarray,   # (n_trials, n_ext_features, n_times)
    eeg_bands: dict = None,
) -> pd.DataFrame:
    """
    Builds a trial × feature DataFrame combining EEG and external data.
    Ready for scikit-learn input.
    """
    if eeg_bands is None:
        eeg_bands = {
            'theta': (4, 8), 'alpha': (8, 13),
            'beta': (13, 30), 'gamma': (30, 45)
        }

    rows = []
    eeg_data = epochs.get_data()  # (n_trials, n_channels, n_times)
    sfreq = epochs.info['sfreq']

    for trial_idx in range(len(epochs)):
        row = {'trial_idx': trial_idx}

        # Behavioral features from aligned trial_data
        if trial_data is not None:
            for col in ['reaction_time_ms', 'accuracy', 'condition']:
                if col in trial_data.columns:
                    row[col] = trial_data.iloc[trial_idx][col]

        # EEG band power features (mean across time, per channel)
        eeg_trial = eeg_data[trial_idx]  # (n_channels, n_times)
        for band_name, (flo, fhi) in eeg_bands.items():
            freqs_w, psd_trial = sp_signal.welch(
                eeg_trial, fs=sfreq, nperseg=min(256, eeg_trial.shape[1])
            )
            band_mask = (freqs_w >= flo) & (freqs_w <= fhi)
            band_power = np.log10(psd_trial[:, band_mask].mean(axis=1) + 1e-12)
            for ch_idx, ch_name in enumerate(epochs.ch_names):
                row[f'{band_name}_{ch_name}'] = band_power[ch_idx]

        # External signal features (if provided)
        if external_epochs is not None:
            ext_trial = external_epochs[trial_idx]  # (n_ext_features, n_times)
            for feat_idx in range(ext_trial.shape[0]):
                row[f'ext_{feat_idx}_mean'] = np.nanmean(ext_trial[feat_idx])
                row[f'ext_{feat_idx}_max']  = np.nanmax(ext_trial[feat_idx])
                row[f'ext_{feat_idx}_std']  = np.nanstd(ext_trial[feat_idx])

        rows.append(row)

    feature_df = pd.DataFrame(rows)
    print(f"Feature matrix: {feature_df.shape[0]} trials × {feature_df.shape[1]} features")
    print(f"Missing values: {feature_df.isna().sum().sum()}")
    return feature_df
```

---

### 15.8 Data Ingestion Dos and Don'ts

|✅ DO|❌ DON'T|
|---|---|
|Build a device registry documenting sfreq, format, and clock source for every modality|Assume all devices share the same clock or that software timestamps are reliable|
|Use hardware trigger pulses as the synchronization ground truth|Use system UTC timestamps alone for alignment — they drift and jitter|
|Compute linear clock drift correction from multiple sync events|Use only a single sync event (captures only offset, not drift)|
|Validate alignment visually by overlaying time-locked events on all modalities|Trust alignment code without visual verification|
|Log every ingestion issue per subject in a quality report|Silently drop subjects or trials with issues|
|Resample external signals to EEG timebase (not the reverse)|Resample EEG to a lower sampling rate external signal|
|Use `interp1d` with `bounds_error=False, fill_value=np.nan`|Extrapolate beyond the recorded range (garbage values at edges)|
|Document the behavioral codebook (what each event code means)|Assume event code meanings are obvious or remembered|
|Check for duplicate trial IDs, missing triggers, or extra triggers|Merge behavioral and EEG trial counts and assume they match|
|Store raw ingested data as MNE FIF or HDF5 before processing|Work from the original CSV/EDF every time (slow, fragile)|
|Normalize units to µV (EEG) and SI units (external) at ingestion|Mix unit conventions across pipeline stages|

---

## 16. STATISTICAL ANALYSIS AND VISUALIZATION — COMPLETE GUIDE

This section gives Claude everything needed to perform rigorous statistical analysis on EEG-derived features: which test to choose, how to check assumptions, what to plot and when, and how to avoid the most common statistical mistakes in neuroscience research.

---

### 16.1 The Statistical Workflow — Always Follow This Order

Before computing any p-value, work through these steps in sequence:

```
1. Visualize raw distributions (histogram + violin/box per group)
2. Check normality (Shapiro-Wilk, Q-Q plot)
3. Check variance homogeneity if comparing groups (Levene's test)
4. Choose parametric vs. non-parametric based on above
5. Check for multiple comparisons — apply correction before reporting
6. Compute effect size alongside p-value
7. Visualize the result (not just report the number)
```

Skipping steps 1–3 and jumping to a t-test is the most common mistake in EEG data analysis.

---

### 16.2 Assumption Checking — Code Reference

```python
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg

# ─── Normality ───────────────────────────────────────────────────────────────

def check_normality(data: np.ndarray, label: str = 'data', alpha: float = 0.05):
    """
    Shapiro-Wilk (n < 5000) or D'Agostino-Pearson (n >= 5000).
    For EEG band power: always log-transform first.
    """
    n = len(data)
    if n < 3:
        print(f"[{label}] Too few samples for normality test (n={n})")
        return None

    if n < 5000:
        stat, p = stats.shapiro(data)
        test_name = "Shapiro-Wilk"
    else:
        stat, p = stats.normaltest(data)  # D'Agostino + Pearson
        test_name = "D'Agostino-Pearson"

    print(f"[{label}] {test_name}: W={stat:.4f}, p={p:.4f} "
          f"{'→ NORMAL ✓' if p > alpha else '→ NON-NORMAL ✗'}")
    return p > alpha


def qq_plot(data: np.ndarray, label: str = ''):
    """Q-Q plot for visual normality assessment — use alongside Shapiro-Wilk."""
    fig, ax = plt.subplots(figsize=(5, 5))
    stats.probplot(data, dist="norm", plot=ax)
    ax.set_title(f"Q-Q Plot: {label}")
    plt.tight_layout()
    return fig


# ─── Variance Homogeneity ─────────────────────────────────────────────────────

def check_homogeneity(*groups, alpha: float = 0.05):
    """Levene's test for equal variances. Required before unpaired t-test or ANOVA."""
    stat, p = stats.levene(*groups)
    print(f"Levene's test: W={stat:.4f}, p={p:.4f} "
          f"{'→ EQUAL VARIANCES ✓' if p > alpha else '→ UNEQUAL VARIANCES ✗'}")
    if p <= alpha:
        print("  → Use Welch's t-test (equal_var=False) or non-parametric test")
    return p > alpha


# ─── Sphericity (for repeated-measures ANOVA) ─────────────────────────────────

# Use pingouin — it automatically applies Greenhouse-Geisser correction
# when sphericity is violated. Always use pingouin for rm_anova.
```

---

### 16.3 Choosing the Right Test — Decision Guide

```
Is the question about differences between groups/conditions?
│
├── Two groups / two conditions
│   ├── Paired (same subjects, two conditions)?
│   │   ├── Normal + equal var → Paired t-test: stats.ttest_rel()
│   │   └── Non-normal          → Wilcoxon signed-rank: stats.wilcoxon()
│   └── Independent (different subjects)?
│       ├── Normal + equal var  → Independent t-test: stats.ttest_ind(equal_var=True)
│       ├── Normal + unequal var → Welch's t-test: stats.ttest_ind(equal_var=False)
│       └── Non-normal           → Mann-Whitney U: stats.mannwhitneyu()
│
├── Three or more groups / conditions
│   ├── Repeated-measures (within-subject)?
│   │   ├── Normal + sphericity → rm_anova: pg.rm_anova()
│   │   ├── Sphericity violated → Greenhouse-Geisser (auto in pingouin)
│   │   └── Non-normal          → Friedman: stats.friedmanchisquare()
│   └── Independent groups?
│       ├── Normal + equal var  → One-way ANOVA: stats.f_oneway()
│       └── Non-normal           → Kruskal-Wallis: stats.kruskal()
│
├── Post-hoc after ANOVA (which pairs differ)?
│   ├── Parametric → Tukey HSD: pg.pairwise_tukey()
│   └── Non-parametric → Dunn's test with Bonferroni/FDR: pg.pairwise_tests()
│
└── Is the question about a relationship between two continuous variables?
    ├── Linear + normal → Pearson r: stats.pearsonr()
    ├── Non-linear or non-normal → Spearman ρ: stats.spearmanr()
    ├── Predicting one from another → Linear regression: stats.linregress()
    └── Multiple predictors → OLS: pg.linear_regression() or statsmodels
```

**Critical EEG-specific rules:**

- **Always log-transform spectral power** before any parametric test — PSD is log-normally distributed by nature.
- **Reaction times** are right-skewed — use log-transform or non-parametric tests.
- **Correlation matrices** across many EEG channels require multiple comparisons correction.
- **ERP amplitudes** are typically close enough to normal for parametric tests after averaging across sufficient trials, but verify with Shapiro-Wilk first.

---

### 16.4 Core Statistical Tests — Full Code Reference

```python
# ─── T-tests ──────────────────────────────────────────────────────────────────

# Paired t-test (within-subject, two conditions)
t, p = stats.ttest_rel(condition_A, condition_B)
d = pg.compute_effsize(condition_A, condition_B, eftype='cohen')
print(f"Paired t-test: t={t:.3f}, p={p:.4f}, Cohen's d={d:.3f}")

# Independent t-test (Welch's — always safer, doesn't assume equal variance)
t, p = stats.ttest_ind(group1, group2, equal_var=False)
d = pg.compute_effsize(group1, group2, eftype='cohen')

# Wilcoxon signed-rank (non-parametric paired alternative)
stat, p = stats.wilcoxon(condition_A, condition_B, alternative='two-sided')
r = stat / np.sqrt(len(condition_A))  # rank-biserial effect size approximation

# Mann-Whitney U (non-parametric independent groups)
stat, p = stats.mannwhitneyu(group1, group2, alternative='two-sided')
r = 1 - (2 * stat) / (len(group1) * len(group2))  # rank-biserial r


# ─── ANOVA ────────────────────────────────────────────────────────────────────

# One-way ANOVA (independent groups)
f, p = stats.f_oneway(group1, group2, group3)
# Effect size: eta-squared
ss_between = sum(len(g) * (np.mean(g) - np.mean(np.concatenate([group1, group2, group3])))**2
                 for g in [group1, group2, group3])
ss_total = np.var(np.concatenate([group1, group2, group3]), ddof=0) * \
           (len(group1) + len(group2) + len(group3))
eta_sq = ss_between / ss_total
print(f"One-way ANOVA: F={f:.3f}, p={p:.4f}, η²={eta_sq:.3f}")

# Repeated-measures ANOVA (within-subject, ≥3 conditions) — use pingouin
import pingouin as pg
# Data must be in long format: columns = [subject, condition, value]
aov = pg.rm_anova(data=long_df, dv='alpha_power', within='condition',
                   subject='subject_id', detailed=True, correction=True)
print(aov[['Source', 'F', 'p-unc', 'p-GG-corr', 'np2']].to_string())
# np2 = partial eta-squared; GG = Greenhouse-Geisser sphericity correction

# Post-hoc pairwise for rm_anova
posthoc = pg.pairwise_tests(data=long_df, dv='alpha_power',
                              within='condition', subject='subject_id',
                              padjust='bonf')  # or 'fdr_bh'
print(posthoc[['A', 'B', 'T', 'p-unc', 'p-corr', 'cohen-d']].to_string())

# Kruskal-Wallis (non-parametric one-way ANOVA)
stat, p = stats.kruskal(group1, group2, group3)
# Post-hoc: Dunn's test
posthoc = pg.pairwise_tests(data=long_df, dv='value', between='group',
                              parametric=False, padjust='bonf')


# ─── Correlation ──────────────────────────────────────────────────────────────

# Pearson (linear, normal data)
r, p = stats.pearsonr(x, y)
n = len(x)
# 95% CI via Fisher z-transform
z = np.arctanh(r)
se = 1 / np.sqrt(n - 3)
ci_low, ci_high = np.tanh(z - 1.96*se), np.tanh(z + 1.96*se)
print(f"Pearson r={r:.3f}, p={p:.4f}, 95% CI [{ci_low:.3f}, {ci_high:.3f}]")

# Spearman (non-linear or non-normal)
rho, p = stats.spearmanr(x, y)

# Partial correlation (controlling for confound z)
result = pg.partial_corr(data=df, x='alpha_power', y='reaction_time', covar='age')

# Point-biserial (continuous vs. binary)
r, p = stats.pointbiserialr(binary_group, continuous_measure)


# ─── Multiple Comparisons Correction ─────────────────────────────────────────

from statsmodels.stats.multitest import multipletests

p_values = np.array([0.01, 0.03, 0.05, 0.001, 0.2])  # from multiple tests

# FDR (Benjamini-Hochberg) — preferred for exploratory EEG
reject, p_corrected, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')

# Bonferroni — preferred for confirmatory, few comparisons
reject, p_corrected, _, _ = multipletests(p_values, alpha=0.05, method='bonferroni')

# FWE permutation (for channel × time mass univariate — see Section 4.2)
# Use mne.stats.permutation_cluster_test — handles spatial correlation correctly

print(f"Significant after FDR: {reject.sum()} / {len(p_values)}")
print(f"Corrected p-values: {p_corrected.round(4)}")


# ─── Effect Sizes — Always Report These ──────────────────────────────────────

# Cohen's d (for t-tests)
# Small: 0.2, Medium: 0.5, Large: 0.8
d = pg.compute_effsize(group_A, group_B, eftype='cohen')

# Eta-squared / partial eta-squared (for ANOVA)
# Small: 0.01, Medium: 0.06, Large: 0.14

# Pearson r (for correlations)
# Small: 0.1, Medium: 0.3, Large: 0.5

# Rank-biserial r (for non-parametric tests)
# Compute from Mann-Whitney or Wilcoxon statistics as shown above

# Hedges' g (Cohen's d corrected for small samples — use when n < 20 per group)
g = pg.compute_effsize(group_A, group_B, eftype='hedges')
```

---

### 16.5 What to Plot — Visualization Reference by Analysis Type

This is the primary reference for which plot to generate for each analytical question. Always visualize before and after the statistical test.

#### Distribution Plots

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ── Histogram: understand the raw distribution of one variable ──────────────
# Use for: checking normality, identifying outliers, seeing bimodality
fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(alpha_power, bins=30, edgecolor='white', color='steelblue', alpha=0.8)
ax.axvline(np.mean(alpha_power), color='red', linestyle='--', label='Mean')
ax.axvline(np.median(alpha_power), color='orange', linestyle='--', label='Median')
ax.set_xlabel('Alpha Power (log µV²/Hz)')
ax.set_ylabel('Count')
ax.legend()
# Rule: if mean and median diverge visibly → skewed → log-transform or non-parametric

# ── Violin Plot: compare distributions across conditions/groups ─────────────
# Use for: group comparisons. Shows full distribution, not just quartiles.
# PREFER over bar plots. Always pair with individual data points.
fig, ax = plt.subplots(figsize=(8, 5))
sns.violinplot(data=long_df, x='condition', y='alpha_power',
               inner='box', palette='Set2', ax=ax)
# Overlay individual subject means
sns.stripplot(data=long_df, x='condition', y='alpha_power',
              color='black', size=4, alpha=0.5, jitter=True, ax=ax)
ax.set_ylabel('Alpha Power (log µV²/Hz)')

# ── Box Plot: compact distribution comparison ────────────────────────────────
# Use for: many groups, publication figures where space is limited
# Always show individual data points on top (strip or swarm plot)
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=long_df, x='condition', y='alpha_power',
            palette='Set2', width=0.5, ax=ax)
sns.swarmplot(data=long_df, x='condition', y='alpha_power',
              color='black', size=3, alpha=0.6, ax=ax)

# ── Raincloud Plot: best of violin + box + strip ─────────────────────────────
# Use for: final publication figures combining all distribution information
# Requires: pip install ptitprince
import ptitprince as pt
pt.RainCloud(data=long_df, x='condition', y='alpha_power',
             palette='Set2', bw=0.2, width_viol=0.6, ax=ax,
             orient='h', alpha=0.65, dodge=True)
```

#### Correlation and Relationship Plots

```python
# ── Scatter Plot with Regression Line: two continuous variables ──────────────
# Use for: EEG feature vs. behavioral measure (RT, accuracy, age)
fig, ax = plt.subplots(figsize=(6, 5))
ax.scatter(reaction_times, alpha_power, alpha=0.6, s=40, color='steelblue')
# Regression line with 95% CI
slope, intercept, r, p, se = stats.linregress(reaction_times, alpha_power)
x_line = np.linspace(reaction_times.min(), reaction_times.max(), 100)
ax.plot(x_line, slope * x_line + intercept, color='red', linewidth=2)
ax.fill_between(x_line,
                (slope * x_line + intercept) - 1.96 * se * np.sqrt(len(reaction_times)),
                (slope * x_line + intercept) + 1.96 * se * np.sqrt(len(reaction_times)),
                alpha=0.15, color='red')
ax.set_xlabel('Reaction Time (ms)')
ax.set_ylabel('Alpha Power (log µV²/Hz)')
ax.text(0.05, 0.95, f'r={r:.3f}, p={p:.3f}', transform=ax.transAxes,
        verticalalignment='top', fontsize=11)

# ── Correlation Matrix: pairwise relationships across multiple features ───────
# Use for: feature selection, collinearity check before regression, EEG connectivity
corr_matrix = feature_df.corr(method='spearman')  # spearman for robustness
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)  # upper triangle only

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            square=True, linewidths=0.5, ax=ax)
ax.set_title('Spearman Correlation Matrix')
# Important: compute p-values for each pair and mask non-significant correlations
from scipy.stats import spearmanr
corr_p = np.zeros_like(corr_matrix.values)
for i in range(corr_matrix.shape[0]):
    for j in range(corr_matrix.shape[1]):
        if i != j:
            _, corr_p[i, j] = spearmanr(
                feature_df.iloc[:, i].dropna(),
                feature_df.iloc[:, j].dropna()
            )
# Mask non-significant cells
sig_mask = (corr_p > 0.05) | mask
sns.heatmap(corr_matrix, mask=sig_mask | mask, cmap='RdBu_r',
            center=0, annot=True, fmt='.2f', ax=ax, alpha=0.5)

# ── Pair Plot: all pairwise scatter plots across several features ─────────────
# Use for: exploratory analysis of a small feature set (<10 features)
g = sns.pairplot(feature_df[['alpha_power', 'beta_power', 'theta_power', 'RT']],
                  hue='condition', diag_kind='kde', plot_kws={'alpha': 0.4})
```

#### Time-Series and Cross-Correlation Plots

```python
# ── Cross-Correlation: lag relationship between two time series ───────────────
# Use for: EEG feature vs. behavioral time series, EEG-EMG, inter-channel coupling
from scipy.signal import correlate, correlation_lags

def plot_cross_correlation(x: np.ndarray, y: np.ndarray,
                            sfreq: float, max_lag_sec: float = 1.0,
                            labels: tuple = ('Signal 1', 'Signal 2')):
    """
    Normalized cross-correlation between two same-length signals.
    Positive lag: y leads x. Negative lag: x leads y.
    """
    # Normalize before cross-correlation
    x_norm = (x - x.mean()) / (x.std() * len(x))
    y_norm = (y - y.mean()) / y.std()

    xcorr = correlate(x_norm, y_norm, mode='full')
    lags = correlation_lags(len(x), len(y), mode='full') / sfreq  # in seconds

    # Crop to max_lag_sec
    lag_mask = np.abs(lags) <= max_lag_sec
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(lags[lag_mask], xcorr[lag_mask], color='steelblue')
    ax.axvline(0, color='black', linestyle='--', alpha=0.5)
    ax.axhline(0, color='gray', linestyle='--', alpha=0.3)

    # Mark peak
    peak_idx = np.argmax(np.abs(xcorr[lag_mask]))
    peak_lag = lags[lag_mask][peak_idx]
    peak_val = xcorr[lag_mask][peak_idx]
    ax.scatter([peak_lag], [peak_val], color='red', zorder=5, s=60)
    ax.annotate(f'Peak: {peak_lag*1000:.1f} ms', xy=(peak_lag, peak_val),
                xytext=(peak_lag + 0.05, peak_val), fontsize=9)

    # Significance threshold (approximate: 2/sqrt(N))
    sig_thresh = 2 / np.sqrt(len(x))
    ax.axhline(sig_thresh, color='red', linestyle=':', alpha=0.5, label='p≈0.05 threshold')
    ax.axhline(-sig_thresh, color='red', linestyle=':', alpha=0.5)

    ax.set_xlabel('Lag (s)')
    ax.set_ylabel('Cross-correlation')
    ax.set_title(f'Cross-correlation: {labels[0]} vs {labels[1]}')
    ax.legend()
    return fig


# ── Auto-Correlation: detect periodicity in a single EEG-derived time series ──
# Use for: checking non-stationarity, verifying independence assumption for ML
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
plot_acf(alpha_power_timeseries, lags=50, ax=ax1)
plot_pacf(alpha_power_timeseries, lags=50, ax=ax2)
ax1.set_title('Autocorrelation Function (ACF)')
ax2.set_title('Partial Autocorrelation Function (PACF)')
# If ACF decays slowly → strong autocorrelation → cannot use i.i.d. ML assumptions
# without temporal blocking in cross-validation
```

#### Group Comparison Plots

```python
# ── Bar Plot with Error Bars (use sparingly — prefer violin) ──────────────────
# Acceptable for: mean ± SEM across subjects when n is large and distribution is normal
# ALWAYS show the individual subject means on top
group_means = long_df.groupby('condition')['alpha_power'].mean()
group_sems  = long_df.groupby('condition')['alpha_power'].sem()

fig, ax = plt.subplots(figsize=(6, 5))
bars = ax.bar(group_means.index, group_means.values,
               yerr=group_sems.values, capsize=5,
               color=['steelblue', 'coral'], alpha=0.7, edgecolor='black')
# Individual subject lines (shows paired structure)
subjects = long_df['subject_id'].unique()
for subj in subjects:
    subj_data = long_df[long_df['subject_id'] == subj].set_index('condition')
    ax.plot(subj_data.index, subj_data['alpha_power'],
            color='gray', alpha=0.3, linewidth=1, marker='o', markersize=3)
ax.set_ylabel('Alpha Power (log µV²/Hz)')

# ── Significance Brackets: annotating p-values on group comparison plots ───────
# Use statannotations library for clean brackets
from statannotations.Annotator import Annotator

pairs = [('condition_A', 'condition_B'), ('condition_A', 'condition_C')]
annotator = Annotator(ax, pairs, data=long_df, x='condition', y='alpha_power')
annotator.configure(test='Wilcoxon', text_format='star',
                    loc='inside', verbose=2)
annotator.apply_and_annotate()
```

#### EEG-Specific Diagnostic Plots

```python
# ── ERP with Single-Trial Overlay (best for ERP quality evaluation) ──────────
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Top: single trials as light lines, mean as thick line
single_trials = epochs['target'].get_data(picks='Pz').squeeze() * 1e6
times = epochs.times * 1000  # to ms
for trial in single_trials:
    axes[0].plot(times, trial, color='steelblue', alpha=0.05, linewidth=0.5)
axes[0].plot(times, single_trials.mean(axis=0), color='navy', linewidth=2, label='Mean ERP')
axes[0].axvline(0, color='black', linestyle='--')
axes[0].axhline(0, color='gray', linestyle='--', alpha=0.5)
axes[0].set_ylabel('Amplitude (µV)')
axes[0].legend()

# Bottom: epoch image (trial × time heatmap, sorted by RT)
sort_order = np.argsort(trial_data['reaction_time_ms'].values)
im = axes[1].imshow(single_trials[sort_order],
                     aspect='auto', origin='lower',
                     extent=[times[0], times[-1], 0, len(sort_order)],
                     cmap='RdBu_r', vmin=-15, vmax=15)
plt.colorbar(im, ax=axes[1], label='µV')
axes[1].set_xlabel('Time (ms)')
axes[1].set_ylabel('Trial (sorted by RT)')
axes[1].axvline(0, color='black', linestyle='--')

# ── Power Spectrum + FOOOF Fit: PSD with aperiodic and peak decomposition ────
from fooof import FOOOF

fm = FOOOF(peak_width_limits=[1, 8], max_n_peaks=6, aperiodic_mode='fixed')
fm.fit(freqs, psd_1d, freq_range=[1, 40])
fm.plot(plot_peaks='shade', add_legend=True)
# Shows: raw PSD (black), aperiodic fit (blue dashed), peaks (shaded)
```

---

### 16.6 Regression and Linear Modeling

```python
# ── Simple Linear Regression ─────────────────────────────────────────────────
slope, intercept, r, p, se = stats.linregress(x, y)
print(f"y = {slope:.4f}x + {intercept:.4f}")
print(f"R²={r**2:.4f}, p={p:.4f}")

# ── Multiple Linear Regression (pingouin) ────────────────────────────────────
result = pg.linear_regression(
    X=df[['alpha_power', 'beta_power', 'age', 'sex']],
    y=df['reaction_time_ms'],
    relimp=True  # computes relative importance of each predictor
)
print(result[['names', 'coef', 'se', 'T', 'pval', 'CI[2.5%]', 'CI[97.5%]', 'r2']].to_string())

# ── Multiple Regression (statsmodels — for detailed diagnostics) ─────────────
import statsmodels.api as sm
X = sm.add_constant(df[['alpha_power', 'beta_power', 'age']])
model = sm.OLS(df['reaction_time_ms'], X).fit()
print(model.summary())

# Diagnostic plots for regression assumptions
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
# 1. Residuals vs Fitted (check linearity and homoscedasticity)
axes[0,0].scatter(model.fittedvalues, model.resid, alpha=0.5)
axes[0,0].axhline(0, color='red', linestyle='--')
axes[0,0].set_xlabel('Fitted values'); axes[0,0].set_ylabel('Residuals')
# 2. Q-Q plot of residuals
stats.probplot(model.resid, plot=axes[0,1])
# 3. Scale-Location plot
axes[1,0].scatter(model.fittedvalues, np.sqrt(np.abs(model.resid)), alpha=0.5)
axes[1,0].set_xlabel('Fitted values'); axes[1,0].set_ylabel('√|Residuals|')
# 4. Residuals vs Leverage
sm.graphics.influence_plot(model, ax=axes[1,1])
plt.tight_layout()

# ── Mixed-Effects Model (for repeated-measures data) ─────────────────────────
# When you have: multiple observations per subject, trial-level predictors
import statsmodels.formula.api as smf

# Random intercept model (each subject has their own baseline)
lme = smf.mixedlm(
    "alpha_power ~ condition + time_in_session + age",
    data=long_df,
    groups=long_df['subject_id'],    # random intercept per subject
    exog_re=long_df[['condition']]  # optional: random slope for condition
)
result = lme.fit()
print(result.summary())
```

---

### 16.7 Summary Statistics — Standard Reporting Format

```python
def summarize_eeg_feature(data_by_group: dict[str, np.ndarray],
                            feature_name: str) -> pd.DataFrame:
    """
    Produces a publication-ready summary table for an EEG feature across groups.
    data_by_group: {'condition_A': array, 'condition_B': array, ...}
    """
    rows = []
    for group_name, values in data_by_group.items():
        values = np.array(values)
        valid = values[~np.isnan(values)]
        rows.append({
            'Group': group_name,
            'N': len(valid),
            'Mean': np.mean(valid),
            'SD': np.std(valid, ddof=1),
            'SEM': stats.sem(valid),
            'Median': np.median(valid),
            'IQR_25': np.percentile(valid, 25),
            'IQR_75': np.percentile(valid, 75),
            'Min': np.min(valid),
            'Max': np.max(valid),
            'Skewness': stats.skew(valid),
            'Kurtosis': stats.kurtosis(valid),
            'Normal (p>0.05)': stats.shapiro(valid)[1] > 0.05 if len(valid) >= 3 else None,
        })
    df = pd.DataFrame(rows).set_index('Group')
    print(f"\n=== {feature_name} ===")
    print(df.round(4).to_string())
    return df
```

---

## 17. SCIKIT-LEARN MODELING — COMPLETE GUIDE FOR EEG

This section provides everything Claude needs to build rigorous, properly validated machine learning models from EEG features using scikit-learn — from feature preparation through hyperparameter tuning and result reporting.

---

### 17.1 The Modeling Mindset for EEG

Before building any sklearn model, answer these questions:

- **What is the target?** Classification (discrete states) or regression (continuous behavioral variable)?
- **What is the sample size?** Number of trials × subjects. EEG datasets are often small (<500 trials).
- **Is the data balanced?** Class imbalance is the rule in EEG, not the exception.
- **Is the data i.i.d.?** EEG trials are autocorrelated — random splits inflate accuracy. Use temporal or subject-based splits.
- **What features?** Band power (established, interpretable), covariance matrices (Riemannian), raw epochs (deep learning), or handcrafted time-domain features?
- **Do you need to generalize across subjects?** If yes, within-subject pipelines are insufficient.

---

### 17.2 Feature Preparation — The Right Way

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import (
    StandardScaler, RobustScaler, PowerTransformer,
    FunctionTransformer, LabelEncoder
)
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# ── Choosing the Right Scaler ─────────────────────────────────────────────────

# StandardScaler: zero mean, unit variance
# Use for: normally distributed features, SVM, LDA, logistic regression
# DON'T use for: heavily skewed features without log-transform first

# RobustScaler: median and IQR-based scaling
# Use for: features with outliers (common in EEG — artifact epochs that survived)
# Better than StandardScaler for EEG amplitude features

# PowerTransformer (Yeo-Johnson): makes features more Gaussian
# Use for: when you need normality (e.g., before LDA which assumes Gaussian features)
# Yeo-Johnson handles zeros and negatives (unlike Box-Cox)

# FunctionTransformer for log-transform of PSD:
log_scaler = FunctionTransformer(func=np.log10,
                                  inverse_func=lambda x: 10**x,
                                  validate=True)

# ── Handling Missing Values ───────────────────────────────────────────────────
# EEG features can be NaN from: bad epochs, missing channels, failed spectral windows

imputer = SimpleImputer(strategy='median')  # median is robust to outliers
# NEVER use mean imputation without checking for outliers
# For channel-specific features: impute per channel, not across all features
# If >30% missing in a feature column: drop the column, don't impute

# ── Feature Selection Before Modeling ────────────────────────────────────────
from sklearn.feature_selection import (
    SelectKBest, f_classif, mutual_info_classif,
    VarianceThreshold, RFECV
)

# Step 1: Remove near-zero variance features (channels with constant power)
selector_var = VarianceThreshold(threshold=0.01)

# Step 2: Univariate filter (for initial dimensionality reduction)
# f_classif: ANOVA F-value (assumes normality)
# mutual_info_classif: non-parametric, handles non-linear relationships
selector_k = SelectKBest(score_func=mutual_info_classif, k=50)

# Step 3: Recursive feature elimination with cross-validation (expensive but thorough)
from sklearn.svm import SVC
rfecv = RFECV(estimator=SVC(kernel='linear'), step=1, cv=5, scoring='balanced_accuracy')
```

---

### 17.3 Building Sklearn Pipelines — The Correct Pattern

Always use `Pipeline` so that all preprocessing steps are properly scoped inside cross-validation. This is the most important sklearn practice for EEG.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, PowerTransformer, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    StratifiedKFold, GroupKFold, LeaveOneGroupOut,
    cross_validate, GridSearchCV, RandomizedSearchCV
)
import numpy as np

# ── Canonical EEG Classification Pipeline ────────────────────────────────────

def build_eeg_pipeline(clf_name: str = 'svm') -> Pipeline:
    """
    Returns a complete, leak-proof sklearn pipeline for EEG band power features.
    All steps are inside the pipeline — nothing is fit outside.
    """
    classifiers = {
        'lda': LinearDiscriminantAnalysis(solver='svd'),
        'svm': SVC(kernel='rbf', C=1.0, gamma='scale', probability=True),
        'svm_linear': SVC(kernel='linear', C=0.1, probability=True),
        'rf': RandomForestClassifier(n_estimators=200, max_depth=5,
                                      class_weight='balanced', random_state=42),
        'lr': LogisticRegression(C=0.1, max_iter=1000, class_weight='balanced',
                                  solver='lbfgs', multi_class='auto'),
        'gb': GradientBoostingClassifier(n_estimators=100, max_depth=3,
                                          learning_rate=0.1, random_state=42),
    }

    return Pipeline([
        ('impute',    SimpleImputer(strategy='median')),
        ('log',       FunctionTransformer(np.log10)),   # for PSD features
        ('scale',     RobustScaler()),
        ('select',    SelectKBest(mutual_info_classif, k=50)),
        ('clf',       classifiers[clf_name])
    ])

# ── Regression Pipeline ───────────────────────────────────────────────────────
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor

def build_eeg_regression_pipeline(model_name: str = 'ridge') -> Pipeline:
    regressors = {
        'ridge':    Ridge(alpha=1.0),
        'lasso':    Lasso(alpha=0.01, max_iter=5000),
        'elastic':  ElasticNet(alpha=0.01, l1_ratio=0.5, max_iter=5000),
        'rf':       RandomForestRegressor(n_estimators=200, max_depth=5, random_state=42),
    }
    return Pipeline([
        ('impute', SimpleImputer(strategy='median')),
        ('log',    FunctionTransformer(np.log10)),
        ('scale',  RobustScaler()),
        ('select', SelectKBest(score_func=lambda X, y: (
            np.abs(np.corrcoef(X.T, y)[-1, :-1]), np.zeros(X.shape[1])
        ), k=30)),
        ('reg',    regressors[model_name])
    ])
```

---

### 17.4 Cross-Validation — The EEG-Correct Approach

```python
from sklearn.model_selection import (
    StratifiedKFold, GroupKFold, LeaveOneGroupOut, cross_validate
)
from sklearn.metrics import make_scorer, balanced_accuracy_score, f1_score
import pandas as pd

# ── Define Scorers (always more than one) ────────────────────────────────────
scorers = {
    'balanced_accuracy': make_scorer(balanced_accuracy_score),
    'f1_macro':          make_scorer(f1_score, average='macro'),
    'roc_auc':           'roc_auc',  # only for binary
}

# ── Within-Subject CV: trials from one subject ───────────────────────────────
# CRITICAL: use StratifiedKFold but split by BLOCK, not randomly
# If your data has temporal structure (trials 1-50 from block 1, 51-100 block 2),
# use GroupKFold with block_ids as groups to avoid temporal leakage

def within_subject_cv(X: np.ndarray, y: np.ndarray,
                       block_ids: np.ndarray,
                       pipeline: Pipeline) -> pd.DataFrame:
    """
    Proper within-subject CV splitting by experimental block.
    block_ids: integer array indicating which block each trial belongs to.
    """
    cv = GroupKFold(n_splits=len(np.unique(block_ids)))
    results = cross_validate(
        pipeline, X, y,
        cv=cv.split(X, y, groups=block_ids),
        scoring=scorers,
        return_train_score=True,
        return_estimator=True,
        n_jobs=-1
    )
    return pd.DataFrame(results)


# ── Cross-Subject CV: leave-one-subject-out ───────────────────────────────────
def cross_subject_cv(X: np.ndarray, y: np.ndarray,
                      subject_ids: np.ndarray,
                      pipeline: Pipeline) -> pd.DataFrame:
    """
    True cross-subject generalization via LOSO-CV.
    This is the only valid metric for claims of cross-subject generalization.
    """
    loso = LeaveOneGroupOut()
    results = cross_validate(
        pipeline, X, y,
        cv=loso.split(X, y, groups=subject_ids),
        scoring=scorers,
        return_train_score=True,
        n_jobs=-1
    )
    df = pd.DataFrame(results)
    print(f"\nCross-Subject LOSO Results ({len(np.unique(subject_ids))} subjects):")
    for metric in ['test_balanced_accuracy', 'test_f1_macro']:
        if metric in df.columns:
            vals = df[metric]
            print(f"  {metric}: {vals.mean():.3f} ± {vals.std():.3f} "
                  f"[min={vals.min():.3f}, max={vals.max():.3f}]")
    return df


# ── Nested CV: hyperparameter tuning + evaluation (prevents optimistic bias) ──
def nested_cv(X: np.ndarray, y: np.ndarray,
               subject_ids: np.ndarray,
               pipeline: Pipeline,
               param_grid: dict) -> dict:
    """
    Outer loop: LOSO for unbiased performance estimate.
    Inner loop: StratifiedKFold for hyperparameter tuning.
    This is the gold standard — prevents using the test set for tuning.
    """
    outer_cv = LeaveOneGroupOut()
    outer_scores = []
    best_params_list = []

    for train_idx, test_idx in outer_cv.split(X, y, groups=subject_ids):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        # Inner CV for hyperparameter selection
        inner_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        search = RandomizedSearchCV(
            pipeline, param_grid, n_iter=50,
            cv=inner_cv, scoring='balanced_accuracy',
            n_jobs=-1, random_state=42, refit=True
        )
        search.fit(X_train, y_train)

        # Evaluate best model on held-out subject
        score = balanced_accuracy_score(y_test, search.predict(X_test))
        outer_scores.append(score)
        best_params_list.append(search.best_params_)

    print(f"\nNested CV Balanced Accuracy: {np.mean(outer_scores):.3f} ± {np.std(outer_scores):.3f}")
    return {'scores': outer_scores, 'best_params': best_params_list}
```

---

### 17.5 Hyperparameter Tuning Reference

```python
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from scipy.stats import loguniform, randint, uniform

# ── Parameter Grids for Common EEG Classifiers ───────────────────────────────

# SVM — most common EEG classifier
svm_param_grid = {
    'clf__C':     loguniform(1e-3, 1e3),      # regularization strength
    'clf__gamma': ['scale', 'auto'] + list(loguniform(1e-4, 1e0).rvs(10)),
    'clf__kernel': ['rbf', 'linear'],
    'select__k':  [20, 50, 100, 'all'],
}

# LDA — excellent for ERP and band-power features
lda_param_grid = {
    'clf__solver':    ['svd', 'lsqr', 'eigen'],
    'clf__shrinkage': [None, 'auto'] + list(uniform(0, 1).rvs(10)),
    'select__k':      [20, 50, 100, 'all'],
}

# Random Forest — good for mixed feature types
rf_param_grid = {
    'clf__n_estimators': [100, 200, 500],
    'clf__max_depth':    [3, 5, 10, None],
    'clf__min_samples_leaf': [1, 5, 10],
    'clf__max_features': ['sqrt', 'log2', 0.3],
    'select__k': [30, 60, 100],
}

# ── Running Hyperparameter Search ────────────────────────────────────────────

pipeline = build_eeg_pipeline('svm')
inner_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

search = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=svm_param_grid,
    n_iter=100,                      # number of random combinations to try
    cv=inner_cv,
    scoring='balanced_accuracy',
    refit=True,                      # refit best model on full training set
    n_jobs=-1,
    verbose=1,
    random_state=42
)
search.fit(X_train, y_train)

print(f"Best params: {search.best_params_}")
print(f"Best CV score: {search.best_score_:.4f}")

# Visualize hyperparameter search results
import pandas as pd
cv_results = pd.DataFrame(search.cv_results_)
cv_results_sorted = cv_results.sort_values('mean_test_score', ascending=False)
print(cv_results_sorted[['params', 'mean_test_score', 'std_test_score']].head(10))
```

---

### 17.6 Model Evaluation — Complete Metrics Reference

```python
from sklearn.metrics import (
    classification_report, confusion_matrix, ConfusionMatrixDisplay,
    roc_curve, auc, precision_recall_curve,
    balanced_accuracy_score, f1_score, cohen_kappa_score,
    r2_score, mean_absolute_error, mean_squared_error
)
import matplotlib.pyplot as plt
import numpy as np

def full_classification_report(y_true, y_pred, y_prob=None,
                                 class_names=None, title='') -> dict:
    """Complete evaluation for an EEG classifier."""
    print(f"\n{'='*60}")
    print(f"  CLASSIFICATION RESULTS: {title}")
    print(f"{'='*60}")

    # Basic metrics
    print(classification_report(y_true, y_pred, target_names=class_names, digits=4))
    ba = balanced_accuracy_score(y_true, y_pred)
    kappa = cohen_kappa_score(y_true, y_pred)
    print(f"Balanced Accuracy: {ba:.4f}")
    print(f"Cohen's Kappa:     {kappa:.4f}")

    # Confusion matrix
    fig, axes = plt.subplots(1, 2 if y_prob is not None else 1,
                              figsize=(12 if y_prob is not None else 5, 5))
    if y_prob is None:
        axes = [axes]

    cm = confusion_matrix(y_true, y_pred, normalize='true')
    ConfusionMatrixDisplay(cm, display_labels=class_names).plot(ax=axes[0], cmap='Blues')
    axes[0].set_title('Confusion Matrix (normalized)')

    # ROC curve (binary) or per-class (multiclass)
    if y_prob is not None:
        if y_prob.ndim == 1 or y_prob.shape[1] == 2:
            # Binary
            prob_pos = y_prob if y_prob.ndim == 1 else y_prob[:, 1]
            fpr, tpr, _ = roc_curve(y_true, prob_pos)
            roc_auc = auc(fpr, tpr)
            prec, rec, _ = precision_recall_curve(y_true, prob_pos)
            pr_auc = auc(rec, prec)

            axes[1].plot(fpr, tpr, color='steelblue', lw=2,
                          label=f'ROC (AUC={roc_auc:.3f})')
            axes[1].plot([0,1], [0,1], 'k--', alpha=0.3)
            axes[1].set_xlabel('False Positive Rate')
            axes[1].set_ylabel('True Positive Rate')
            axes[1].set_title('ROC Curve')
            axes[1].legend()
            print(f"AUC-ROC: {roc_auc:.4f}")
            print(f"AUC-PR:  {pr_auc:.4f}")

    plt.tight_layout()
    return {'balanced_accuracy': ba, 'kappa': kappa}


def full_regression_report(y_true, y_pred, feature_names=None,
                             model=None, title='') -> dict:
    """Complete evaluation for an EEG regression model (e.g., predicting RT)."""
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r, p = stats.pearsonr(y_true, y_pred)

    print(f"\n=== REGRESSION: {title} ===")
    print(f"R²={r2:.4f}, MAE={mae:.3f}, RMSE={rmse:.3f}")
    print(f"Pearson r={r:.4f}, p={p:.4f}")

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Predicted vs. Actual
    axes[0].scatter(y_true, y_pred, alpha=0.5, s=30)
    lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
    axes[0].plot(lims, lims, 'r--', label='Perfect prediction')
    axes[0].set_xlabel('True values'); axes[0].set_ylabel('Predicted values')
    axes[0].set_title(f'Predicted vs Actual (R²={r2:.3f})')
    axes[0].legend()

    # Residuals vs. Predicted (homoscedasticity check)
    residuals = y_true - y_pred
    axes[1].scatter(y_pred, residuals, alpha=0.5, s=30)
    axes[1].axhline(0, color='red', linestyle='--')
    axes[1].set_xlabel('Predicted values'); axes[1].set_ylabel('Residuals')
    axes[1].set_title('Residuals vs Predicted')

    # Residual distribution
    axes[2].hist(residuals, bins=30, edgecolor='white', color='steelblue', alpha=0.8)
    axes[2].set_xlabel('Residual'); axes[2].set_title('Residual Distribution')

    plt.tight_layout()
    return {'r2': r2, 'mae': mae, 'rmse': rmse, 'pearson_r': r}
```

---

### 17.7 Feature Importance and Interpretability

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ── Random Forest / Tree-Based Feature Importance ────────────────────────────
def plot_feature_importance(model, feature_names: list, top_n: int = 30,
                              title: str = 'Feature Importance') -> pd.DataFrame:
    """Works for RandomForest, GradientBoosting, ExtraTrees."""
    # Extract from pipeline if needed
    clf = model.named_steps.get('clf', model)
    importances = clf.feature_importances_

    # If SelectKBest was in the pipeline, map back to original feature names
    if 'select' in model.named_steps:
        selector = model.named_steps['select']
        selected_mask = selector.get_support()
        selected_features = np.array(feature_names)[selected_mask]
    else:
        selected_features = np.array(feature_names)

    fi_df = pd.DataFrame({
        'feature': selected_features,
        'importance': importances,
        'std': getattr(clf, 'estimators_', [clf]) and
               np.std([est.feature_importances_ for est in getattr(clf, 'estimators_', [])],
                       axis=0) if hasattr(clf, 'estimators_') else np.zeros_like(importances)
    }).sort_values('importance', ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=(8, top_n * 0.3 + 2))
    ax.barh(fi_df['feature'][::-1], fi_df['importance'][::-1],
             xerr=fi_df['std'][::-1] if fi_df['std'].sum() > 0 else None,
             color='steelblue', alpha=0.8)
    ax.set_xlabel('Importance')
    ax.set_title(title)
    plt.tight_layout()
    return fi_df


# ── Permutation Importance (model-agnostic, more reliable than built-in) ─────
from sklearn.inspection import permutation_importance

perm = permutation_importance(
    model, X_test, y_test,
    n_repeats=30,
    scoring='balanced_accuracy',
    random_state=42,
    n_jobs=-1
)
perm_df = pd.DataFrame({
    'feature': feature_names,
    'importance_mean': perm.importances_mean,
    'importance_std':  perm.importances_std,
}).sort_values('importance_mean', ascending=False)
print(perm_df.head(20).to_string())


# ── SVM Linear Weights as Feature Importance ──────────────────────────────────
# For linear SVM: coefficients represent discriminative weight per feature
# For binary: one weight vector. For multiclass (OvO): one per pair.
clf = model.named_steps['clf']
if hasattr(clf, 'coef_'):
    weights = clf.coef_.squeeze()
    # Map back through SelectKBest mask
    selector_mask = model.named_steps['select'].get_support()
    all_weights = np.zeros(len(feature_names))
    all_weights[selector_mask] = weights

    # EEG-specific: reshape weights to (n_channels, n_bands) and plot as topomap
    n_channels = 64; n_bands = 4  # example
    weight_matrix = all_weights[:n_channels * n_bands].reshape(n_channels, n_bands)

    fig, axes = plt.subplots(1, n_bands, figsize=(16, 4))
    band_names = ['theta', 'alpha', 'beta', 'gamma']
    for bi, (ax, band) in enumerate(zip(axes, band_names)):
        mne.viz.plot_topomap(weight_matrix[:, bi], epochs.info,
                              axes=ax, show=False, cmap='RdBu_r')
        ax.set_title(f'SVM weights: {band}')
    plt.suptitle('SVM Linear Weights — Spatial Distribution')
    plt.tight_layout()


# ── SHAP Values (best general interpretability tool) ─────────────────────────
# pip install shap
import shap

# For tree models (fast)
explainer = shap.TreeExplainer(model.named_steps['clf'])
X_transformed = model[:-1].transform(X_test)
shap_values = explainer.shap_values(X_transformed)

# Summary plot: feature importance + direction of effect
shap.summary_plot(shap_values, X_transformed,
                   feature_names=[f for f, m in zip(feature_names,
                                   model.named_steps['select'].get_support()) if m])

# For linear models (fast)
explainer = shap.LinearExplainer(model.named_steps['clf'], X_transformed)
shap_values = explainer.shap_values(X_transformed)
shap.summary_plot(shap_values, X_transformed)
```

---

### 17.8 Common Sklearn Models — When to Use Each for EEG

|Model|When to use|When NOT to use|Key hyperparameters|
|---|---|---|---|
|`LinearDiscriminantAnalysis`|ERP features, band power, small samples (<200), interpretable spatial filters|Non-linearly separable data, very high-dimensional features|`solver`, `shrinkage` (set to 'auto' always)|
|`SVC(kernel='rbf')`|Best general-purpose for EEG features, works well with ~50–200 samples per class|Very large datasets (slow), when interpretability required|`C` (try log-range 0.001–1000), `gamma='scale'`|
|`SVC(kernel='linear')`|When you need weights for neurological interpretation (spatial filter equivalent)|Non-linear class boundaries|`C` (try 0.001–10)|
|`LogisticRegression`|Binary classification, probability outputs needed, regularization important|Many correlated features without prior dimensionality reduction|`C`, `solver='lbfgs'`, `class_weight='balanced'`|
|`RandomForestClassifier`|Mixed feature types, automatic feature selection, robust to outliers|Small samples (<100 trials), when interpretability via weights needed|`n_estimators` (≥200), `max_depth` (3–10), `max_features`|
|`GradientBoostingClassifier`|Best accuracy on tabular EEG features with enough data (>500 trials)|Small datasets (overfits), real-time (slow inference)|`n_estimators`, `max_depth` (3–5), `learning_rate`|
|`Ridge / Lasso`|Regression (predicting RT, score), when features > samples|Classification tasks|`alpha` (regularization strength, log-scale search)|
|`MDM` (pyRiemann)|Covariance matrix input, motor imagery, cross-subject|When covariances are not positive definite (bad data)|Riemannian metric choice|

---

### 17.9 Sklearn Dos and Don'ts for EEG

|✅ DO|❌ DON'T|
|---|---|
|Put ALL preprocessing inside a `Pipeline`|Fit any preprocessing step outside the cross-validation loop|
|Use `GroupKFold` or `LeaveOneGroupOut` for EEG splits|Use `StratifiedKFold` with random shuffle on temporal EEG data|
|Use `class_weight='balanced'` for imbalanced datasets|Use default class weights and report accuracy as the metric|
|Use `RandomizedSearchCV` (not `GridSearchCV`) for large search spaces|Exhaustively grid search over many hyperparameters (overfits)|
|Use nested CV (outer evaluation + inner tuning)|Tune hyperparameters on same fold used for final score|
|Use `balanced_accuracy_score` as primary metric|Use `accuracy_score` on imbalanced EEG class distributions|
|Report mean ± std across folds, plus individual fold scores|Report only mean accuracy across folds|
|Use permutation importance (not built-in tree importance) for unbiased feature importance|Trust built-in feature_importances_ alone (biased toward high-cardinality features)|
|Apply `RobustScaler` before SVM to handle EEG outliers|Apply `StandardScaler` to raw amplitude features with outliers|
|Set `random_state` in all stochastic components|Leave random state unset (irreproducible results)|
|Use `PowerTransformer` or log-transform before LDA|Feed raw (non-Gaussian) PSD values to LDA (violates assumptions)|
|Plot learning curves to diagnose overfitting vs. underfitting|Assume a single CV score tells you whether the model is well-fit|

---

### 17.10 Learning Curve Diagnostics

```python
from sklearn.model_selection import learning_curve

def plot_learning_curve(pipeline, X, y, groups=None, title='Learning Curve'):
    """
    Diagnoses underfitting (both curves low) vs.
    overfitting (large train-val gap).
    """
    if groups is not None:
        cv = LeaveOneGroupOut()
        cv_iter = list(cv.split(X, y, groups))
    else:
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_iter = cv

    train_sizes, train_scores, val_scores = learning_curve(
        pipeline, X, y,
        cv=cv_iter,
        train_sizes=np.linspace(0.1, 1.0, 10),
        scoring='balanced_accuracy',
        n_jobs=-1,
        shuffle=False
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.fill_between(train_sizes,
                     train_scores.mean(1) - train_scores.std(1),
                     train_scores.mean(1) + train_scores.std(1),
                     alpha=0.15, color='steelblue')
    ax.fill_between(train_sizes,
                     val_scores.mean(1) - val_scores.std(1),
                     val_scores.mean(1) + val_scores.std(1),
                     alpha=0.15, color='coral')
    ax.plot(train_sizes, train_scores.mean(1), 'o-', color='steelblue', label='Train')
    ax.plot(train_sizes, val_scores.mean(1),   'o-', color='coral',     label='Validation')
    ax.axhline(0.5, color='gray', linestyle='--', label='Chance (binary)')
    ax.set_xlabel('Training set size')
    ax.set_ylabel('Balanced Accuracy')
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()

    # Diagnose
    final_train = train_scores[-1].mean()
    final_val   = val_scores[-1].mean()
    gap = final_train - final_val
    print(f"\nDiagnosis:")
    print(f"  Train: {final_train:.3f}, Val: {final_val:.3f}, Gap: {gap:.3f}")
    if final_val < 0.6 and gap < 0.05:
        print("  → UNDERFITTING: both train and val low. Need richer features or more powerful model.")
    elif gap > 0.15:
        print("  → OVERFITTING: large train-val gap. Need regularization, fewer features, or more data.")
    else:
        print("  → REASONABLE FIT: consider collecting more data to push validation score higher.")
    return fig
```

---

_ClaudeEEG — Last updated April 2026. Grounded in MNE-Python docs, EEGLAB tutorials, peer-reviewed literature (2020–2025), braindecode documentation, NeuroPype documentation, and multimodal neuroscience data engineering practice._
