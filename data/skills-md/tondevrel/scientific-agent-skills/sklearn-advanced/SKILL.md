---
name: sklearn-advanced
description: Professional sub-skill for scikit-learn focused on robust pipeline architecture, custom estimator development, advanced feature engineering, and rigorous model validation. Covers Target Encoding, Nested Cross-Validation, and Production Deployment.
version: 1.4
license: BSD-3-Clause
---

# scikit-learn - Advanced Architecture

To move beyond simple scripts, you must master the Pipeline API. This allows you to treat your entire preprocessing and modeling sequence as a single object, ensuring that your training logic is identical to your production inference logic.

## When to Use

- Building complex feature engineering flows for heterogeneous data.
- Creating reusable, custom preprocessing steps (e.g., domain-specific cleaning).
- Performing rigorous hyperparameter tuning without data leakage.
- Implementing ensemble methods beyond standard Random Forest.
- Monitoring and interpreting model decisions (Partial Dependence, Permutation Importance).
- Exporting models for high-performance production environments.

## Reference Documentation

- **Pipeline Guide**: https://scikit-learn.org/stable/modules/compose.html
- **Custom Estimators**: https://scikit-learn.org/stable/developers/develop.html
- **Model Evaluation**: https://scikit-learn.org/stable/modules/model_evaluation.html
- **Search patterns**: `sklearn.base.BaseEstimator`, `sklearn.compose.make_column_selector`, `sklearn.model_selection.GridSearchCV`

## Core Principles

### Everything is an Object

Every step in your workflow should be an estimator. If you find yourself doing manual pandas operations between training and testing, you are risking Data Leakage.

### The Pipeline Contract

A Pipeline ensures that `.fit()` is only called on training data and `.transform()` is applied consistently to both train and test sets.

### Heterogeneous Data handling

Use `ColumnTransformer` to apply different logic to numerical, categorical, and text data in parallel, then merge the results automatically.

## Quick Reference

### Standard Imports

```python
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import FunctionTransformer, StandardScaler, OneHotEncoder
from sklearn.model_selection import cross_validate, StratifiedKFold
```

### Basic Pattern - Professional Pipeline

```python
# 1. Define Preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), make_column_selector(dtype_include=np.number)),
        ('cat', OneHotEncoder(handle_unknown='ignore'), make_column_selector(dtype_include=object))
    ])

# 2. Create the Full Pipeline
clf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])

# 3. Fit and Tune (The entire pipeline is tuned together)
# Use 'classifier__' prefix to access parameters inside the pipeline
param_grid = {'classifier__n_estimators': [100, 200]}
grid = GridSearchCV(clf, param_grid, cv=5).fit(X_train, y_train)
```

## Critical Rules

### ✅ DO

- **Inherit from BaseEstimator and TransformerMixin** - This gives you `.fit_transform()` and `.get_params()` for free.
- **Use check_is_fitted** - In custom transformers, always verify the model is trained before allowing `.transform()`.
- **Set handle_unknown='ignore'** - In OneHotEncoder, this prevents crashes if a new category appears in production.
- **Use TransformedTargetRegressor** - If you need to log-transform the target variable (Y), use this to automate the inverse transformation for predictions.
- **Prefer cross_validate over cross_val_score** - It allows multiple metrics and returns training scores to detect overfitting.
- **Set n_jobs=-1** - Maximize CPU usage during GridSearch and Cross-validation.

### ❌ DON'T

- **Don't use fit_transform on Test Data** - This is the #1 cause of over-optimistic results.
- **Don't implement fit if it's not needed** - For stateless transformations (like log-transform), use `FunctionTransformer`.
- **Don't hardcode Column Names** - Use `make_column_selector` to make your pipelines resilient to new columns.
- **Don't ignore the Pipeline index** - If a pipeline fails, use `pipe.named_steps['step_name']` to inspect internal state.

## Custom Estimator Development

### Creating a Custom Feature Selector

```python
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted

class VarianceSelector(BaseEstimator, TransformerMixin):
    def __init__(self, threshold=0.01):
        self.threshold = threshold

    def fit(self, X, y=None):
        X = pd.DataFrame(X)
        self.variances_ = X.var()
        self.columns_to_keep_ = self.variances_[self.variances_ > self.threshold].index
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        check_is_fitted(self)
        X = pd.DataFrame(X)
        return X[self.columns_to_keep_]
```

## Advanced Preprocessing

### Target Encoding (Handling high-cardinality categories)

```python
from sklearn.preprocessing import TargetEncoder

# Efficiently encodes categories like 'City' or 'ZipCode' 
# based on the average target value, with internal cross-validation
encoder = TargetEncoder(smooth="auto")
X_encoded = encoder.fit_transform(X_cat, y)
```

### Stacking and Voting Ensembles

```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

estimators = [
    ('rf', RandomForestClassifier()),
    ('svc', Pipeline([('scaler', StandardScaler()), ('svr', SVC())]))
]

# Use a meta-learner (LogisticRegression) to combine base model predictions
stack_clf = StackingClassifier(
    estimators=estimators, final_estimator=LogisticRegression()
)
```

## Model Evaluation & Diagnostics

### Rigorous Cross-Validation

```python
from sklearn.model_selection import cross_validate

scoring = ['accuracy', 'precision_macro', 'recall_macro', 'f1_macro']
results = cross_validate(clf, X, y, cv=5, scoring=scoring, return_train_score=True)

print(f"Test F1: {results['test_f1_macro'].mean():.4f}")
print(f"Train F1: {results['train_f1_macro'].mean():.4f}") # Check for gap (overfitting)
```

### Calibration Curves (Ensuring probabilities are real)

```python
from sklearn.calibration import CalibrationDisplay

# A well-calibrated model's predicted probability matches the actual frequency
CalibrationDisplay.from_estimator(clf, X_test, y_test, n_bins=10)
```

## Production & Persistence

### Using Joblib for large models

```python
import joblib

# Save model
joblib.dump(clf, 'final_model.joblib', compress=3)

# Load model
loaded_model = joblib.load('final_model.joblib')
```

### Exporting to ONNX (High-speed inference)

```python
# requires skl2onnx
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

initial_type = [('float_input', FloatTensorType([None, X.shape[1]]))]
onx = convert_sklearn(clf, initial_types=initial_type)
with open("model.onnx", "wb") as f:
    f.write(onx.SerializeToString())
```

## Practical Workflows

### 1. Handling Missing Data and Outliers automatically

```python
from sklearn.impute import KNNImputer
from sklearn.ensemble import IsolationForest

def build_robust_pipe():
    return Pipeline([
        ('imputer', KNNImputer(n_neighbors=5)),
        # FunctionTransformer for outlier removal is tricky because 
        # it changes row count. IsolationForest is better used for filtering.
        ('scaler', StandardScaler()),
        ('model', GradientBoostingClassifier())
    ])
```

### 2. Time-Series Split (Avoid future leakage)

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
# Use this cv object in GridSearchCV
grid = GridSearchCV(model, params, cv=tscv)
```

### 3. Feature Union (Parallel Feature Extraction)

```python
from sklearn.pipeline import FeatureUnion
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest

# Extract PCA features AND SelectKBest features in parallel
combined_features = FeatureUnion([
    ("pca", PCA(n_components=2)),
    ("univ_select", SelectKBest(k=5))
])

pipe = Pipeline([
    ("features", combined_features),
    ("clf", RandomForestClassifier())
])
```

## Performance Optimization

### Cache Pipeline Results

If your preprocessing (like KNNImputer) is slow and you are doing GridSearch, use memory to cache the transformer output.

```python
from tempfile import mkdtemp
from shutil import rmtree

cachedir = mkdtemp()
pipe = Pipeline(steps=[...], memory=cachedir)
# Clean up after
# rmtree(cachedir)
```

## Common Pitfalls and Solutions

### The "LabelEncoder for X" Error

LabelEncoder is only for labels (y). For features (X), always use OrdinalEncoder or OneHotEncoder.

### Column Mismatch in Production

The Pipeline stores the training column order. If you pass a DataFrame with different column order in production, it might fail or give wrong results.

```python
# ✅ Solution: Ensure your pipeline is the first point of entry 
# for raw data, or use a custom transformer that sorts columns.
```

### Leakage during Hyperparameter Tuning

Standard Cross-validation inside a Pipeline is safe. But if you perform feature selection (like SelectKBest) before the Pipeline, you have leaked information from the whole dataset into your model.

```python
# ✅ Solution: Always include feature selection AS A STEP in the Pipeline.
```

Advanced scikit-learn is about discipline. By forcing all data transformations into the Pipeline/Transformer architecture, you create models that are not only accurate but also robust, maintainable, and ready for real-world deployment.
