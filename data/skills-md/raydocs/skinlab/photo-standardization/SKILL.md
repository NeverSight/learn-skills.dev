---
name: photo-standardization
description: 标准化拍照流程，确保光线、角度、距离一致，用于效果追踪对比。实现拍照引导功能时使用此技能。
---

# 标准化拍照技能

## 概述
确保每次拍照条件一致，使前后对比有效可信。

## 检测模块

### 1. 光线检测
```swift
class LightingDetector {
    func detectLighting(from sampleBuffer: CMSampleBuffer) -> LightingCondition {
        // 使用AVCaptureDevice获取曝光信息
        let exposureValue = calculateEV(from: sampleBuffer)
        
        switch exposureValue {
        case ..<6:
            return .tooDark(suggestion: "请移到光线更充足的地方")
        case 6..<8:
            return .slightlyDark(suggestion: "光线略暗，建议开灯或靠近窗户")
        case 8..<12:
            return .optimal
        case 12..<14:
            return .slightlyBright(suggestion: "光线略强，避免直射光")
        default:
            return .tooBright(suggestion: "光线过强，请避开强光源")
        }
    }
}

enum LightingCondition {
    case tooDark(suggestion: String)
    case slightlyDark(suggestion: String)
    case optimal
    case slightlyBright(suggestion: String)
    case tooBright(suggestion: String)
    
    var isAcceptable: Bool {
        switch self {
        case .optimal, .slightlyDark, .slightlyBright:
            return true
        default:
            return false
        }
    }
}
```

### 2. 角度检测
```swift
import Vision

class FaceAngleDetector {
    func detectFaceAngle(in image: CGImage) async throws -> FaceAngle {
        let request = VNDetectFaceRectanglesRequest()
        request.revision = VNDetectFaceRectanglesRequestRevision3
        
        let handler = VNImageRequestHandler(cgImage: image)
        try handler.perform([request])
        
        guard let face = request.results?.first else {
            throw DetectionError.noFaceDetected
        }
        
        return FaceAngle(
            yaw: face.yaw?.doubleValue ?? 0,    // 左右转头
            pitch: face.pitch?.doubleValue ?? 0, // 上下点头
            roll: face.roll?.doubleValue ?? 0    // 歪头
        )
    }
}

struct FaceAngle {
    let yaw: Double
    let pitch: Double
    let roll: Double
    
    var isOptimal: Bool {
        abs(yaw) < 10 && abs(pitch) < 10 && abs(roll) < 5
    }
    
    var suggestion: String? {
        if abs(yaw) >= 10 {
            return yaw > 0 ? "请稍微向左转" : "请稍微向右转"
        }
        if abs(pitch) >= 10 {
            return pitch > 0 ? "请稍微低头" : "请稍微抬头"
        }
        if abs(roll) >= 5 {
            return "请保持头部端正"
        }
        return nil
    }
}
```

### 3. 距离检测
```swift
class FaceDistanceDetector {
    func detectDistance(faceRect: CGRect, imageSize: CGSize) -> DistanceCondition {
        let faceRatio = (faceRect.width * faceRect.height) / (imageSize.width * imageSize.height)
        
        switch faceRatio {
        case ..<0.15:
            return .tooFar(suggestion: "请靠近一些")
        case 0.15..<0.25:
            return .slightlyFar(suggestion: "可以再靠近一点")
        case 0.25..<0.45:
            return .optimal
        case 0.45..<0.55:
            return .slightlyClose(suggestion: "可以稍微远一点")
        default:
            return .tooClose(suggestion: "请稍微远离镜头")
        }
    }
}

enum DistanceCondition {
    case tooFar(suggestion: String)
    case slightlyFar(suggestion: String)
    case optimal
    case slightlyClose(suggestion: String)
    case tooClose(suggestion: String)
    
    var isAcceptable: Bool {
        switch self {
        case .optimal, .slightlyFar, .slightlyClose:
            return true
        default:
            return false
        }
    }
}
```

### 4. 综合检测状态
```swift
struct PhotoCondition {
    let lighting: LightingCondition
    let angle: FaceAngle
    let distance: DistanceCondition
    let timestamp: Date
    
    var isReady: Bool {
        lighting.isAcceptable && angle.isOptimal && distance.isAcceptable
    }
    
    var suggestions: [String] {
        var result: [String] = []
        if case .tooDark(let s) = lighting { result.append(s) }
        if case .tooBright(let s) = lighting { result.append(s) }
        if let s = angle.suggestion { result.append(s) }
        if case .tooFar(let s) = distance { result.append(s) }
        if case .tooClose(let s) = distance { result.append(s) }
        return result
    }
}
```

## UI引导组件
```swift
struct PhotoGuideOverlay: View {
    let condition: PhotoCondition
    
    var body: some View {
        ZStack {
            // 面部对齐框
            FaceAlignmentGuide(isAligned: condition.angle.isOptimal)
            
            // 状态指示器
            VStack {
                Spacer()
                ConditionIndicators(condition: condition)
                    .padding(.bottom, 100)
            }
            
            // 提示文字
            if !condition.isReady {
                SuggestionBanner(suggestions: condition.suggestions)
            }
        }
    }
}

struct FaceAlignmentGuide: View {
    let isAligned: Bool
    
    var body: some View {
        RoundedRectangle(cornerRadius: 120)
            .stroke(isAligned ? Color.green : Color.orange, lineWidth: 3)
            .frame(width: 240, height: 320)
    }
}
```

## 输出
```swift
struct StandardizedPhoto {
    let image: UIImage
    let metadata: PhotoMetadata
}

struct PhotoMetadata: Codable {
    let captureDate: Date
    let exposureValue: Double
    let faceAngle: FaceAngle
    let faceRatio: Double
    let deviceModel: String
}
```

## 验证
- [ ] 光线检测准确
- [ ] 角度检测灵敏度合适
- [ ] 自动拍摄触发正确
- [ ] UI引导清晰易懂
- [ ] 支持无障碍（VoiceOver提示）
