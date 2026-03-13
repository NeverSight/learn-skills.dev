---
name: revenuecat
description: Comprehensive assistance with RevenueCat in-app subscriptions and purchases
---

# RevenueCat Skill

Expert assistance for implementing in-app subscriptions and purchases using RevenueCat across iOS, Android, Flutter, React Native, and web platforms.

## When to Use This Skill

This skill should be triggered when:

- **SDK Setup**: Initializing RevenueCat SDK in iOS, Android, Flutter, or React Native apps
- **Subscription Implementation**: Adding subscription or in-app purchase functionality
- **Entitlement Checks**: Verifying user access to premium features or content
- **Purchase Flow**: Implementing buy buttons, handling transactions, or processing purchases
- **Restore Purchases**: Adding restore functionality for users switching devices
- **Offerings/Products**: Fetching and displaying subscription options or product catalogs
- **Paywall Design**: Building or configuring paywalls and purchase screens
- **Customer Info**: Retrieving subscription status or customer data
- **Debugging Purchases**: Troubleshooting subscription issues or transaction failures
- **REST API Integration**: Server-side subscription validation or webhook handling

## Quick Reference

### SDK Configuration

**Swift (iOS)**
```swift
import RevenueCat

Purchases.logLevel = .debug
Purchases.configure(withAPIKey: "your_public_api_key", appUserID: "user_123")
```

**Kotlin (Android)**
```kotlin
Purchases.logLevel = LogLevel.DEBUG
Purchases.configure(PurchasesConfiguration.Builder(this, "your_public_api_key").build())
```

**Flutter**
```dart
await Purchases.setLogLevel(LogLevel.debug);
PurchasesConfiguration configuration = PurchasesConfiguration("your_public_api_key");
await Purchases.configure(configuration);
```

**React Native**
```javascript
Purchases.setLogLevel(Purchases.LOG_LEVEL.DEBUG);
Purchases.configure({ apiKey: "your_public_api_key" });
```

### Checking Entitlements

**Swift**
```swift
let customerInfo = try await Purchases.shared.customerInfo()
if customerInfo.entitlements["pro"]?.isActive == true {
    // User has premium access
}
```

**Kotlin**
```kotlin
Purchases.sharedInstance.getCustomerInfoWith(
    onSuccess = { customerInfo ->
        if (customerInfo.entitlements["pro"]?.isActive == true) {
            // User has premium access
        }
    }
)
```

**React Native**
```javascript
const customerInfo = await Purchases.getCustomerInfo();
if (customerInfo.entitlements.active["pro"] !== undefined) {
    // User has premium access
}
```

### Fetching Offerings

**Swift**
```swift
Purchases.shared.getOfferings { (offerings, error) in
    if let packages = offerings?.current?.availablePackages {
        self.display(packages)
    }
}
```

**Kotlin**
```kotlin
Purchases.sharedInstance.getOfferingsWith({ error -> }) { offerings ->
    offerings.current?.availablePackages?.let { packages ->
        // Display packages
    }
}
```

### Making a Purchase

**Swift**
```swift
Purchases.shared.purchase(package: package) { (transaction, customerInfo, error, userCancelled) in
    if customerInfo.entitlements["pro"]?.isActive == true {
        // Unlock premium content
    }
}
```

**Kotlin**
```kotlin
Purchases.sharedInstance.purchase(
    packageToPurchase = aPackage,
    onError = { error, userCancelled -> },
    onSuccess = { storeTransaction, customerInfo ->
        if (customerInfo.entitlements["pro"]?.isActive == true) {
            // Unlock premium content
        }
    }
)
```

### Restoring Purchases

**Swift**
```swift
Purchases.shared.restorePurchases { customerInfo, error in
    // Check customerInfo to see if entitlement is now active
}
```

**Kotlin**
```kotlin
Purchases.sharedInstance.restorePurchases(
    onError = { error -> },
    onSuccess = { customerInfo ->
        // Check customerInfo to see if entitlement is now active
    }
)
```

### REST API - Get Customer Info

```bash
curl --request GET \
  --url https://api.revenuecat.com/v1/subscribers/app_user_id \
  --header 'Authorization: Bearer PUBLIC_API_KEY'
```

## Key Concepts

### Entitlements
A level of access, features, or content that a user is "entitled" to. Most apps use a single entitlement (e.g., "pro"). Created in the RevenueCat dashboard and linked to products. When a product is purchased, its associated entitlements become active.

### Offerings
The set of products available to a user. Configured remotely in the dashboard, allowing you to change available products without app updates. Access via `offerings.current` for the default offering.

### Packages
Containers for products within an offering. Include convenience accessors like `.monthly`, `.annual`, `.lifetime`. Each package contains a `storeProduct` with pricing details.

### CustomerInfo
The central object containing all subscription and purchase data for a user. Retrieved via `getCustomerInfo()` or returned after purchases. Contains the `entitlements` dictionary for access checks.

### App User ID
Unique identifier for each user. Can be provided during configuration or auto-generated as an anonymous ID. Used to sync purchases across devices.

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **other.md** - General RevenueCat documentation and overview

For detailed implementation patterns beyond the quick reference, consult the official documentation at https://www.revenuecat.com/docs/

## Working with This Skill

### For Beginners
1. Start by configuring the SDK in your app's initialization code
2. Create entitlements and offerings in the RevenueCat dashboard
3. Implement a simple entitlement check before showing premium content
4. Add a purchase button using `purchase(package:)`
5. Include a "Restore Purchases" button for App Store compliance

### For Intermediate Users
- Implement dynamic paywalls by fetching offerings and displaying packages
- Handle multiple entitlements for tiered access levels
- Set up customer info listeners for real-time subscription updates
- Use the REST API for server-side validation

### For Advanced Users
- Configure webhooks for server-side event handling
- Implement A/B testing with different offerings
- Set up integrations with analytics and attribution platforms
- Handle edge cases like grace periods and billing retry

## Common Patterns

### Paywall Display Logic
```swift
// Show paywall only if user doesn't have active subscription
if customerInfo.entitlements["pro"]?.isActive != true {
    showPaywall()
}
```

### Conditional Offerings
```swift
if user.isPaidDownload {
    packages = offerings?.offering(identifier: "paid_download_offer")?.availablePackages
} else {
    packages = offerings?.current?.availablePackages
}
```

## Important Notes

- Always initialize the SDK early in your app's lifecycle
- Use debug logging during development (`Purchases.logLevel = .debug`)
- The SDK automatically finishes/acknowledges transactions
- Only call `restorePurchases` from user interaction (like a button tap)
- Use public API keys from Project Settings; never expose secret keys
- Test Store allows development testing without real charges

## Resources

### Official Documentation
- Getting Started: https://www.revenuecat.com/docs/getting-started/quickstart
- SDK Reference: https://www.revenuecat.com/docs/
- REST API: https://docs.revenuecat.com/reference

### references/
Organized documentation extracted from official sources with detailed explanations and code examples.

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.
