---
name: type4me-macos-voice-input
description: MacOS voice input tool with local/cloud ASR engines, LLM text optimization, and fully local storage built in Swift
triggers:
  - add a new ASR provider to type4me
  - build and deploy type4me from source
  - configure local voice recognition with sherpa
  - set up volcengine speech recognition
  - add custom prompt mode for voice input
  - implement speech recognizer protocol
  - troubleshoot type4me voice input not working
  - extend type4me with new cloud ASR service

---

# Type4Me macOS Voice Input

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Type4Me is a macOS voice input tool that captures audio via global hotkey, transcribes it using local (SherpaOnnx/Paraformer/Zipformer) or cloud (Volcengine/Deepgram) ASR engines, optionally post-processes text via LLM, and injects the result into any app. All credentials and history are stored locally — no telemetry, no cloud sync.

## Architecture Overview

```
Type4Me/
├── ASR/                    # ASR engine abstraction
│   ├── ASRProvider.swift          # Provider enum + protocols
│   ├── ASRProviderRegistry.swift  # Plugin registry
│   ├── Providers/                 # Per-vendor config files
│   ├── SherpaASRClient.swift      # Local streaming ASR
│   ├── SherpaOfflineASRClient.swift
│   ├── VolcASRClient.swift        # Volcengine streaming ASR
│   └── DeepgramASRClient.swift    # Deepgram streaming ASR
├── Bridge/                 # SherpaOnnx C API Swift bridge
├── Audio/                  # Audio capture
├── Session/                # Core state machine: record→ASR→inject
├── Input/                  # Global hotkey management
├── Services/               # Credentials, hotwords, model manager
├── Protocol/               # Volcengine WebSocket codec
└── UI/                     # SwiftUI (FloatingBar + Settings)
```

## Installation

### Prerequisites

```bash
# Xcode Command Line Tools
xcode-select --install

# CMake (for local ASR engine)
brew install cmake
```

### Build & Deploy from Source

```bash
git clone https://github.com/joewongjc/type4me.git
cd type4me

# Step 1: Compile SherpaOnnx local engine (~5 min, one-time)
bash scripts/build-sherpa.sh

# Step 2: Build, bundle, sign, install to /Applications, and launch
bash scripts/deploy.sh
```

### Download Pre-built App

Download `Type4Me-v1.2.3.dmg` from releases (cloud ASR only, no local engine):
```
https://github.com/joewongjc/type4me/releases/tag/v1.2.3
```

If macOS blocks the app:
```bash
xattr -d com.apple.quarantine /Applications/Type4Me.app
```

### Download Local ASR Models

```bash
mkdir -p ~/Library/Application\ Support/Type4Me/Models

# Option A: Lightweight ~20MB
tar xjf ~/Downloads/sherpa-onnx-streaming-zipformer-small-ctc-zh-int8-2025-04-01.tar.bz2 \
    -C ~/Library/Application\ Support/Type4Me/Models/

# Option B: Balanced ~236MB (recommended)
tar xjf ~/Downloads/sherpa-onnx-streaming-zipformer-ctc-multi-zh-hans-2023-12-13.tar.bz2 \
    -C ~/Library/Application\ Support/Type4Me/Models/

# Option C: Bilingual Chinese+English ~1GB
tar xjf ~/Downloads/sherpa-onnx-streaming-paraformer-bilingual-zh-en.tar.bz2 \
    -C ~/Library/Application\ Support/Type4Me/Models/
```

Expected structure for Paraformer model:
```
~/Library/Application Support/Type4Me/Models/
└── sherpa-onnx-streaming-paraformer-bilingual-zh-en/
    ├── encoder.int8.onnx
    ├── decoder.int8.onnx
    └── tokens.txt
```

## Key Protocols

### SpeechRecognizer Protocol

Every ASR client must implement this protocol:

```swift
protocol SpeechRecognizer: AnyObject {
    /// Start a new recognition session
    func startRecognition() async throws
    
    /// Feed raw PCM audio data
    func appendAudio(_ buffer: AVAudioPCMBuffer) async
    
    /// Stop and get final result
    func stopRecognition() async throws -> String
    
    /// Cancel without result
    func cancelRecognition() async
    
    /// Streaming partial results (optional)
    var partialResultHandler: ((String) -> Void)? { get set }
}
```

### ASRProviderConfig Protocol

Each vendor's credential definition:

```swift
protocol ASRProviderConfig {
    /// Unique identifier string
    static var providerID: String { get }
    
    /// Display name in Settings UI
    static var displayName: String { get }
    
    /// Credential fields shown in Settings
    static var credentialFields: [CredentialField] { get }
    
    /// Validate credentials before use
    static func validate(_ credentials: [String: String]) -> Bool
    
    /// Create the recognizer instance
    static func createClient(
        credentials: [String: String],
        config: RecognitionConfig
    ) throws -> SpeechRecognizer
}
```

## Adding a New ASR Provider

### Step 1: Create Provider Config

Create `Type4Me/ASR/Providers/OpenAIWhisperProvider.swift`:

```swift
import Foundation

struct OpenAIWhisperProvider: ASRProviderConfig {
    static let providerID = "openai_whisper"
    static let displayName = "OpenAI Whisper"
    
    static let credentialFields: [CredentialField] = [
        CredentialField(
            key: "api_key",
            label: "API Key",
            placeholder: "sk-...",
            isSecret: true
        ),
        CredentialField(
            key: "model",
            label: "Model",
            placeholder: "whisper-1",
            isSecret: false
        )
    ]
    
    static func validate(_ credentials: [String: String]) -> Bool {
        guard let apiKey = credentials["api_key"], !apiKey.isEmpty else {
            return false
        }
        return apiKey.hasPrefix("sk-")
    }
    
    static func createClient(
        credentials: [String: String],
        config: RecognitionConfig
    ) throws -> SpeechRecognizer {
        guard let apiKey = credentials["api_key"] else {
            throw ASRError.missingCredential("api_key")
        }
        let model = credentials["model"] ?? "whisper-1"
        return OpenAIWhisperASRClient(apiKey: apiKey, model: model, config: config)
    }
}
```

### Step 2: Implement the ASR Client

Create `Type4Me/ASR/OpenAIWhisperASRClient.swift`:

```swift
import Foundation
import AVFoundation

final class OpenAIWhisperASRClient: SpeechRecognizer {
    var partialResultHandler: ((String) -> Void)?
    
    private let apiKey: String
    private let model: String
    private let config: RecognitionConfig
    private var audioData: Data = Data()
    
    init(apiKey: String, model: String, config: RecognitionConfig) {
        self.apiKey = apiKey
        self.model = model
        self.config = config
    }
    
    func startRecognition() async throws {
        audioData = Data()
    }
    
    func appendAudio(_ buffer: AVAudioPCMBuffer) async {
        // Convert PCM buffer to raw bytes and accumulate
        guard let channelData = buffer.floatChannelData?[0] else { return }
        let frameCount = Int(buffer.frameLength)
        let bytes = UnsafeBufferPointer(start: channelData, count: frameCount)
        // Convert Float32 PCM to Int16 for Whisper API
        let int16Samples = bytes.map { sample -> Int16 in
            return Int16(max(-32768, min(32767, Int(sample * 32767))))
        }
        int16Samples.withUnsafeBytes { ptr in
            audioData.append(contentsOf: ptr)
        }
    }
    
    func stopRecognition() async throws -> String {
        // Build multipart form request to Whisper API
        var request = URLRequest(url: URL(string: "https://api.openai.com/v1/audio/transcriptions")!)
        request.httpMethod = "POST"
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        
        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", 
                        forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        // Append audio file part
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"audio.raw\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: audio/raw\r\n\r\n".data(using: .utf8)!)
        body.append(audioData)
        body.append("\r\n".data(using: .utf8)!)
        // Append model part
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"model\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(model)\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        let (data, response) = try await URLSession.shared.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw ASRError.networkError("Whisper API returned error")
        }
        
        let result = try JSONDecoder().decode(WhisperResponse.self, from: data)
        return result.text
    }
    
    func cancelRecognition() async {
        audioData = Data()
    }
}

private struct WhisperResponse: Codable {
    let text: String
}
```

### Step 3: Register the Provider

In `Type4Me/ASR/ASRProviderRegistry.swift`, add to the `all` array:

```swift
struct ASRProviderRegistry {
    static let all: [any ASRProviderConfig.Type] = [
        SherpaParaformerProvider.self,
        VolcengineProvider.self,
        DeepgramProvider.self,
        OpenAIWhisperProvider.self,   // ← Add your provider here
    ]
}
```

## Credentials Storage

Credentials are stored at `~/Library/Application Support/Type4Me/credentials.json` with permissions `0600`. Never hardcode secrets — always load via `CredentialStore`:

```swift
// Reading credentials
let store = CredentialStore.shared
let apiKey = store.get(providerID: "openai_whisper", key: "api_key")

// Writing credentials  
store.set(providerID: "openai_whisper", key: "api_key", value: userInputKey)

// Checking if configured
let isConfigured = store.isConfigured(providerID: "openai_whisper", 
                                       fields: OpenAIWhisperProvider.credentialFields)
```

## Custom Processing Modes with Prompt Variables

Processing modes use LLM post-processing with three context variables:

| Variable | Value |
|---|---|
| `{text}` | Recognized speech text |
| `{selected}` | Text selected in active app at record start |
| `{clipboard}` | Clipboard content at record start |

Example custom mode prompts:

```swift
// Translate selection using voice command
let translatePrompt = """
The user selected this text: {selected}
Voice command: {text}
Execute the command on the selected text. Output only the result.
"""

// Code review via voice
let codeReviewPrompt = """
Code to review:
{clipboard}

Review instruction: {text}

Provide focused feedback addressing the instruction.
"""

// Email reply drafting
let emailPrompt = """
Original email: {selected}
My reply intent (spoken): {text}
Write a professional email reply. Output only the email body.
"""
```

## Built-in Processing Modes

```swift
enum ProcessingMode {
    case fast           // Direct ASR output, zero latency
    case performance    // Dual-channel: streaming + offline refinement
    case englishTranslation  // Chinese speech → English text
    case promptOptimize // Raw prompt → optimized prompt via LLM
    case command        // Voice command + selected/clipboard context → LLM action
    case custom(prompt: String)  // User-defined prompt template
}
```

## Session State Machine

The core recording flow in `Session/`:

```
[Idle]
  → hotkey pressed → [Recording] → audio streams to ASR client
  → hotkey released/pressed again → [Processing]
  → ASR returns text → [LLM Post-processing] (if mode requires)
  → [Injecting] → text injected into active app
  → [Idle]
```

## Updating After Source Changes

```bash
cd type4me
git pull
bash scripts/deploy.sh
# SherpaOnnx does NOT need recompiling unless engine version changed
```

## Troubleshooting

### App won't open (security warning)
```bash
xattr -d com.apple.quarantine /Applications/Type4Me.app
```

### Local model not recognized in Settings
Verify the directory structure exactly matches:
```bash
ls ~/Library/Application\ Support/Type4Me/Models/sherpa-onnx-streaming-paraformer-bilingual-zh-en/
# Must show: encoder.int8.onnx  decoder.int8.onnx  tokens.txt
```

### SherpaOnnx build fails
```bash
# Ensure cmake is installed
brew install cmake
# Clean and retry
rm -rf Frameworks/
bash scripts/build-sherpa.sh
```

### New ASR provider not appearing in Settings
- Confirm the provider type is added to `ASRProviderRegistry.all`
- Ensure `providerID` is unique across all providers
- Clean build: `swift package clean && bash scripts/deploy.sh`

### Audio not captured / no floating bar
- Grant microphone permission: System Settings → Privacy & Security → Microphone → Type4Me ✓
- Grant Accessibility permission for text injection: System Settings → Privacy & Security → Accessibility → Type4Me ✓

### Credentials not saving
```bash
# Check file exists and has correct permissions
ls -la ~/Library/Application\ Support/Type4Me/credentials.json
# Should show: -rw------- (0600)
# Fix permissions if needed:
chmod 0600 ~/Library/Application\ Support/Type4Me/credentials.json
```

### Export history to CSV
Open Settings → History → select date range → Export CSV. The SQLite database is at:
```bash
~/Library/Application\ Support/Type4Me/history.db
# Direct query:
sqlite3 ~/Library/Application\ Support/Type4Me/history.db \
  "SELECT datetime(timestamp,'unixepoch'), text FROM records ORDER BY timestamp DESC LIMIT 20;"
```

## System Requirements

- macOS 14.0 (Sonoma) or later
- Apple Silicon (M1/M2/M3/M4) recommended for local ASR inference
- Xcode Command Line Tools + CMake for source builds
- Internet connection only needed for cloud ASR providers
