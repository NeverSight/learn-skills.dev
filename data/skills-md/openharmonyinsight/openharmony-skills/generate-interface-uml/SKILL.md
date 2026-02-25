---
name: generate-interface-uml
description: This skill should be used when user asks to "generate UML", "create sequence diagram", "生成时序图", "生成类图", "generate PlantUML", or discusses generating UML diagrams for new interfaces or API design.
version: 1.0.0
---

# Interface UML Generator

This skill helps generate PlantUML sequence diagrams and class diagrams for new interfaces, based on existing similar interfaces in the codebase.

## When to Use

User wants to create UML diagrams (sequence diagrams, class diagrams) for:
- New API interfaces
- New method implementations
- Interface call chains
- IPC communication flows

## Workflow

### Step 1: Gather Basic Information

Start with what the user provides (often just an interface name), then ask questions to collect:

**Essential Information:**
1. **Interface name(s)** - e.g., `AddGlocalBlackList`, `RemoveGlocalBlackList`
2. **Parameters** - What are the input parameters and their types?
3. **Return type** - What does the interface return?
4. **Reference interface** - Is there an existing similar interface to use as a template?

**Optional Information (ask if needed):**
5. **Output directory** - Where should the PlantUML files be saved?
6. **Diagram types** - Sequence diagram? Class diagram? Both?
7. **Call chain destination** - Which class/method does it ultimately call?

### Step 2: Analyze Reference Interface

Search the codebase for the reference interface to understand the call chain:

```bash
# Find the reference interface implementation
grep -r "SetFocusAppInfo" --include="*.h" --include="*.cpp"
```

**Key files to examine:**
- Client-side interfaces: `RSInterfaces`, `RSRenderInterface`
- IPC layer: `RSIClientToRenderConnection`, `RSClientToRenderConnection`
- Service-side: `RSRenderPipelineAgent`, `RSMainThread`
- Target class: Where the interface ultimately executes

### Step 3: Generate PlantUML Diagrams

#### Sequence Diagram Template

```plantuml
@startuml InterfaceName序列图
title InterfaceName 接口调用时序图

autonumber
skinparam maxMessageSize 150
skinparam boxPadding 10

actor "客户端应用" as Client
box "客户端进程 (Client Process)" #LightBlue
    participant "RSInterfaces" as RSInterfaces
    participant "RSRenderInterface" as RSRenderInterface
    participant "RSRenderPipelineClient\n(IPC Proxy)" as IPCProxy
end box

box "跨进程通信 (IPC)" #LightYellow
    participant "Binder/Hipc\n通信通道" as Binder
end box

box "服务端进程 (Render Service)" #LightGreen
    participant "RSClientToRenderConnection\n(IPC Stub)" as IPCStub
    participant "RSRenderPipelineAgent" as Agent
    participant "RSMainThread" as MainThread
    participant "TargetClass\n(在RSMainThread线程中执行)" as Target
end box

== 客户端调用流程 ==

Client -> RSInterfaces: InterfaceName(params)
activate RSInterfaces

RSInterfaces -> RSRenderInterface: InterfaceName(params)
activate RSRenderInterface

RSRenderInterface -> IPCProxy: InterfaceName(params)
activate IPCProxy

== 跨进程IPC调用 ==

IPCProxy -> Binder: IPC调用\nInterfaceName
activate Binder

Binder -> IPCStub: 接收IPC调用\nInterfaceName
activate IPCStub

== 服务端处理流程 ==

IPCStub -> Agent: InterfaceName(params)
activate Agent

Agent -> Agent: ScheduleMainThreadTask(\nlambda任务)

Agent -> MainThread: PostTask(\n执行InterfaceName)
activate MainThread

MainThread -> Target: TargetMethod(params)
activate Target

note right of Target
    描述具体操作
end note

Target --> MainThread: 返回
deactivate Target

MainThread --> Agent: 任务完成
deactivate MainThread

Agent --> IPCStub: 返回结果\n(ERR_OK)
deactivate Agent

IPCStub --> Binder: 返回IPC结果
deactivate IPCStub

Binder --> IPCProxy: 返回IPC结果
deactivate Binder

IPCProxy --> RSRenderInterface: 返回结果
deactivate IPCProxy

RSRenderInterface --> RSInterfaces: 返回结果
deactivate RSRenderInterface

RSInterfaces --> Client: 返回结果
deactivate RSInterfaces

@enduml
```

#### Class Diagram Template

```plantuml
@startuml InterfaceName类图
title InterfaceName系列接口涉及的类关系图

skinparam classAttributeIconSize 0
skinparam class {
    BackgroundColor<<client>> LightBlue
    BackgroundColor<<service>> LightGreen
    BackgroundColor<<static>> LightYellow
    BorderColor Black
}

package "客户端 (Client)" <<client>> {
    class RSInterfaces {
        + {static} GetInstance(): RSInterfaces&
        + InterfaceName(params): ReturnType
        --
        - renderInterface_: RSRenderInterface*
    }

    class RSRenderInterface {
        + InterfaceName(params): ReturnType
        --
        - renderPipelineClient_: RSRenderPipelineClient*
    }

    RSInterfaces --> RSRenderInterface
}

package "IPC通信层" {
    interface RSIClientToRenderConnection {
        + InterfaceName(params, ErrorCode&): ErrCode
    }

    class RSClientToRenderConnection {
        + InterfaceName(params, ErrorCode&): ErrCode
        --
        - renderPipelineAgent_: sptr<RSRenderPipelineAgent>
    }

    RSClientToRenderConnection ..|> RSIClientToRenderConnection
}

package "服务端 (Render Service)" <<service>> {
    class RSRenderPipelineAgent {
        + InterfaceName(params, ErrorCode&): ErrCode
        --
        - rsRenderPipeline_: std::shared_ptr<RSRenderPipeline>
    }

    class RSMainThread {
        + PostTask(RSTask): void
        + ScheduleTask(Task): std::future<Return>
        --
        - mainThreadId_: std::thread::id
    }
}

package "TargetClass (静态类)" <<static>> {
    class TargetClass {
        + {static} TargetMethod(params): void
        --
        - {static} member_: Type
    }
}

RSRenderInterface --> RSIClientToRenderConnection: 通过IPC调用
RSClientToRenderConnection --> RSRenderPipelineAgent
RSRenderPipelineAgent ..> RSMainThread: ScheduleMainThreadTask
RSRenderPipelineAgent ..> TargetClass: 调用静态方法

@enduml
```

### Step 4: Save PlantUML Files

Write the generated PlantUML files to the specified directory:
- Use descriptive filenames: `InterfaceName_sequence.puml`, `InterfaceName_ClassDiagram.puml`
- Include UTF-8 BOM for Chinese character support if needed
- Save to user-specified output directory

### Step 5: Optional - Create Comparison Diagram

If comparing with existing interfaces, create a comparison diagram showing:
- Parameter differences
- Call chain differences
- Target class differences

## Questions to Ask User

1. **Interface names**: What are the interface names you want to generate UML for?
2. **Reference interface**: Which existing interface should be used as a reference?
3. **Parameters**: What are the parameter types for the new interface(s)?
4. **Return type**: What should the interface return?
5. **Target class**: Which class does the interface ultimately call? (e.g., ScreenSpecialLayerInfo, RSMainThread)
6. **Thread requirement**: Does it need to execute in a specific thread? (e.g., RSMainThread thread)
7. **Output directory**: Where should the PlantUML files be saved?

## Example Usage

**User provides:**
```
Generate UML for AddGlocalBlackList, RemoveGlocalBlackList, SetGlocalBlackList
```

**Ask follow-up questions:**
1. "What should be the parameter type?" → `const std::vector<NodeId>&`
2. "Which existing interface is similar?" → `SetFocusAppInfo`
3. "Which class does it ultimately call?" → `ScreenSpecialLayerInfo`
4. "What's the output directory?" → Current code directory

**Generate output:**
- `AddGlocalBlackList_sequence.puml`
- `RemoveGlocalBlackList_sequence.puml`
- `SetGlocalBlackList_sequence.puml`
- `InterfaceName_ClassDiagram.puml`

## Tips

- Use Chinese for diagram titles and notes if the codebase uses Chinese
- Include `autonumber` for sequence diagrams
- Use color coding to distinguish client/service/static layers
- Add notes to explain key operations
- Group related steps with `== Section Name ==`
