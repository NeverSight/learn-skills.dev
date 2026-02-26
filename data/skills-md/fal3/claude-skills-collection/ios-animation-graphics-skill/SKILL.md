---
name: iOS Animation Graphics Skill
description: Creating animations and graphics using SwiftUI Canvas, Core Animation, and Lottie integration for engaging iOS app experiences.
version: 1.0
activation: Activate for queries on iOS animations, SwiftUI Canvas usage, Lottie integration, Core Animation, or custom graphics creation.
---

# iOS Animation Graphics Skill

This skill provides expertise in creating smooth animations and custom graphics for iOS applications using SwiftUI Canvas, Core Animation, and Lottie. It covers animation principles, performance considerations, and integration with Apple's design system.

## Best Practices

1. **Performance First**: Use lightweight animations that don't impact scrolling or user interaction.

2. **Meaningful Motion**: Ensure animations enhance user experience and provide visual feedback.

3. **Consistent Timing**: Use standard animation durations (0.2-0.5 seconds) for familiarity.

4. **Hardware Acceleration**: Leverage GPU-accelerated properties for smooth animations.

5. **Accessibility**: Respect reduced motion preferences and provide alternatives.

6. **State-Driven**: Bind animations to view state for automatic updates.

## Animation Guidelines

- Use SwiftUI's built-in animation modifiers for simple transitions.
- Implement Canvas for custom drawings and complex graphics.
- Integrate Lottie for designer-created animations.
- Combine multiple animation techniques for rich interactions.
- Test animations on actual devices for performance.
- Consider different screen sizes and orientations.

## Examples

### Example 1: Basic SwiftUI Animations

**User Prompt:** "Create a button that scales and changes color when tapped using SwiftUI animations."

**Expected Output:**
```swift
import SwiftUI

struct AnimatedButton: View {
    @State private var isPressed = false
    @State private var tapCount = 0
    
    var body: some View {
        ZStack {
            Circle()
                .fill(isPressed ? Color.blue : Color.red)
                .frame(width: isPressed ? 120 : 100, height: isPressed ? 120 : 100)
                .shadow(radius: isPressed ? 10 : 5)
                .animation(.spring(response: 0.3, dampingFraction: 0.6), value: isPressed)
            
            Text("\(tapCount)")
                .font(.title)
                .foregroundColor(.white)
                .scaleEffect(isPressed ? 1.2 : 1.0)
                .animation(.easeInOut(duration: 0.2), value: isPressed)
        }
        .onTapGesture {
            isPressed.toggle()
            tapCount += 1
            
            // Reset after animation
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
                isPressed = false
            }
        }
    }
}

// Advanced example with multiple animations
struct ComplexAnimatedView: View {
    @State private var isAnimating = false
    
    var body: some View {
        VStack(spacing: 20) {
            RoundedRectangle(cornerRadius: 20)
                .fill(Color.blue)
                .frame(width: isAnimating ? 200 : 100, height: 100)
                .rotationEffect(.degrees(isAnimating ? 360 : 0))
                .offset(y: isAnimating ? -50 : 0)
                .animation(.interpolatingSpring(mass: 1.0, stiffness: 100, damping: 10, initialVelocity: 0), value: isAnimating)
            
            Button("Animate") {
                isAnimating.toggle()
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
```

### Example 2: SwiftUI Canvas for Custom Graphics

**User Prompt:** "Draw a custom animated waveform using SwiftUI Canvas."

**Expected Output:**
```swift
import SwiftUI

struct WaveformView: View {
    @State private var phase = 0.0
    
    var body: some View {
        VStack {
            Canvas { context, size in
                let width = size.width
                let height = size.height
                let centerY = height / 2
                
                // Draw waveform
                var path = Path()
                path.move(to: CGPoint(x: 0, y: centerY))
                
                for x in stride(from: 0, to: width, by: 1) {
                    let relativeX = x / width
                    let y = centerY + sin(relativeX * .pi * 4 + phase) * 30
                    path.addLine(to: CGPoint(x: x, y: y))
                }
                
                context.stroke(path, with: .color(.blue), lineWidth: 2)
                
                // Draw amplitude bars
                for i in 0..<10 {
                    let barHeight = abs(sin(phase + Double(i) * 0.5)) * 50
                    let barX = width * 0.1 * Double(i + 1)
                    
                    let barRect = CGRect(x: barX - 2, y: centerY - barHeight/2, width: 4, height: barHeight)
                    context.fill(Path(barRect), with: .color(.green.opacity(0.6)))
                }
            }
            .frame(height: 200)
            .background(Color.gray.opacity(0.1))
            .cornerRadius(10)
            
            Button("Animate Wave") {
                withAnimation(.linear(duration: 2).repeatForever(autoreverses: false)) {
                    phase += .pi * 2
                }
            }
            .buttonStyle(.bordered)
        }
        .padding()
    }
}

// Interactive canvas example
struct DrawingCanvas: View {
    @State private var paths: [Path] = []
    @State private var currentPath = Path()
    @State private var isDrawing = false
    
    var body: some View {
        VStack {
            Canvas { context, size in
                for path in paths {
                    context.stroke(path, with: .color(.blue), lineWidth: 3)
                }
                context.stroke(currentPath, with: .color(.red), lineWidth: 3)
            }
            .frame(height: 300)
            .background(Color.white)
            .border(Color.gray, width: 1)
            .gesture(
                DragGesture(minimumDistance: 0)
                    .onChanged { value in
                        let point = value.location
                        if !isDrawing {
                            currentPath.move(to: point)
                            isDrawing = true
                        } else {
                            currentPath.addLine(to: point)
                        }
                    }
                    .onEnded { _ in
                        paths.append(currentPath)
                        currentPath = Path()
                        isDrawing = false
                    }
            )
            
            Button("Clear") {
                paths = []
                currentPath = Path()
            }
            .buttonStyle(.bordered)
        }
        .padding()
    }
}
```

### Example 3: Lottie Animation Integration

**User Prompt:** "Integrate a Lottie animation that plays on button tap."

**Expected Output:**
First, add Lottie to your project using Swift Package Manager:
- Add https://github.com/airbnb/lottie-ios.git

```swift
import SwiftUI
import Lottie

struct LottieAnimationView: View {
    @State private var isPlaying = false
    @State private var animationView: LottieAnimationView?
    
    var body: some View {
        VStack(spacing: 20) {
            // Lottie Animation Container
            ZStack {
                Color.gray.opacity(0.1)
                    .frame(height: 200)
                    .cornerRadius(10)
                
                if let animationView = animationView {
                    LottieView(animationView: animationView)
                        .frame(height: 200)
                } else {
                    Text("Loading animation...")
                        .foregroundColor(.secondary)
                }
            }
            
            HStack(spacing: 20) {
                Button(action: {
                    playAnimation()
                }) {
                    Label("Play", systemImage: "play.fill")
                }
                .buttonStyle(.borderedProminent)
                .disabled(isPlaying)
                
                Button(action: {
                    stopAnimation()
                }) {
                    Label("Stop", systemImage: "stop.fill")
                }
                .buttonStyle(.bordered)
                .disabled(!isPlaying)
            }
        }
        .padding()
        .onAppear {
            loadAnimation()
        }
    }
    
    private func loadAnimation() {
        // Load animation from bundle (you would add the JSON file to your project)
        if let animation = LottieAnimation.named("celebration") {
            animationView = LottieAnimationView(animation: animation)
            animationView?.loopMode = .playOnce
        }
    }
    
    private func playAnimation() {
        isPlaying = true
        animationView?.play { _ in
            isPlaying = false
        }
    }
    
    private func stopAnimation() {
        animationView?.stop()
        isPlaying = false
    }
}

// UIViewRepresentable wrapper for Lottie
struct LottieView: UIViewRepresentable {
    let animationView: LottieAnimationView
    
    func makeUIView(context: Context) -> UIView {
        let view = UIView()
        view.addSubview(animationView)
        animationView.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            animationView.topAnchor.constraint(equalTo: view.topAnchor),
            animationView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
            animationView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            animationView.trailingAnchor.constraint(equalTo: view.trailingAnchor)
        ])
        return view
    }
    
    func updateUIView(_ uiView: UIView, context: Context) {
        // Update if needed
    }
}

// Alternative: Using Lottie with SwiftUI state
struct StatefulLottieView: View {
    @State private var play = false
    
    var body: some View {
        VStack {
            LottieView(animation: .named("loading"))
                .playbackMode(.playing(.toProgress(1, loopMode: .loop)))
                .frame(height: 100)
            
            Button("Toggle Animation") {
                play.toggle()
            }
            .buttonStyle(.bordered)
        }
    }
}
```

### Example 4: Core Animation with UIViewRepresentable

**User Prompt:** "Create a UIViewRepresentable that uses Core Animation for a rotating gradient border."

**Expected Output:**
```swift
import SwiftUI
import UIKit

struct RotatingGradientBorder: View {
    @State private var isAnimating = false
    
    var body: some View {
        ZStack {
            GradientBorderView(isAnimating: $isAnimating)
                .frame(width: 150, height: 150)
            
            Button(action: {
                isAnimating.toggle()
            }) {
                Text(isAnimating ? "Stop" : "Start")
                    .foregroundColor(.white)
                    .padding()
                    .background(Color.blue.opacity(0.8))
                    .cornerRadius(10)
            }
        }
    }
}

struct GradientBorderView: UIViewRepresentable {
    @Binding var isAnimating: Bool
    
    func makeUIView(context: Context) -> UIView {
        let view = UIView()
        view.backgroundColor = .clear
        
        // Create gradient layer
        let gradientLayer = CAGradientLayer()
        gradientLayer.colors = [UIColor.red.cgColor, UIColor.blue.cgColor, UIColor.green.cgColor, UIColor.red.cgColor]
        gradientLayer.startPoint = CGPoint(x: 0, y: 0)
        gradientLayer.endPoint = CGPoint(x: 1, y: 1)
        gradientLayer.frame = view.bounds
        
        // Create shape layer for border
        let shapeLayer = CAShapeLayer()
        shapeLayer.lineWidth = 4
        shapeLayer.fillColor = UIColor.clear.cgColor
        shapeLayer.strokeColor = UIColor.black.cgColor
        shapeLayer.path = UIBezierPath(roundedRect: view.bounds.insetBy(dx: 2, dy: 2), cornerRadius: 20).cgPath
        
        // Mask gradient with shape
        gradientLayer.mask = shapeLayer
        
        // Add rotation animation
        let rotationAnimation = CABasicAnimation(keyPath: "transform.rotation.z")
        rotationAnimation.fromValue = 0
        rotationAnimation.toValue = CGFloat.pi * 2
        rotationAnimation.duration = 2.0
        rotationAnimation.repeatCount = .infinity
        
        context.coordinator.animation = rotationAnimation
        context.coordinator.gradientLayer = gradientLayer
        
        view.layer.addSublayer(gradientLayer)
        
        return view
    }
    
    func updateUIView(_ uiView: UIView, context: Context) {
        if isAnimating {
            context.coordinator.gradientLayer?.add(context.coordinator.animation!, forKey: "rotation")
        } else {
            context.coordinator.gradientLayer?.removeAnimation(forKey: "rotation")
        }
    }
    
    func makeCoordinator() -> Coordinator {
        Coordinator()
    }
    
    class Coordinator {
        var animation: CABasicAnimation?
        var gradientLayer: CAGradientLayer?
    }
}

// Advanced Core Animation example
struct ParticleSystemView: UIViewRepresentable {
    func makeUIView(context: Context) -> UIView {
        let view = UIView()
        
        // Create particle emitter
        let emitter = CAEmitterLayer()
        emitter.emitterPosition = CGPoint(x: 200, y: 100)
        emitter.emitterSize = CGSize(width: 10, height: 10)
        emitter.emitterShape = .circle
        
        // Create particle cell
        let cell = CAEmitterCell()
        cell.birthRate = 50
        cell.lifetime = 2.0
        cell.velocity = 100
        cell.velocityRange = 50
        cell.emissionRange = .pi * 2
        cell.scale = 0.1
        cell.scaleRange = 0.05
        cell.contents = UIImage(systemName: "star.fill")?.cgImage
        cell.color = UIColor.blue.cgColor
        
        emitter.emitterCells = [cell]
        view.layer.addSublayer(emitter)
        
        return view
    }
    
    func updateUIView(_ uiView: UIView, context: Context) {
        // Update if needed
    }
}
```

### Example 5: Matched Geometry Effect

**User Prompt:** "Implement a hero transition between two views using SwiftUI's matchedGeometryEffect."

**Expected Output:**
```swift
import SwiftUI

struct HeroTransitionView: View {
    @State private var selectedItem: Item?
    @Namespace private var namespace
    
    let items = [
        Item(id: 1, title: "Mountain", imageName: "mountain", description: "A beautiful mountain landscape"),
        Item(id: 2, title: "Ocean", imageName: "ocean", description: "Peaceful ocean waves"),
        Item(id: 3, title: "Forest", imageName: "forest", description: "Lush green forest")
    ]
    
    var body: some View {
        ZStack {
            if let selectedItem = selectedItem {
                DetailView(item: selectedItem, namespace: namespace)
                    .onTapGesture {
                        withAnimation(.spring()) {
                            self.selectedItem = nil
                        }
                    }
            } else {
                GridView(items: items, selectedItem: $selectedItem, namespace: namespace)
            }
        }
    }
}

struct GridView: View {
    let items: [Item]
    @Binding var selectedItem: Item?
    let namespace: Namespace.ID
    
    var body: some View {
        ScrollView {
            LazyVGrid(columns: [GridItem(.adaptive(minimum: 150))], spacing: 16) {
                ForEach(items) { item in
                    GridItemView(item: item, namespace: namespace)
                        .onTapGesture {
                            withAnimation(.spring()) {
                                selectedItem = item
                            }
                        }
                }
            }
            .padding()
        }
    }
}

struct GridItemView: View {
    let item: Item
    let namespace: Namespace.ID
    
    var body: some View {
        VStack {
            Image(item.imageName)
                .resizable()
                .aspectRatio(contentMode: .fill)
                .frame(height: 100)
                .clipped()
                .cornerRadius(8)
                .matchedGeometryEffect(id: item.id, in: namespace)
            
            Text(item.title)
                .font(.caption)
                .foregroundColor(.primary)
        }
        .background(Color.white)
        .cornerRadius(8)
        .shadow(radius: 2)
    }
}

struct DetailView: View {
    let item: Item
    let namespace: Namespace.ID
    
    var body: some View {
        VStack {
            Spacer()
            
            Image(item.imageName)
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(maxHeight: 300)
                .clipped()
                .cornerRadius(16)
                .matchedGeometryEffect(id: item.id, in: namespace)
                .padding()
            
            Text(item.title)
                .font(.largeTitle)
                .foregroundColor(.primary)
            
            Text(item.description)
                .font(.body)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
                .padding()
            
            Spacer()
        }
        .background(Color.white)
        .edgesIgnoringSafeArea(.all)
    }
}

struct Item: Identifiable {
    let id: Int
    let title: String
    let imageName: String
    let description: String
}
```

Note: For the image examples above, you would need to add actual images to your asset catalog or use system images.