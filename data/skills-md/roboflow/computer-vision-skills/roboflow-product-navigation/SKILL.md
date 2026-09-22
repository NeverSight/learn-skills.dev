---
name: roboflow-product-navigation
description: Use when explaining where Roboflow features live in the app.roboflow.com web app, mapping intents like upload, annotate, train, deploy to specific page URLs.
---

> **For agents — source-of-truth:** This skill is authored in [`roboflow/computer-vision-skills`](https://github.com/roboflow/computer-vision-skills) and shipped with the Roboflow plugin. If your client has loaded the plugin (you'll see `roboflow:<name>` skills in your available skills list), use those local skills — they're read fresh from disk every session. The same content served as MCP resources at `roboflow://skills/<name>/...` is a fallback for clients without the plugin and may lag this repo. **Don't call `ReadMcpResourceTool` for `roboflow://skills/...` URIs when a local `roboflow:<name>` skill is available.**

# Roboflow Web App Navigation

Base URL: `https://app.roboflow.com`

## URL Hierarchy

```
Workspace -> Project -> Version -> Model
/{workspace} -> /{workspace}/{project} -> /{workspace}/{project}/{version} -> trained model
```

## Page Reference

### Workspace Level

| Page | URL Pattern | What's There |
|------|-------------|--------------|
| Workspace projects | `/{workspace}` | Project list, asset library tab, create new project |
| Home | `/{workspace}/home` | Dashboard, recent activity, quick actions |
| Asset Library | `/{workspace}?tab=asset-library` | Cross-project image library (tab on projects page) |
| Browse images | `/{workspace}/browse` | Browse all workspace images |
| Models | `/{workspace}/models` | All models in workspace |
| Workflows list | `/{workspace}/workflows` | All workflows in workspace, create/manage |
| Vision Events | `/{workspace}/vision-events` | Inference volume, class distribution, monitoring |
| Deployments | `/{workspace}/deployments` | Dedicated deployments, batch processing, edge devices (tabs) |
| Edge Devices | `/{workspace}/deployment-manager/devices` | Edge device management |

#### Workspace Settings (`/{workspace}/settings/...`)

| Page | URL Pattern | What's There |
|------|-------------|--------------|
| Plan & Billing | `/{workspace}/settings/plan` | Plan, credit usage, invoices, payment method |
| Usage | `/{workspace}/settings/usage` | API call history, credit consumption |
| Team members | `/{workspace}/settings/members` | Invite, remove, change roles (RBAC) |
| API keys | `/{workspace}/settings/api` | Workspace API keys |
| Annotation insights | `/{workspace}/settings/insights` | Annotator productivity, agreement metrics |
| Workflow blocks | `/{workspace}/settings/workflow-blocks` | Custom workflow block management |
| Project settings | `/{workspace}/settings/project-settings` | Workspace-wide project settings |
| Third-party keys | `/{workspace}/settings/thirdpartykeys` | External service API keys |
| Data sources | `/{workspace}/settings/datasources` | Bucket mirror / cloud import config |
| Audit logs | `/{workspace}/settings/audit-logs` | Workspace activity audit trail (Enterprise) |

### Project Level

| Page | URL Pattern | What's There |
|------|-------------|--------------|
| Project (auto-redirect) | `/{workspace}/{project}` | Redirects to most relevant sub-page based on state |
| Upload | `/{workspace}/{project}/upload` | Drag-and-drop images/videos, import from cloud (S3/GCS/Azure) |
| Annotate | `/{workspace}/{project}/annotate` | Annotation tool: bbox, polygon, mask, keypoints, AI labeling |
| Annotate batch | `/{workspace}/{project}/annotate/batch/{batchId}` | Annotate specific batch, create jobs, auto-label |
| Annotate job | `/{workspace}/{project}/annotate/job/{jobId}` | Work on specific annotation job |
| Images | `/{workspace}/{project}/images` | Grid view of all images, search, filter by tag/class/split |
| Browse | `/{workspace}/{project}/browse` | Dataset image browser |
| Explore | `/{workspace}/{project}/explore` | Visual dataset exploration |
| Dataset health | `/{workspace}/{project}/health` | Class balance, image sizes, annotation stats |
| Settings / Classes | `/{workspace}/{project}/settings` | Manage classes, project settings |
| Videos | `/{workspace}/{project}/videos` | Video management |
| Active Learning | `/{workspace}/{project}/active-learning` | Active learning configuration |
| Train | `/{workspace}/{project}/train` | Start training, model architecture selection |
| Deploy | `/{workspace}/{project}/deploy` | API snippet, SDK code, deployment options |
| Overview | `/{workspace}/{project}/overview` | Project overview (public projects) |

### Version Level

| Page | URL Pattern | What's There |
|------|-------------|--------------|
| Generate version | `/{workspace}/{project}/generate` | Train/test split, preprocessing, augmentation config |
| Version list / detail | `/{workspace}/{project}/versions` | All versions, version summary |
| Version detail | `/{workspace}/{project}/{version}` | Version summary, image counts per split |
| Training | `/{workspace}/{project}/{version}/train` | Start training on this version |
| Training results | `/{workspace}/{project}/{version}/train/results` | mAP, precision, recall, confusion matrix |
| Export | `/{workspace}/{project}/{version}/export` | Download in various formats (COCO, YOLO, VOC, etc.) |
| Version images | `/{workspace}/{project}/{version}/images` | Browse images in this version |

### Workflows

| Page | URL Pattern | What's There |
|------|-------------|--------------|
| Workflows list | `/{workspace}/workflows` | All workflows, create new |
| Workflow editor | `/{workspace}/workflows/{workflow-id}` | Visual block editor, JSON editor, preview, test |

### Universe (separate domain)

| Page | URL Pattern | What's There |
|------|-------------|--------------|
| Universe home | `universe.roboflow.com` | Search datasets/models, trending projects |
| Dataset page | `universe.roboflow.com/{user}/{project}` | Overview, images, classes, download, fork |
| Model page | `universe.roboflow.com/{user}/{project}/model` | Try model, API snippet, deploy |
| Dataset browse | `universe.roboflow.com/{user}/{project}/browse` | Explore images with annotations |

### Other Pages

| Page | URL Pattern | What's There |
|------|-------------|--------------|
| Account settings | `/settings/account` | Profile, email, password, API keys |
| Roboflow Rapid | `/{workspace}/rapid/{rapidDataId}` | Guided flow: upload, auto-label, train, deploy |

## API Keys

- Workspace API key: `/{workspace}/settings/api`
- Personal API key: `/settings/account` -> API Keys tab
- Both are needed for different SDK/API operations

## Project Types

When creating a project, choose one (cannot be changed later):

| Type | Use Case |
|------|----------|
| Object Detection | Locate objects with bounding boxes |
| Instance Segmentation | Pixel-level object boundaries |
| Semantic Segmentation | Pixel-level class regions |
| Keypoint Detection | Object pose/skeleton |
| Single-Label Classification | One label per image |
| Multi-Label Classification | Multiple labels per image |

## Related Pages

- `roboflow://skills/roboflow-product-navigation/features-by-page` — intent-to-URL lookup table ("I want to do X → go here")
