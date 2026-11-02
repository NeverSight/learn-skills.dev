---
name: skin-matching
description: 皮肤双胞胎匹配算法，找到相似皮肤用户并推荐其有效产品。实现社区匹配功能时使用此技能。
---

# 皮肤匹配技能

## 概述
通过皮肤指纹向量匹配相似用户，推荐他们验证有效的产品。

## 皮肤指纹设计
```swift
struct SkinFingerprint: Codable {
    // 基础信息（用于匹配）
    let skinType: SkinType              // 肤质
    let ageRange: AgeRange              // 年龄段
    let gender: Gender?                 // 性别（可选）
    let region: String?                 // 地区/气候（可选）
    
    // 问题向量（0-1归一化）
    let issueVector: [Double]           // [spots, acne, pores, wrinkles, redness, evenness, texture]
    
    // 计算后的向量表示
    var vector: [Double] {
        var v: [Double] = []
        
        // One-hot编码肤质
        v.append(contentsOf: skinType.oneHot)
        
        // 年龄归一化
        v.append(ageRange.normalized)
        
        // 问题向量
        v.append(contentsOf: issueVector)
        
        return v
    }
}

enum SkinType: String, Codable, CaseIterable {
    case dry, oily, combination, sensitive
    
    var oneHot: [Double] {
        Self.allCases.map { $0 == self ? 1.0 : 0.0 }
    }
}

enum AgeRange: String, Codable {
    case under20, age20to25, age25to30, age30to35, age35to40, over40
    
    var normalized: Double {
        switch self {
        case .under20: return 0.1
        case .age20to25: return 0.25
        case .age25to30: return 0.4
        case .age30to35: return 0.55
        case .age35to40: return 0.7
        case .over40: return 0.85
        }
    }
}
```

## 相似度计算
```swift
class SkinMatcher {
    /// 计算余弦相似度
    func cosineSimilarity(_ a: [Double], _ b: [Double]) -> Double {
        guard a.count == b.count, !a.isEmpty else { return 0 }
        
        let dotProduct = zip(a, b).map(*).reduce(0, +)
        let magnitudeA = sqrt(a.map { $0 * $0 }.reduce(0, +))
        let magnitudeB = sqrt(b.map { $0 * $0 }.reduce(0, +))
        
        guard magnitudeA > 0, magnitudeB > 0 else { return 0 }
        return dotProduct / (magnitudeA * magnitudeB)
    }
    
    /// 加权相似度（肤质权重更高）
    func weightedSimilarity(user: SkinFingerprint, other: SkinFingerprint) -> Double {
        let basicSimilarity = cosineSimilarity(user.vector, other.vector)
        
        // 肤质必须相同才算高度相似
        let skinTypeBonus = user.skinType == other.skinType ? 0.2 : -0.3
        
        // 年龄接近加分
        let ageDiff = abs(user.ageRange.normalized - other.ageRange.normalized)
        let ageBonus = ageDiff < 0.2 ? 0.1 : 0
        
        return min(1.0, max(0, basicSimilarity + skinTypeBonus + ageBonus))
    }
    
    /// 查找皮肤双胞胎
    func findSkinTwins(
        for user: SkinFingerprint,
        from pool: [UserProfile],
        limit: Int = 10
    ) -> [SkinTwin] {
        pool
            .map { profile -> SkinTwin in
                let similarity = weightedSimilarity(user: user, other: profile.fingerprint)
                return SkinTwin(
                    userId: profile.id,
                    similarity: similarity,
                    skinProfile: profile.anonymized,
                    effectiveProducts: profile.effectiveProducts
                )
            }
            .filter { $0.similarity >= 0.6 }  // 最低相似度阈值
            .sorted { $0.similarity > $1.similarity }
            .prefix(limit)
            .map { $0 }
    }
}
```

## 匹配结果模型
```swift
struct SkinTwin: Identifiable {
    let id = UUID()
    let userId: String
    let similarity: Double              // 0-1
    let skinProfile: AnonymousProfile
    let effectiveProducts: [EffectiveProduct]
    
    var matchLevel: MatchLevel {
        switch similarity {
        case 0.9...: return .twin        // 皮肤双胞胎
        case 0.8..<0.9: return .verySimilar
        case 0.7..<0.8: return .similar
        default: return .somewhatSimilar
        }
    }
}

enum MatchLevel: String {
    case twin = "皮肤双胞胎 👯"
    case verySimilar = "非常相似"
    case similar = "相似"
    case somewhatSimilar = "有点相似"
}

struct AnonymousProfile: Codable {
    let skinType: SkinType
    let ageRange: String                // "25-30岁"
    let mainConcerns: [SkinConcern]
    let region: String?
    // 不包含任何可识别个人信息
}

struct EffectiveProduct: Identifiable {
    let id: String
    let product: Product
    let usageDuration: Int              // 使用天数
    let improvementPercent: Double      // 改善百分比
    let verifiedAt: Date
}
```

## 推荐分数计算
```swift
struct ProductRecommendationScore {
    let product: Product
    let score: Double
    let reasons: [String]
    
    static func calculate(
        product: Product,
        userFingerprint: SkinFingerprint,
        skinTwins: [SkinTwin]
    ) -> ProductRecommendationScore {
        var score: Double = 0
        var reasons: [String] = []
        
        // 1. 相似用户有效率 (权重40%)
        let relevantTwins = skinTwins.filter { twin in
            twin.effectiveProducts.contains { $0.product.id == product.id }
        }
        if !relevantTwins.isEmpty {
            let weightedEffectiveness = relevantTwins.reduce(0.0) { sum, twin in
                let effectiveness = twin.effectiveProducts
                    .first { $0.product.id == product.id }?
                    .improvementPercent ?? 0
                return sum + twin.similarity * effectiveness
            } / relevantTwins.reduce(0.0) { $0 + $1.similarity }
            
            score += weightedEffectiveness * 0.4
            reasons.append("\(relevantTwins.count)位相似用户验证有效")
        }
        
        // 2. 成分适配度 (权重30%)
        let ingredientMatch = calculateIngredientMatch(product, userFingerprint)
        score += ingredientMatch * 0.3
        if ingredientMatch > 0.7 {
            reasons.append("成分适合你的肤质")
        }
        
        // 3. 问题匹配度 (权重20%)
        let concernMatch = calculateConcernMatch(product, userFingerprint)
        score += concernMatch * 0.2
        if concernMatch > 0.7 {
            reasons.append("针对你的皮肤问题")
        }
        
        // 4. 刺激风险扣分 (权重10%)
        let riskPenalty = calculateRiskPenalty(product, userFingerprint)
        score -= riskPenalty * 0.1
        if riskPenalty > 0.3 {
            reasons.append("⚠️ 部分成分可能刺激")
        }
        
        return ProductRecommendationScore(
            product: product,
            score: min(1.0, max(0, score)),
            reasons: reasons
        )
    }
}
```

## 数据贡献机制
```swift
struct DataContribution {
    /// 用户贡献追踪数据时调用
    func contribute(
        session: TrackingSession,
        report: TrackingReport,
        consentLevel: ConsentLevel
    ) {
        switch consentLevel {
        case .anonymous:
            // 只贡献统计数据，不关联用户
            uploadAnonymousStats(report)
        case .pseudonymous:
            // 贡献数据并参与匹配，但不显示可识别信息
            uploadForMatching(session, report)
        case .public:
            // 公开分享，可被其他用户看到
            uploadPublic(session, report)
        case .none:
            // 不贡献数据
            break
        }
    }
    
    enum ConsentLevel {
        case anonymous      // 匿名统计
        case pseudonymous   // 参与匹配但不公开
        case `public`       // 公开分享
        case none           // 完全私密
    }
}
```

## 验证
- [ ] 相似度计算准确
- [ ] 匹配结果排序正确
- [ ] 推荐分数合理
- [ ] 隐私保护到位
- [ ] 冷启动时有合理降级
