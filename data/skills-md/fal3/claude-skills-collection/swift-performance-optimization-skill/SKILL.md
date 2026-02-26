---
name: Swift Performance Optimization Skill
description: Techniques for optimizing Swift code performance, memory usage, rendering efficiency, and using Instruments for profiling.
version: 1.0
activation: Activate for queries on Swift performance optimization, memory management, rendering improvements, Instruments usage, or profiling Swift/iOS apps.
---

# Swift Performance Optimization Skill

This skill provides expertise in optimizing Swift code for better performance, memory efficiency, and smooth rendering. It covers profiling with Instruments, memory management best practices, and performance patterns specific to iOS development.

## Best Practices

1. **Profile First**: Always use Instruments to identify bottlenecks before optimizing.

2. **Memory Management**: Understand ARC, avoid retain cycles, and manage memory efficiently.

3. **Lazy Loading**: Defer expensive operations and use lazy properties when appropriate.

4. **Efficient Collections**: Choose the right data structures and operations for performance.

5. **UI Performance**: Optimize rendering with techniques like cell reuse and background processing.

6. **Concurrency**: Use GCD or Swift Concurrency for background tasks without blocking the main thread.

## Performance Guidelines

- Minimize work on the main thread, especially UI updates.
- Use Instruments Time Profiler to find CPU hotspots.
- Monitor memory usage with Allocations and Leaks instruments.
- Optimize images and assets for size and loading.
- Cache expensive computations when possible.
- Avoid unnecessary view updates in SwiftUI with proper state management.

## Examples

### Example 1: Optimizing SwiftUI List Performance

**User Prompt:** "How can I optimize a SwiftUI List with many items that's scrolling slowly?"

**Expected Output:**
```swift
import SwiftUI

struct OptimizedListView: View {
    let items = Array(1...10000) // Large dataset
    
    var body: some View {
        List(items, id: \.self) { item in
            OptimizedRowView(item: item)
        }
        .listStyle(.plain)
    }
}

struct OptimizedRowView: View {
    let item: Int
    
    var body: some View {
        HStack {
            Text("Item \(item)")
            Spacer()
            Image(systemName: "star")
                .foregroundColor(.yellow)
        }
        .padding(.vertical, 8)
        // Avoid complex computations in body
        // Use @StateObject for view models if needed
    }
}

// For even better performance with large datasets:
struct LazyOptimizedListView: View {
    let items = Array(1...10000)
    
    var body: some View {
        ScrollView {
            LazyVStack {
                ForEach(items, id: \.self) { item in
                    OptimizedRowView(item: item)
                }
            }
        }
    }
}
```

### Example 2: Memory Management with Weak References

**User Prompt:** "Fix a potential memory leak in a closure capturing self."

**Expected Output:**
```swift
class NetworkManager {
    var completionHandler: (() -> Void)?
    
    func fetchData() {
        // BAD: Strong reference cycle
        // self.completionHandler = {
        //     self.processData()
        // }
        
        // GOOD: Weak self to avoid retain cycle
        self.completionHandler = { [weak self] in
            self?.processData()
        }
        
        // Simulate network call
        DispatchQueue.global().asyncAfter(deadline: .now() + 1) {
            self.completionHandler?()
        }
    }
    
    func processData() {
        print("Data processed")
    }
}

// Alternative with unowned for non-optional self
class ViewController {
    var timer: Timer?
    
    func startTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [unowned self] timer in
            self.updateUI()
        }
    }
    
    func updateUI() {
        // Update UI
    }
}
```

### Example 3: Instruments Time Profiler Usage

**User Prompt:** "How do I use Instruments to profile CPU performance in my Swift app?"

**Expected Output:**
To profile CPU performance:

1. Open Xcode and select Product > Profile (⌘I)
2. Choose "Time Profiler" from the Instruments template
3. Click the record button to start profiling
4. Perform the actions you want to profile in your app
5. Stop recording and examine the call tree
6. Look for methods with high "Self" time (time spent in that method itself)
7. Expand the heaviest stack trace to identify bottlenecks

Key Time Profiler tips:
- Focus on "Self" column for time spent in each method
- Use "Invert Call Tree" to see bottom-up view
- Separate by thread to identify main thread blocking
- Look for recursive calls or unexpected frequent calls

Example findings:
- If `viewDidLoad()` takes 500ms, check for expensive operations
- Heavy `tableView(_:cellForRowAt:)` calls indicate list optimization needed
- Frequent `layoutSubviews()` suggests layout inefficiencies

### Example 4: Efficient Image Loading

**User Prompt:** "Optimize image loading and display in a collection view."

**Expected Output:**
```swift
import UIKit

class ImageCollectionViewCell: UICollectionViewCell {
    let imageView = UIImageView()
    private var imageLoadTask: URLSessionDataTask?
    
    override init(frame: CGRect) {
        super.init(frame: frame)
        setupViews()
    }
    
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    private func setupViews() {
        imageView.contentMode = .scaleAspectFill
        imageView.clipsToBounds = true
        contentView.addSubview(imageView)
        imageView.frame = contentView.bounds
    }
    
    func configure(with imageURL: URL) {
        // Cancel previous task
        imageLoadTask?.cancel()
        
        // Placeholder
        imageView.image = UIImage(named: "placeholder")
        
        // Load image asynchronously
        imageLoadTask = URLSession.shared.dataTask(with: imageURL) { [weak self] data, _, _ in
            guard let data = data, let image = UIImage(data: data) else { return }
            
            DispatchQueue.main.async {
                self?.imageView.image = image
            }
        }
        imageLoadTask?.resume()
    }
    
    override func prepareForReuse() {
        super.prepareForReuse()
        imageLoadTask?.cancel()
        imageView.image = nil
    }
}

// Usage in ViewController
class ImageGalleryViewController: UIViewController, UICollectionViewDataSource {
    let collectionView = UICollectionView(frame: .zero, collectionViewLayout: UICollectionViewFlowLayout())
    let imageURLs: [URL] = [] // Your image URLs
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "ImageCell", for: indexPath) as! ImageCollectionViewCell
        cell.configure(with: imageURLs[indexPath.item])
        return cell
    }
}
```

### Example 5: SwiftUI Rendering Optimization

**User Prompt:** "Optimize SwiftUI view updates to prevent unnecessary re-renders."

**Expected Output:**
```swift
import SwiftUI

// BAD: Causes re-render on every change
struct BadCounterView: View {
    @State private var count = 0
    @State private var name = "Counter"
    
    var body: some View {
        VStack {
            Text(name) // Re-renders when count changes
            Text("\(count)")
            Button("Increment") { count += 1 }
        }
    }
}

// GOOD: Separate concerns
struct OptimizedCounterView: View {
    @State private var count = 0
    
    var body: some View {
        VStack {
            CounterTitleView() // Only re-renders when needed
            CounterDisplayView(count: count)
            CounterButtonView(count: $count)
        }
    }
}

struct CounterTitleView: View {
    var body: some View {
        Text("Counter")
    }
}

struct CounterDisplayView: View {
    let count: Int
    
    var body: some View {
        Text("\(count)")
    }
}

struct CounterButtonView: View {
    @Binding var count: Int
    
    var body: some View {
        Button("Increment") { count += 1 }
    }
}

// Alternative: Use Equatable for custom comparisons
struct EquatableView: View, Equatable {
    let title: String
    let count: Int
    
    var body: some View {
        VStack {
            Text(title)
            Text("\(count)")
        }
    }
    
    static func == (lhs: EquatableView, rhs: EquatableView) -> Bool {
        lhs.title == rhs.title && lhs.count == rhs.count
    }
}
```