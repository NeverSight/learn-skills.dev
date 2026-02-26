---
name: Memory Leak Diagnosis Skill
description: Detecting and fixing memory leaks and retain cycles in Swift apps using Instruments and best practices.
version: 1.0
activation: Activate for queries on memory leaks, retain cycles, Instruments leaks detection, ARC issues, or memory management problems.
---

# Memory Leak Diagnosis Skill

This skill provides expertise in identifying, diagnosing, and fixing memory leaks and retain cycles in Swift applications. It covers Instruments usage, ARC concepts, and memory management best practices for iOS development.

## Best Practices

1. **Understand ARC**: Automatic Reference Counting manages memory automatically, but cycles can still occur.

2. **Use Weak References**: Break retain cycles by using `weak` or `unowned` references in closures and delegates.

3. **Profile Regularly**: Use Instruments to detect leaks early in development.

4. **Avoid Strong Reference Cycles**: Be aware of parent-child relationships and delegate patterns.

5. **Clean Up Resources**: Properly invalidate timers, cancel network requests, and remove observers.

6. **Test Memory Usage**: Monitor memory growth during app usage.

## Memory Management Guidelines

- Classes create strong references by default.
- Use `weak` for optional relationships that can become nil.
- Use `unowned` for non-optional relationships that will always exist.
- Capture `self` weakly in closures to prevent retain cycles.
- Use Instruments Leaks and Allocations instruments for diagnosis.
- Monitor memory usage with Xcode's Memory Graph Debugger.

## Examples

### Example 1: Fixing Retain Cycles in Closures

**User Prompt:** "Fix the retain cycle in this network manager that uses a completion handler."

**Expected Output:**
```swift
import Foundation

// PROBLEMATIC CODE - Retain Cycle
class NetworkManagerBad {
    var completionHandler: (() -> Void)?
    
    func fetchData() {
        // This creates a retain cycle: self -> completionHandler -> self
        self.completionHandler = {
            print("Data fetched")
            self.processData() // 'self' is strongly captured
        }
        
        // Simulate async operation
        DispatchQueue.global().asyncAfter(deadline: .now() + 1) {
            self.completionHandler?()
        }
    }
    
    func processData() {
        print("Processing data")
    }
    
    deinit {
        print("NetworkManagerBad deallocated")
    }
}

// FIXED CODE - Using weak self
class NetworkManagerGood {
    var completionHandler: (() -> Void)?
    
    func fetchData() {
        // Use [weak self] to break the retain cycle
        self.completionHandler = { [weak self] in
            print("Data fetched")
            self?.processData() // 'self' is now weakly captured
        }
        
        // Simulate async operation
        DispatchQueue.global().asyncAfter(deadline: .now() + 1) {
            self.completionHandler?()
        }
    }
    
    func processData() {
        print("Processing data")
    }
    
    deinit {
        print("NetworkManagerGood deallocated") // This will now print!
    }
}

// Alternative: Using unowned for guaranteed non-nil self
class NetworkManagerUnowned {
    var completionHandler: (() -> Void)?
    
    func fetchData() {
        // Use [unowned self] if you're certain self won't be nil
        self.completionHandler = { [unowned self] in
            print("Data fetched")
            self.processData() // No optional chaining needed
        }
        
        DispatchQueue.global().asyncAfter(deadline: .now() + 1) {
            self.completionHandler?()
        }
    }
    
    func processData() {
        print("Processing data")
    }
    
    deinit {
        print("NetworkManagerUnowned deallocated")
    }
}

// Usage example
func testMemoryLeak() {
    print("Creating NetworkManagerBad...")
    var managerBad: NetworkManagerBad? = NetworkManagerBad()
    managerBad?.fetchData()
    managerBad = nil // Won't deallocate due to retain cycle
    
    print("Creating NetworkManagerGood...")
    var managerGood: NetworkManagerGood? = NetworkManagerGood()
    managerGood?.fetchData()
    managerGood = nil // Will deallocate properly
    
    // Give time for async operations
    RunLoop.current.run(until: Date(timeIntervalSinceNow: 2))
}
```

### Example 2: Delegate Pattern Retain Cycles

**User Prompt:** "Fix the retain cycle between a view controller and its delegate."

**Expected Output:**
```swift
import UIKit

// PROBLEMATIC CODE
protocol DataManagerDelegateBad: AnyObject {
    func dataDidUpdate(_ data: [String])
}

class DataManagerBad {
    weak var delegate: DataManagerDelegateBad? // This is correct
    
    func fetchData() {
        // Simulate network call
        DispatchQueue.global().asyncAfter(deadline: .now() + 1) {
            let data = ["Item 1", "Item 2", "Item 3"]
            self.delegate?.dataDidUpdate(data)
        }
    }
}

class ViewControllerBad: UIViewController, DataManagerDelegateBad {
    var dataManager: DataManagerBad?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        dataManager = DataManagerBad()
        dataManager?.delegate = self // This creates: VC -> dataManager -> delegate -> VC
        
        dataManager?.fetchData()
    }
    
    func dataDidUpdate(_ data: [String]) {
        print("Received data: \(data)")
    }
    
    deinit {
        print("ViewControllerBad deallocated")
    }
}

// The issue is that ViewController strongly holds DataManager,
// DataManager weakly holds the delegate (ViewController),
// but the closure in fetchData strongly captures self (DataManager).
// When ViewController is dismissed, DataManager's closure keeps it alive.

// FIXED CODE
protocol DataManagerDelegate: AnyObject {
    func dataDidUpdate(_ data: [String])
}

class DataManager {
    weak var delegate: DataManagerDelegate?
    
    func fetchData() {
        // Use [weak self] in the closure to break any potential cycle
        DispatchQueue.global().asyncAfter(deadline: .now() + 1) { [weak self] in
            let data = ["Item 1", "Item 2", "Item 3"]
            self?.delegate?.dataDidUpdate(data)
        }
    }
    
    deinit {
        print("DataManager deallocated")
    }
}

class ViewController: UIViewController, DataManagerDelegate {
    var dataManager: DataManager?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        dataManager = DataManager()
        dataManager?.delegate = self
        
        dataManager?.fetchData()
    }
    
    func dataDidUpdate(_ data: [String]) {
        print("Received data: \(data)")
    }
    
    deinit {
        print("ViewController deallocated") // This will now print!
    }
}

// Alternative pattern: Using a closure instead of delegate
class DataManagerClosure {
    var onDataUpdate: (([String]) -> Void)?
    
    func fetchData() {
        DispatchQueue.global().asyncAfter(deadline: .now() + 1) { [weak self] in
            let data = ["Item 1", "Item 2", "Item 3"]
            self?.onDataUpdate?(data)
        }
    }
    
    deinit {
        print("DataManagerClosure deallocated")
    }
}

class ViewControllerClosure: UIViewController {
    var dataManager: DataManagerClosure?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        dataManager = DataManagerClosure()
        // Use [weak self] to avoid retain cycle
        dataManager?.onDataUpdate = { [weak self] data in
            print("Received data: \(data)")
        }
        
        dataManager?.fetchData()
    }
    
    deinit {
        print("ViewControllerClosure deallocated")
    }
}
```

### Example 3: Instruments Leaks Detection

**User Prompt:** "How do I use Instruments to detect memory leaks in my iOS app?"

**Expected Output:**
To detect memory leaks using Instruments:

1. **Open Instruments**: In Xcode, go to Product > Profile (⌘I)

2. **Choose Leaks Instrument**: Select the "Leaks" template

3. **Configure Recording**:
   - Target your app
   - Make sure "Record reference counts" is enabled
   - Start recording

4. **Use Your App**: Navigate through the screens where you suspect leaks

5. **Analyze Results**:
   - Look for red bars in the Leaks track - these indicate memory leaks
   - The Detail pane shows leaked objects and their allocation backtraces
   - Use the "Cycles & Roots" view to see retain cycles

6. **Identify the Problem**:
   - Click on a leak to see the allocation history
   - Look for objects that should have been deallocated but weren't
   - Check for strong reference cycles

**Example Leaks Output Interpretation:**

```
Leaks detected: 5
- Leaked Object: ViewController (0x7f9b8c0a5e00)
  - Responsible Library: UIKit
  - Allocation: -[UIViewController initWithNibName:bundle:]
  - Backtrace shows it was created in viewDidLoad of parent VC
  - Never deallocated because of retain cycle with timer

- Leaked Object: Timer (0x7f9b8c0a6120)
  - Responsible Library: Foundation
  - Allocation: +[NSTimer scheduledTimerWithTimeInterval:target:selector:userInfo:repeats:]
  - Strong reference to target (ViewController) prevents deallocation
```

**Common Leak Patterns to Look For:**

1. **Timer Retain Cycles**:
```swift
// BAD
class MyViewController: UIViewController {
    var timer: Timer?
    
    func startTimer() {
        timer = Timer.scheduledTimer(timeInterval: 1.0, target: self, selector: #selector(update), userInfo: nil, repeats: true)
    }
    
    @objc func update() {
        // Update UI
    }
}

// GOOD
class MyViewController: UIViewController {
    var timer: Timer?
    
    func startTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.update()
        }
    }
    
    func update() {
        // Update UI
    }
    
    deinit {
        timer?.invalidate()
    }
}
```

2. **Closure Capture Issues**:
```swift
// BAD
var completion: (() -> Void)?
completion = {
    self.doSomething() // Creates retain cycle
}

// GOOD  
completion = { [weak self] in
    self?.doSomething() // Breaks the cycle
}
```

3. **Delegate Strong References**:
```swift
// BAD
class MyObject {
    var delegate: MyDelegate? // Strong reference
}

// GOOD
class MyObject {
    weak var delegate: MyDelegate? // Weak reference
}
```

### Example 4: Memory Graph Debugger

**User Prompt:** "Use Xcode's Memory Graph Debugger to identify and fix a retain cycle."

**Expected Output:**
To use the Memory Graph Debugger:

1. **Enable Memory Graph**: In Xcode, go to Debug > Debug Workflow > View Memory Graph (⌘⌃M)

2. **Trigger the Debugger**: Run your app and navigate to create the suspected leak

3. **Analyze the Graph**:
   - Look for objects that should be deallocated but remain in memory
   - Purple arrows show strong references
   - Gray arrows show weak references
   - Numbers show reference counts

4. **Inspect Objects**: Click on objects to see their properties and references

5. **Find Cycles**: Look for circular references where objects keep each other alive

**Example Memory Graph Analysis:**

```
Root View Controller (ref count: 1)
├── Strong reference to Data Manager (ref count: 2)
│   ├── Strong reference to Network Client (ref count: 1)
│   └── Strong reference to Delegate (View Controller) (ref count: 1)
│       └── Strong reference back to Data Manager
└── Strong reference to Timer (ref count: 1)
    └── Strong reference to Timer Target (View Controller)
```

**Fixing the Cycle:**

```swift
class DataManager {
    weak var delegate: DataManagerDelegate? // Change to weak
    
    private var timer: Timer?
    
    func startPolling() {
        timer = Timer.scheduledTimer(withTimeInterval: 5.0, repeats: true) { [weak self] _ in
            self?.fetchData()
        }
    }
    
    func stopPolling() {
        timer?.invalidate()
        timer = nil
    }
    
    private func fetchData() {
        // Network request with [weak self] in completion
        networkClient.fetch { [weak self] result in
            switch result {
            case .success(let data):
                self?.delegate?.dataDidUpdate(data)
            case .failure:
                break
            }
        }
    }
}

class ViewController: UIViewController, DataManagerDelegate {
    private let dataManager = DataManager()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        dataManager.delegate = self
        dataManager.startPolling()
    }
    
    override func viewDidDisappear(_ animated: Bool) {
        super.viewDidDisappear(animated)
        dataManager.stopPolling() // Clean up timer
    }
    
    func dataDidUpdate(_ data: [String]) {
        // Update UI
    }
}
```

### Example 5: ARC and Reference Types

**User Prompt:** "Explain and fix ARC-related memory issues in a complex object graph."

**Expected Output:**
```swift
import Foundation

// Understanding Reference Types
class Person {
    let name: String
    var car: Car?
    
    init(name: String) {
        self.name = name
        print("\(name) initialized")
    }
    
    deinit {
        print("\(name) deinitialized")
    }
}

class Car {
    let model: String
    weak var owner: Person? // Use weak to prevent cycle
    
    init(model: String) {
        self.model = model
        print("\(model) initialized")
    }
    
    deinit {
        print("\(model) deinitialized")
    }
}

// BAD EXAMPLE - Retain Cycle
func createRetainCycle() {
    print("=== Creating Retain Cycle ===")
    var person: Person? = Person(name: "John") // ref count: 1
    var car: Car? = Car(model: "Tesla")        // ref count: 1
    
    person?.car = car      // car ref count: 2 (person + car variable)
    car?.owner = person    // person ref count: 2 (car + person variable)
    
    person = nil // person ref count: 1 (still held by car.owner)
    car = nil    // car ref count: 1 (still held by person.car)
    
    // Neither object is deallocated!
    print("=== Memory leak occurred ===")
}

// GOOD EXAMPLE - No Retain Cycle
func createNoRetainCycle() {
    print("=== No Retain Cycle ===")
    var person: Person? = Person(name: "Jane") // ref count: 1
    var car: Car? = Car(model: "Honda")        // ref count: 1
    
    person?.car = car      // car ref count: 2
    car?.owner = person    // person ref count: 1 (weak reference!)
    
    person = nil // person ref count: 0 -> deallocated
    car = nil    // car ref count: 0 -> deallocated
    
    print("=== Both objects properly deallocated ===")
}

// Complex Object Graph Example
class Company {
    let name: String
    var employees: [Employee] = []
    
    init(name: String) {
        self.name = name
        print("Company \(name) initialized")
    }
    
    deinit {
        print("Company \(name) deinitialized")
    }
}

class Employee {
    let name: String
    unowned let company: Company // unowned because company owns employee
    
    init(name: String, company: Company) {
        self.name = name
        self.company = company
        print("Employee \(name) initialized")
    }
    
    deinit {
        print("Employee \(name) deinitialized")
    }
}

func testComplexGraph() {
    print("=== Complex Object Graph ===")
    var company: Company? = Company(name: "Apple")
    
    // Create employees - company owns them strongly
    let employee1 = Employee(name: "John", company: company!)
    let employee2 = Employee(name: "Jane", company: company!)
    
    company?.employees = [employee1, employee2]
    
    company = nil // This will deallocate company AND all employees
    
    print("=== Complex graph deallocated ===")
}

// Value Types vs Reference Types
struct Address {
    var street: String
    var city: String
}

class PersonWithAddress {
    let name: String
    var address: Address // Value type - copied, not referenced
    
    init(name: String, address: Address) {
        self.name = name
        self.address = address
    }
}

func testValueVsReference() {
    let address = Address(street: "123 Main St", city: "Springfield")
    var person1: PersonWithAddress? = PersonWithAddress(name: "John", address: address)
    var person2: PersonWithAddress? = PersonWithAddress(name: "Jane", address: address)
    
    person1?.address.city = "Changed City" // Only affects person1's copy
    
    print("Person1 city: \(person1?.address.city ?? "")")
    print("Person2 city: \(person2?.address.city ?? "")")
    
    person1 = nil // Only person1's struct is deallocated
    person2 = nil // Only person2's struct is deallocated
    // address was copied, so no reference counting involved
}
```

**Key ARC Concepts:**

1. **Strong References** (default): Increase reference count
2. **Weak References**: Don't increase reference count, automatically nil when object deallocated
3. **Unowned References**: Don't increase reference count, assume object won't be deallocated
4. **Value Types** (struct, enum): Copied, not referenced - no retain cycles possible
5. **Reference Types** (class): Shared instances - retain cycles possible

**When to use each:**

- `strong`: Default, use for owned relationships
- `weak`: When reference can become nil, like delegates, parent references
- `unowned`: When reference will never be nil during its lifetime, like self in closures where object owns the closure