---
name: iOS Accessibility Skill
description: Best practices for implementing accessibility features in iOS apps, including VoiceOver support, Dynamic Type, and Human Interface Guidelines compliance.
version: 1.0
activation: Activate for queries on iOS accessibility, VoiceOver implementation, Dynamic Type, or making apps accessible to users with disabilities.
---

# iOS Accessibility Skill

This skill focuses on making iOS applications accessible to all users, including those with visual, motor, or cognitive impairments. It covers VoiceOver, Dynamic Type, and adherence to Apple's Human Interface Guidelines (HIG) for accessibility.

## Best Practices

1. **VoiceOver Support**: Ensure all UI elements are properly labeled and navigable with VoiceOver.

2. **Dynamic Type**: Support text scaling for users with visual impairments.

3. **Color and Contrast**: Use sufficient color contrast and don't rely solely on color to convey information.

4. **Touch Targets**: Make interactive elements large enough (44x44 points minimum).

5. **HIG Compliance**: Follow Apple's accessibility guidelines throughout the design and development process.

6. **Testing**: Regularly test with accessibility features enabled.

## Accessibility Guidelines

- Use semantic UI elements that come with built-in accessibility support.
- Provide meaningful labels and hints for custom controls.
- Group related elements and provide headers for complex layouts.
- Support assistive technologies like VoiceOver, Zoom, and Switch Control.
- Consider motor impairments when designing interactions.
- Test with real users when possible.

## Examples

### Example 1: VoiceOver Labels in SwiftUI

**User Prompt:** "How do I add VoiceOver labels to SwiftUI buttons?"

**Expected Output:**
```swift
import SwiftUI

struct AccessibleButtonView: View {
    var body: some View {
        VStack {
            Button(action: {
                // Action
            }) {
                Image(systemName: "star.fill")
                    .font(.largeTitle)
            }
            .accessibilityLabel("Favorite this item")
            .accessibilityHint("Double tap to add to favorites")
            
            Button("Submit", action: {
                // Submit action
            })
            .accessibilityHint("This will send your information")
        }
    }
}
```

### Example 2: Dynamic Type Support

**User Prompt:** "Implement Dynamic Type in a SwiftUI text view."

**Expected Output:**
```swift
import SwiftUI

struct DynamicTextView: View {
    var body: some View {
        VStack {
            Text("This text scales with Dynamic Type")
                .font(.body)
            
            Text("Headline that adapts")
                .font(.headline)
            
            Text("Custom font that scales")
                .font(.system(size: 17, weight: .regular, design: .default))
                .minimumScaleFactor(0.8)
                .lineLimit(1)
        }
        .padding()
    }
}
```

### Example 3: Accessible Form in UIKit

**User Prompt:** "Create an accessible login form in UIKit with VoiceOver support."

**Expected Output:**
```swift
import UIKit

class LoginViewController: UIViewController {
    let emailTextField = UITextField()
    let passwordTextField = UITextField()
    let loginButton = UIButton(type: .system)
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Email field
        emailTextField.placeholder = "Email"
        emailTextField.keyboardType = .emailAddress
        emailTextField.accessibilityLabel = "Email address"
        emailTextField.accessibilityHint = "Enter your email address"
        
        // Password field
        passwordTextField.placeholder = "Password"
        passwordTextField.isSecureTextEntry = true
        passwordTextField.accessibilityLabel = "Password"
        passwordTextField.accessibilityHint = "Enter your password"
        
        // Login button
        loginButton.setTitle("Log In", for: .normal)
        loginButton.accessibilityHint = "Tap to log in to your account"
        
        // Layout code here...
    }
}
```

### Example 4: Grouping Elements

**User Prompt:** "How to group related accessibility elements in SwiftUI?"

**Expected Output:**
```swift
import SwiftUI

struct GroupedElementsView: View {
    var body: some View {
        VStack {
            VStack {
                Text("Contact Information")
                    .font(.headline)
                TextField("Name", text: .constant(""))
                TextField("Phone", text: .constant(""))
            }
            .accessibilityElement(children: .combine)
            .accessibilityLabel("Contact information form")
            
            Button("Save Contact") {
                // Save action
            }
            .accessibilityHint("Saves the contact information")
        }
        .padding()
    }
}
```

### Example 5: Color Contrast and Alternative Text

**User Prompt:** "Ensure good color contrast and provide alternatives for color-dependent information."

**Expected Output:**
```swift
import SwiftUI

struct ColorAccessibleView: View {
    @State private var isSelected = false
    
    var body: some View {
        VStack {
            // Good contrast example
            Text("Important Message")
                .foregroundColor(.white)
                .background(Color.black)
                .padding()
            
            // Color + shape indicator
            HStack {
                Circle()
                    .fill(isSelected ? Color.green : Color.red)
                    .frame(width: 20, height: 20)
                Text(isSelected ? "Online" : "Offline")
            }
            .accessibilityElement(children: .combine)
            .accessibilityLabel(isSelected ? "Status: Online" : "Status: Offline")
            
            Button(action: { isSelected.toggle() }) {
                Text("Toggle Status")
            }
            .accessibilityHint("Changes the online status indicator")
        }
    }
}
```