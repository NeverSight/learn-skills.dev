---
name: ingredient-scanner
description: 扫描护肤品成分表，OCR识别并AI解读成分功效与风险。实现成分扫描功能时使用此技能。
---

# 成分扫描技能

## 概述
拍摄护肤品成分表，通过OCR识别成分，并使用AI解读功效与风险。

## 处理流程
```
拍照 → OCR识别 → 成分标准化 → 本地匹配 → AI解读 → 结果展示
```

## 1. OCR识别模块
```swift
import Vision

class IngredientOCR {
    func recognizeText(from image: UIImage) async throws -> [String] {
        guard let cgImage = image.cgImage else {
            throw OCRError.invalidImage
        }
        
        let request = VNRecognizeTextRequest()
        request.recognitionLevel = .accurate
        request.recognitionLanguages = ["en-US", "zh-Hans", "zh-Hant"]
        request.usesLanguageCorrection = true
        
        let handler = VNImageRequestHandler(cgImage: cgImage)
        try handler.perform([request])
        
        let text = request.results?
            .compactMap { $0.topCandidates(1).first?.string }
            .joined(separator: " ") ?? ""
        
        return parseIngredients(from: text)
    }
    
    private func parseIngredients(from text: String) -> [String] {
        // 成分表通常用逗号分隔
        let separators = CharacterSet(charactersIn: ",，、;；")
        return text
            .components(separatedBy: separators)
            .map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }
            .filter { !$0.isEmpty }
    }
}
```

## 2. 成分标准化
```swift
class IngredientNormalizer {
    // 成分别名映射
    private let aliasMap: [String: String] = [
        "水": "Water",
        "纯净水": "Water",
        "去离子水": "Water",
        "烟酰胺": "Niacinamide",
        "维生素B3": "Niacinamide",
        "视黄醇": "Retinol",
        "维A醇": "Retinol",
        "透明质酸": "Hyaluronic Acid",
        "玻尿酸": "Hyaluronic Acid",
        "水杨酸": "Salicylic Acid",
        "抗坏血酸": "Ascorbic Acid",
        "维生素C": "Ascorbic Acid",
        // ... 更多映射
    ]
    
    func normalize(_ ingredient: String) -> String {
        let trimmed = ingredient.trimmingCharacters(in: .whitespacesAndNewlines)
        return aliasMap[trimmed] ?? trimmed
    }
}
```

## 3. 本地成分库匹配
```swift
struct IngredientInfo: Codable {
    let name: String
    let function: IngredientFunction
    let safetyRating: Int           // 1-10
    let irritationRisk: IrritationLevel
    let benefits: [String]
    let warnings: [String]?
    let concentration: String?       // 有效浓度范围
}

class IngredientDatabase {
    private var ingredients: [String: IngredientInfo] = [:]
    
    func lookup(_ name: String) -> IngredientInfo? {
        let normalized = name.lowercased()
        return ingredients[normalized]
    }
    
    func loadLocalDatabase() {
        // 从本地JSON加载常见成分信息
        guard let url = Bundle.main.url(forResource: "ingredients", withExtension: "json"),
              let data = try? Data(contentsOf: url),
              let decoded = try? JSONDecoder().decode([String: IngredientInfo].self, from: data) else {
            return
        }
        ingredients = decoded
    }
}
```

## 4. AI解读
```swift
func analyzeIngredients(
    ingredients: [String],
    userProfile: UserProfile?
) async throws -> IngredientAnalysis {
    let prompt = """
    作为护肤品成分分析专家，请分析以下成分表：
    
    成分：\(ingredients.joined(separator: ", "))
    
    用户信息：
    - 肤质：\(userProfile?.skinType.rawValue ?? "未知")
    - 主要问题：\(userProfile?.concerns.map(\.rawValue).joined(separator: ", ") ?? "未知")
    - 已知过敏：\(userProfile?.allergies.joined(separator: ", ") ?? "无")
    
    请以JSON格式返回分析结果：
    {
      "overallRating": 0-10,
      "suitability": "suitable/caution/unsuitable",
      "highlights": ["亮点成分1", "亮点成分2"],
      "warnings": ["风险提示1"],
      "conflicts": ["冲突提示（如与用户已用产品冲突）"],
      "summary": "一句话总结"
    }
    """
    
    return try await geminiService.analyze(prompt: prompt)
}
```

## 5. 结果模型
```swift
struct IngredientAnalysis: Codable {
    let ingredients: [ParsedIngredient]
    let overallRating: Double
    let suitability: Suitability
    let highlights: [String]
    let warnings: [String]
    let conflicts: [String]?
    let summary: String
}

struct ParsedIngredient: Codable {
    let name: String
    let normalizedName: String
    let function: IngredientFunction?
    let safetyRating: Int?
    let isHighlight: Bool
    let isWarning: Bool
}

enum Suitability: String, Codable {
    case suitable    // 适合
    case caution     // 谨慎使用
    case unsuitable  // 不适合
}
```

## 6. 冲突检测规则
```swift
struct ConflictRule {
    let ingredient1: String
    let ingredient2: String
    let severity: ConflictSeverity
    let description: String
}

enum ConflictSeverity {
    case warning    // 建议分开使用
    case danger     // 不建议同时使用
}

let conflictRules: [ConflictRule] = [
    ConflictRule(
        ingredient1: "Retinol",
        ingredient2: "AHA",
        severity: .warning,
        description: "A醇和果酸同时使用可能导致刺激，建议早晚分开使用"
    ),
    ConflictRule(
        ingredient1: "Retinol",
        ingredient2: "BHA",
        severity: .warning,
        description: "A醇和水杨酸同时使用可能导致刺激"
    ),
    ConflictRule(
        ingredient1: "Retinol",
        ingredient2: "Benzoyl Peroxide",
        severity: .danger,
        description: "A醇和过氧化苯甲酰会相互抵消效果"
    ),
    ConflictRule(
        ingredient1: "Vitamin C",
        ingredient2: "Niacinamide",
        severity: .warning,
        description: "高浓度时可能互相影响效果，建议间隔15分钟使用"
    )
]
```

## 验证
- [ ] OCR识别准确率 > 90%
- [ ] 成分标准化覆盖常见别名
- [ ] 本地成分库包含200+常见成分
- [ ] 冲突检测规则完整
- [ ] AI解读结果结构正确
