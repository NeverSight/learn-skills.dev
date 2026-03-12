---
name: multi-canister
description: "Design and deploy multi-canister dapps. Covers inter-canister calls, canister factory pattern, async messaging pitfalls, bounded vs unbounded wait, and 2MB payload limits. Use when splitting an app across canisters, making inter-canister or cross-canister calls, or designing canister-to-canister communication. Do NOT use for single-canister apps."
license: Apache-2.0
compatibility: "icp-cli >= 0.1.0"
metadata:
  title: Multi-Canister Architecture
  category: Architecture
---

# Multi-Canister Architecture

## What This Is

Splitting an IC application across multiple canisters for scaling, separation of concerns, or independent upgrade cycles. Each canister has its own state, cycle balance, and upgrade path. Canisters communicate via async inter-canister calls.

## Prerequisites

- For Motoko: `mops` package manager, `core = "2.0.0"` in mops.toml
- For Rust: `ic-cdk >= 0.19`, `candid`, `serde`, `ic-stable-structures`

## How It Works

A caller canister makes a call to a callee canister: the method name, arguments (payload) and attached cycles are packed into a canister request message, which is delivered to the callee after the caller blocks on `await`; the callee executes the request and produces a response; this is packed into a canister response message and delivered to the caller; the caller awakes fron the `await` and continues execution (executes the canister response message). The system may produce a reject response message if e.g. the callee is not found or some resource limit was reached.

Calls may be unbounded wait (caller MUST wait until the callee produces a response) or bounded wait (caller MAY get a `SYS_UNKNOWN` response instead of the actual response after the call timeout expires or if the subnet runs low on resources). Request delivery is best-effort: the system may decide to reject any request instead of delivering it. Unbounded wait response (including reject response) delivery is guaranteed: the caller will always learn the outcome of the call. Bounded wait response delivery is best-effort: the caller may receive a system-generated `SYS_UNKNOWN` reject response (unknown outcome) instead of the actual response if the call timed out or some system resource was exhausted, whether or not the request was delivered to the callee.

## When to Use Multi-Canister

| Reason | Threshold |
|---|---|
| Storage limits | Each canister: up to hundreds of GB stable memory + 4GB heap. If your data could exceed heap limits or benefit from partitioning, split storage across canisters. |
| Scalable compute | Canisters are single-threaded actors. Sharding load across multiple canisters, potentially across multiple subnets, can significantly improve throughput. |
| Separation of concerns | Auth service, content service, payment service as independent units. |
| Independent upgrades | Upgrade the payments canister without touching the user canister. |
| Access control | Different controllers for different canisters (e.g., DAO controls one, team controls another). |

**When NOT to use:** Simple apps with <1GB data. Single-canister is simpler, faster, and avoids inter-canister call overhead. Do not over-architect.

## Issues that May Cause Functional Bugs

For building a multi-canister application, take the perspective of an experienced senior software engineer and carefully read the following issues that may cause subtle functional bugs. Meticulously avoid bugs that could be caused by these issues. 

1. **Request and response payloads are limited to 2 MB.** Because any canister call may be required to cross subnet boundaries; and cross-subnet (or XNet) messages (the request and response corresponding to each canister call) are inducted in (packaged into) 4 MB blocks; canister request and response payloads are limited to 2 MB. A call with a request payload above 2 MB will fail synchronously; and a response with a payload above 2 MB will trap. Chunk larger payloads into 1 MB chunks (to allow for any encoding overhead) and deliver them over multiple calls (e.g. chunked uploads or byte range queries).

2. **Update methods that make calls are NOT executed atomically.** When an update method makes a call, the code before the `await` is one atomic message execution (i.e. the ingress message or canister request that invoked the update method); and the code after the `await` is a separate atomic message execution (the response to the call). In particular, if the update method traps after the `await`, any mutations before the `await` have already been persisted; and any mutations after the `await` will be rolled back. Design for eventual consistency or use a saga pattern. If more context on this is needed, you can optionally refer to [properties of message executions on ICP](https://docs.internetcomputer.org/references/message-execution-properties). 

3. **Use idempotent APIs. Or provide a separate endpoint to query the outcome of a non-idempotent call.** If a call to a non-idempotent API times out, there must be another way for the caller to learn the outcome of the call (e.g. by attaching a unique ID to the original call and querying for the outcome of the call with that unique ID). Without a way to learn the outcome, when the caller receives a `SYS_UNKNOWN` response it may be unable to decide whether to continue, retry the call or abort.

4. **Calls across subnet boundaries are slower than calls on the same subnet.** Under light subnet load, a call to a canister on the same subnet may complete and its response may be processed by the caller within a single round. The call latency only depends on how frequently the caller and callee are scheduled (which may be multiple times per round). A cross canister call requires 2-3 rounds either way (request delivery and response delivery), plus scheduler latency.

5. **Calls across subnet boundaries have relatively low bandwidth.** Cross-subnet (or XNet) messages are inducted in (packaged into) 4 MB blocks once per round, along with any ingress messages and other XNet messages. Expect multiple MBs of messages to take multiple rounds to deliver, on top of the XNet latency. (Subnet-local messages are routed within the subnet, so they don't suffer from this bandwidth limitation).

6. **Defensive practice: bind `msg_caller()` before `.await` in Rust.** The current ic-cdk executor preserves caller across `.await` points via protected tasks, but capturing it early guards against future executor changes. **Motoko is safe:** `public shared ({ caller }) func` captures `caller` as an immutable binding at function entry.

    ```rust
    // Recommended (Rust) — capture caller before await:
    #[update]
    async fn do_thing() {
        let original_caller = ic_cdk::api::msg_caller(); // Defensive: capture before await
        let _ = some_canister_call().await;
        let who = original_caller; // Safe
    }
    ```

7. **Not handling rejected calls.** Inter-canister calls can fail (callee trapped, out of cycles, canister stopped). In Motoko use `try/catch`. In Rust, handle the `Result` from `ic_cdk::call`. Unhandled rejections trap your canister.

8. **Canister factory without enough cycles.** Creating a canister requires cycles. The management canister charges for creation and the initial cycle balance. If you do not attach enough cycles, creation fails.

9. **Not setting up `#[init]` and `#[post_upgrade]` in Rust.** Without a `post_upgrade` handler, canister upgrades may behave unexpectedly. Always define both.

## Issues that May Cause Security Bugs

Take the perspective of an experienced senior security engineer and carefully read the following issues that may cause risky security issues. Meticulously avoid such security bugs.

1. **Avoid reentrancy issues.** The fact that calls are not atomic can cause reentrancy bugs such as double-spending vulnerabilities, see also "Update methods that make calls are NOT executed atomically" above. Avoid such issues, e.g. by employing locking patterns. If more context is needed, you can optionally refer to the [security best practices](https://docs.internetcomputer.org/building-apps/security/inter-canister-calls#be-aware-that-there-is-no-reliable-message-ordering) or the [paper](https://arxiv.org/pdf/2506.05932).  

2. **Securely handle traps in callbacks.** A trap (a panic in Rust) in a callback causes the callback to not apply any state changes. For example, if a trap can be caused by a malicious entity, it could mean that security critical actions like debiting an account in a DeFi context can be skipped, leading to critical issues like double-spending. To avoid this, avoid traps in callbacks that could cause such bugs, consider using `call_on_cleanup`, and use "journaling". If more context is needed, optionally consider this [security best practice](https://docs.internetcomputer.org/building-apps/security/inter-canister-calls#securely-handle-traps-in-callbacks). 

3. **Unbounded wait calls may prevent canister upgrades, indefinitely.** Unbounded wait calls may take arbitrarily long to complete: a malicious or incorrect callee may spin indefinitely without producing a response. Canisters cannot be stopped while awaiting responses to outstanding calls. Bounded wait calls avoid this issue by making sure that calls complete in a bounded time, independent of whether the callee responded or not. If more context is needed, optionally consider [this security best practice](https://docs.internetcomputer.org/building-apps/security/inter-canister-calls#be-aware-of-the-risks-involved-in-calling-untrustworthy-canisters). 

4. **`canister_inspect_message` is not called for inter-canister calls.** It only runs for ingress messages (from external users). Do not rely on it for access control between canisters. Use explicit principal checks instead. If more context is needed, optionally consider [this security best practice](https://docs.internetcomputer.org/building-apps/security/iam#do-not-rely-on-ingress-message-inspection). 

## Mistakes That Break Your Build

1. **Deploying canisters in the wrong order.** Canisters with dependencies must be deployed according to their dependencies. Declare `dependencies` in icp.yaml so `icp deploy` orders them correctly.

2. **Forgetting to generate type declarations for each backend canister.** Use language-specific tooling (e.g., `didc` for Candid bindings) to generate declarations for each backend canister individually.

3. **Shared types diverging between canisters.** If canister A expects `{ id: Nat; name: Text }` and canister B sends `{ id: Nat; title: Text }`, the call silently fails or traps. Use a shared types module imported by both canisters.

## Implementation

### Project Structure

```
my-project/
  icp.yaml
  mops.toml
  src/
    shared/
      Types.mo          # Shared type definitions
    user_service/
      main.mo           # User canister
    content_service/
      main.mo           # Content canister
    frontend/
      ...               # Frontend assets
```

### icp.yaml

```yaml
canisters:
  - name: user_service
    recipe:
      type: "@dfinity/motoko@v4.1.0"
      configuration:
        main: src/user_service/main.mo
  - name: content_service
    recipe:
      type: "@dfinity/motoko@v4.1.0"
      configuration:
        main: src/content_service/main.mo
```

### Motoko

#### src/shared/Types.mo — Shared Types

```motoko
module {
  public type UserId = Principal;
  public type PostId = Nat;

  public type UserProfile = {
    id : UserId;
    username : Text;
    created : Int;
  };

  public type Post = {
    id : PostId;
    author : UserId;
    title : Text;
    body : Text;
    created : Int;
  };

  public type ServiceError = {
    #NotFound;
    #Unauthorized;
    #AlreadyExists;
    #InternalError : Text;
  };
};
```

#### src/user_service/main.mo — User Canister

```motoko
import Map "mo:core/Map";
import Principal "mo:core/Principal";
import Array "mo:core/Array";
import Time "mo:core/Time";
import Result "mo:core/Result";
import Runtime "mo:core/Runtime";
import Types "../shared/Types";

persistent actor {

  type UserProfile = Types.UserProfile;

  let users = Map.empty<Principal, UserProfile>();

  // Register a new user
  public shared ({ caller }) func register(username : Text) : async Result.Result<UserProfile, Types.ServiceError> {
    if (Principal.isAnonymous(caller)) {
      return #err(#Unauthorized);
    };
    switch (Map.get(users, Principal.compare, caller)) {
      case (?_existing) { #err(#AlreadyExists) };
      case null {
        let profile : UserProfile = {
          id = caller;
          username;
          created = Time.now();
        };
        Map.add(users, Principal.compare, caller, profile);
        #ok(profile)
      };
    }
  };

  // Check if a user exists (called by other canisters)
  public shared query func isValidUser(userId : Principal) : async Bool {
    switch (Map.get(users, Principal.compare, userId)) {
      case (?_) { true };
      case null { false };
    }
  };

  // Get user profile
  public shared query func getUser(userId : Principal) : async ?UserProfile {
    Map.get(users, Principal.compare, userId)
  };

  // Get all users
  public query func getUsers() : async [UserProfile] {
    Array.fromIter<UserProfile>(Map.values(users))
  };
};
```

#### src/content_service/main.mo — Content Canister (calls User Service)

```motoko
import Map "mo:core/Map";
import Nat "mo:core/Nat";
import Array "mo:core/Array";
import Time "mo:core/Time";
import Result "mo:core/Result";
import Runtime "mo:core/Runtime";
import Error "mo:core/Error";
import Principal "mo:core/Principal";
import Types "../shared/Types";

// Import the other canister — name must match icp.yaml canister key
import UserService "canister:user_service";

persistent actor {

  type Post = Types.Post;

  let posts = Map.empty<Nat, Post>();
  var postCounter : Nat = 0;

  // Create a post — validates user via inter-canister call
  public shared ({ caller }) func createPost(title : Text, body : Text) : async Result.Result<Post, Types.ServiceError> {
    let originalCaller = caller;

    if (Principal.isAnonymous(originalCaller)) {
      return #err(#Unauthorized);
    };

    // Inter-canister call to user_service
    let isValid = try {
      await UserService.isValidUser(originalCaller)
    } catch (e : Error.Error) {
      Runtime.trap("User service unavailable: " # Error.message(e));
    };

    if (not isValid) {
      return #err(#Unauthorized);
    };

    let id = postCounter;
    let post : Post = {
      id;
      author = originalCaller; 
      title;
      body;
      created = Time.now();
    };
    Map.add(posts, Nat.compare, id, post);
    postCounter += 1;
    #ok(post)
  };

  // Get all posts
  public query func getPosts() : async [Post] {
    Array.fromIter<Post>(Map.values(posts))
  };

  // Get posts by author — with enriched user data
  public func getPostsWithAuthor(authorId : Principal) : async {
    user : ?Types.UserProfile;
    posts : [Post];
  } {
    let userProfile = try {
      await UserService.getUser(authorId)
    } catch (_e : Error.Error) { null };

    let authorPosts = Array.filter<Post>(
      Array.fromIter<Post>(Map.values(posts)),
      func(p : Post) : Bool { p.author == authorId }
    );

    { user = userProfile; posts = authorPosts }
  };

  // Delete a post — only the author can delete
  public shared ({ caller }) func deletePost(id : Nat) : async Result.Result<(), Types.ServiceError> {
    let originalCaller = caller;

    switch (Map.get(posts, Nat.compare, id)) {
      case (?post) {
        if (post.author != originalCaller) {
          return #err(#Unauthorized);
        };
        ignore Map.delete(posts, Nat.compare, id);
        #ok(())
      };
      case null { #err(#NotFound) };
    }
  };
};
```

#### Production Readiness: Content Service

The content service examples above are intentionally kept simple to demonstrate multi-canister communication patterns. They lack several things that would be needed for production use:

- **Input validation.** The `username` parameter in `register` accepts any string — including empty strings or strings up to the 2MB message size limit. Validate length (e.g., 1–64 characters), enforce allowed character sets, and add a uniqueness constraint via a reverse lookup map to prevent impersonation.
- **User enumeration and pagination on `getUsers`.** Using `getUsers`, it's possible for everyone to enumerate all users on the platform, which may not be desirable. Furthermore, the `getUsers` endpoint returns all user profiles in a single response. As the user base grows, this will hit the 2MB response size limit and trap, bricking the endpoint. Add pagination (offset/limit parameters). The same applies to `getPosts`.

### Rust

#### Project Structure (Rust)

```
my-project/
  icp.yaml
  Cargo.toml          # workspace
  src/
    user_service/
      Cargo.toml
      src/lib.rs
    content_service/
      Cargo.toml
      src/lib.rs
```

#### Cargo.toml (workspace root)

```toml
[workspace]
members = [
  "src/user_service",
  "src/content_service",
]
```

#### icp.yaml (Rust)

```yaml
canisters:
  - name: user_service
    recipe:
      type: "@dfinity/rust@v3.2.0"
      configuration:
        package: user_service
        candid: src/user_service/user_service.did
  - name: content_service
    recipe:
      type: "@dfinity/rust@v3.2.0"
      configuration:
        package: content_service
        candid: src/content_service/content_service.did
```

#### src/user_service/Cargo.toml

```toml
[package]
name = "user_service"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
ic-cdk = "0.19"
candid = "0.10"
serde = { version = "1", features = ["derive"] }
ic-stable-structures = "0.7"
```

#### src/user_service/src/lib.rs

```rust
use candid::{CandidType, Deserialize, Principal};
use ic_cdk::{init, post_upgrade, query, update};
use ic_stable_structures::memory_manager::{MemoryId, MemoryManager, VirtualMemory};
use ic_stable_structures::{DefaultMemoryImpl, StableBTreeMap};
use std::cell::RefCell;

type Memory = VirtualMemory<DefaultMemoryImpl>;

#[derive(CandidType, Deserialize, Clone, Debug)]
struct UserProfile {
    id: Principal,
    username: String,
    created: i64,
}

// Stable storage
thread_local! {
    static MEMORY_MANAGER: RefCell<MemoryManager<DefaultMemoryImpl>> =
        RefCell::new(MemoryManager::init(DefaultMemoryImpl::default()));

    static USERS: RefCell<StableBTreeMap<Vec<u8>, Vec<u8>, Memory>> = RefCell::new(
        StableBTreeMap::init(
            MEMORY_MANAGER.with(|m| m.borrow().get(MemoryId::new(0)))
        )
    );
}

fn principal_to_key(p: &Principal) -> Vec<u8> {
    p.as_slice().to_vec()
}

fn serialize_profile(profile: &UserProfile) -> Vec<u8> {
    candid::encode_one(profile).unwrap()
}

fn deserialize_profile(bytes: &[u8]) -> UserProfile {
    candid::decode_one(bytes).unwrap()
}

#[init]
fn init() {}

#[post_upgrade]
fn post_upgrade() {}

#[update]
fn register(username: String) -> Result<UserProfile, String> {
    let caller = ic_cdk::api::msg_caller();
    if caller == Principal::anonymous() {
        return Err("Unauthorized".to_string());
    }

    let key = principal_to_key(&caller);
    USERS.with(|users| {
        if users.borrow().contains_key(&key) {
            return Err("Already exists".to_string());
        }

        let profile = UserProfile {
            id: caller,
            username,
            created: ic_cdk::api::time() as i64,
        };
        let bytes = serialize_profile(&profile);
        users.borrow_mut().insert(key, bytes);
        Ok(profile)
    })
}

#[query]
fn is_valid_user(user_id: Principal) -> bool {
    let key = principal_to_key(&user_id);
    USERS.with(|users| users.borrow().contains_key(&key))
}

#[query]
fn get_user(user_id: Principal) -> Option<UserProfile> {
    let key = principal_to_key(&user_id);
    USERS.with(|users| {
        users.borrow().get(&key).map(|bytes| deserialize_profile(&bytes))
    })
}

ic_cdk::export_candid!();
```

#### src/content_service/Cargo.toml

```toml
[package]
name = "content_service"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
ic-cdk = "0.19"
candid = "0.10"
serde = { version = "1", features = ["derive"] }
ic-stable-structures = "0.7"
```

#### src/content_service/src/lib.rs

```rust
use candid::{CandidType, Deserialize, Principal};
use ic_cdk::call::Call;
use ic_cdk::{init, post_upgrade, query, update};
use ic_stable_structures::memory_manager::{MemoryId, MemoryManager, VirtualMemory};
use ic_stable_structures::{DefaultMemoryImpl, StableBTreeMap, StableCell};
use std::cell::RefCell;

type Memory = VirtualMemory<DefaultMemoryImpl>;

#[derive(CandidType, Deserialize, Clone, Debug)]
struct Post {
    id: u64,
    author: Principal,
    title: String,
    body: String,
    created: i64,
}

#[derive(CandidType, Deserialize, Clone, Debug)]
struct UserProfile {
    id: Principal,
    username: String,
    created: i64,
}

// Stable storage -- survives canister upgrades
thread_local! {
    static MEMORY_MANAGER: RefCell<MemoryManager<DefaultMemoryImpl>> =
        RefCell::new(MemoryManager::init(DefaultMemoryImpl::default()));

    // Posts keyed by id (u64 as big-endian bytes) -> candid-encoded Post
    static POSTS: RefCell<StableBTreeMap<Vec<u8>, Vec<u8>, Memory>> = RefCell::new(
        StableBTreeMap::init(
            MEMORY_MANAGER.with(|m| m.borrow().get(MemoryId::new(0)))
        )
    );

    // Post counter in stable memory
    static POST_COUNTER: RefCell<StableCell<u64, Memory>> = RefCell::new(
        StableCell::init(
            MEMORY_MANAGER.with(|m| m.borrow().get(MemoryId::new(1))),
            0u64,
        )
    );

    // Store the user_service canister ID (set during init, re-set on upgrade)
    static USER_SERVICE_ID: RefCell<Option<Principal>> = RefCell::new(None);
}

fn post_id_to_key(id: u64) -> Vec<u8> {
    id.to_be_bytes().to_vec()
}

fn serialize_post(post: &Post) -> Vec<u8> {
    candid::encode_one(post).unwrap()
}

fn deserialize_post(bytes: &[u8]) -> Post {
    candid::decode_one(bytes).unwrap()
}

#[init]
fn init(user_service_id: Principal) {
    USER_SERVICE_ID.with(|id| *id.borrow_mut() = Some(user_service_id));
}

#[post_upgrade]
fn post_upgrade(user_service_id: Principal) {
    // Re-set the user_service ID (not stored in stable memory for simplicity,
    // since it is always passed as an init/upgrade argument)
    init(user_service_id);
}

fn get_user_service_id() -> Principal {
    USER_SERVICE_ID.with(|id| {
        id.borrow().expect("user_service canister ID not set")
    })
}

// Defensive: capture caller before any await
#[update]
async fn create_post(title: String, body: String) -> Result<Post, String> {
    // Capture caller before the await as defensive practice
    let original_caller = ic_cdk::api::msg_caller();

    if original_caller == Principal::anonymous() {
        return Err("Unauthorized".to_string());
    }

    // Inter-canister call to user_service
    let user_service = get_user_service_id();
    let (is_valid,): (bool,) = Call::unbounded_wait(user_service, "is_valid_user")
        .with_arg(original_caller)
        .await
        .map_err(|e| format!("User service call failed: {:?}", e))?
        .candid_tuple()
        .map_err(|e| format!("Failed to decode response: {:?}", e))?;

    if !is_valid {
        return Err("User not registered".to_string());
    }

    let id = POST_COUNTER.with(|counter| {
        let mut counter = counter.borrow_mut();
        let id = *counter.get();
        counter.set(id + 1);
        id
    });

    let post = Post {
        id,
        author: original_caller, // Use captured caller
        title,
        body,
        created: ic_cdk::api::time() as i64,
    };

    POSTS.with(|posts| {
        posts.borrow_mut().insert(post_id_to_key(id), serialize_post(&post));
    });

    Ok(post)
}

#[query]
fn get_posts() -> Vec<Post> {
    POSTS.with(|posts| {
        posts.borrow().iter()
            .map(|entry| deserialize_post(&entry.value()))
            .collect()
    })
}

// Cross-canister enrichment: get posts with author profile
#[update]
async fn get_posts_with_author(author_id: Principal) -> (Option<UserProfile>, Vec<Post>) {
    let user_service = get_user_service_id();

    // Call user_service for profile data
    let user_profile: Option<UserProfile> =
        match Call::unbounded_wait(user_service, "get_user")
            .with_arg(author_id)
            .await
        {
            Ok(response) => response.candid_tuple::<(Option<UserProfile>,)>()
                .map(|(profile,)| profile)
                .unwrap_or(None),
            Err(_) => None, // Handle gracefully if user service is down
        };

    let author_posts = POSTS.with(|posts| {
        posts.borrow().iter()
            .map(|entry| deserialize_post(&entry.value()))
            .filter(|p| p.author == author_id)
            .collect()
    });

    (user_profile, author_posts)
}

#[update]
async fn delete_post(id: u64) -> Result<(), String> {
    let original_caller = ic_cdk::api::msg_caller();

    POSTS.with(|posts| {
        let mut posts = posts.borrow_mut();
        let key = post_id_to_key(id);
        match posts.get(&key) {
            Some(bytes) => {
                let post = deserialize_post(&bytes);
                if post.author != original_caller {
                    return Err("Unauthorized".to_string());
                }
                posts.remove(&key);
                Ok(())
            }
            None => Err("Not found".to_string()),
        }
    })
}

ic_cdk::export_candid!();
```

### Canister Factory Pattern

A canister that creates other canisters dynamically. Useful for per-user canisters, sharding, or dynamic scaling.

#### Motoko Factory

```motoko
import Principal "mo:core/Principal";
import Map "mo:core/Map";
import Array "mo:core/Array";
import Runtime "mo:core/Runtime";

persistent actor Self {

  type CanisterSettings = {
    controllers : ?[Principal];
    compute_allocation : ?Nat;
    memory_allocation : ?Nat;
    freezing_threshold : ?Nat;
  };

  type CreateCanisterResult = {
    canister_id : Principal;
  };

  // IC Management canister
  transient let ic : actor {
    create_canister : shared ({ settings : ?CanisterSettings }) -> async CreateCanisterResult;
    install_code : shared ({
      mode : { #install; #reinstall; #upgrade };
      canister_id : Principal;
      wasm_module : Blob;
      arg : Blob;
    }) -> async ();
    deposit_cycles : shared ({ canister_id : Principal }) -> async ();
  } = actor "aaaaa-aa";

  // Track created canisters
  let childCanisters = Map.empty<Principal, Principal>(); // owner -> canister

  // Create a new canister for a user (one per caller)
  public shared ({ caller }) func createChildCanister(wasmModule : Blob) : async Principal {
    if (Principal.isAnonymous(caller)) { Runtime.trap("Auth required") };
    if (Map.get(childCanisters, Principal.compare, caller) != null) {
      Runtime.trap("Child canister already exists for this caller");
    };

    // Create canister with cycles
    let createResult = await (with cycles = 1_000_000_000_000)
      ic.create_canister({
        settings = ?{
          controllers = ?[Principal.fromActor(Self), caller];
          compute_allocation = null;
          memory_allocation = null;
          freezing_threshold = null;
        };
      });

    let canisterId = createResult.canister_id;

    // Install code
    await ic.install_code({
      mode = #install;
      canister_id = canisterId;
      wasm_module = wasmModule;
      arg = to_candid (caller); // Pass owner as init arg
    });

    Map.add(childCanisters, Principal.compare, caller, canisterId);
    canisterId
  };

  // Get a user's canister
  public query func getChildCanister(owner : Principal) : async ?Principal {
    Map.get(childCanisters, Principal.compare, owner)
  };
};
```

#### Rust Factory

```rust
use candid::{CandidType, Deserialize, Nat, Principal, encode_one};
use ic_cdk::management_canister::{
    create_canister_with_extra_cycles, install_code,
    CreateCanisterArgs, InstallCodeArgs, CanisterInstallMode, CanisterSettings,
};
use ic_cdk::update;
use ic_stable_structures::memory_manager::{MemoryId, MemoryManager, VirtualMemory};
use ic_stable_structures::{DefaultMemoryImpl, StableBTreeMap};
use std::cell::RefCell;

type Memory = VirtualMemory<DefaultMemoryImpl>;

thread_local! {
    static MEMORY_MANAGER: RefCell<MemoryManager<DefaultMemoryImpl>> =
        RefCell::new(MemoryManager::init(DefaultMemoryImpl::default()));

    // Stable storage: owner principal -> child canister principal (survives upgrades)
    static CHILD_CANISTERS: RefCell<StableBTreeMap<Vec<u8>, Vec<u8>, Memory>> = RefCell::new(
        StableBTreeMap::init(
            MEMORY_MANAGER.with(|m| m.borrow().get(MemoryId::new(0)))
        )
    );
}

#[update]
async fn create_child_canister(wasm_module: Vec<u8>) -> Principal {
    let caller = ic_cdk::api::msg_caller();
    assert_ne!(caller, Principal::anonymous(), "Auth required");

    // One child canister per caller
    let already_exists = CHILD_CANISTERS.with(|c| c.borrow().contains_key(&caller.as_slice().to_vec()));
    if already_exists {
        ic_cdk::trap("Child canister already exists for this caller");
    }

    // Create canister
    let create_args = CreateCanisterArgs {
        settings: Some(CanisterSettings {
            controllers: Some(vec![ic_cdk::api::canister_self(), caller]),
            compute_allocation: None,
            memory_allocation: None,
            freezing_threshold: None,
            reserved_cycles_limit: None,
            log_visibility: None,
            wasm_memory_limit: None,
            wasm_memory_threshold: None,
            environment_variables: None,
        }),
    };

    // Attach 1T cycles for the new canister
    let create_result = create_canister_with_extra_cycles(&create_args, 1_000_000_000_000u128)
        .await
        .expect("Failed to create canister");

    let canister_id = create_result.canister_id;

    // Install code
    let install_args = InstallCodeArgs {
        mode: CanisterInstallMode::Install,
        canister_id,
        wasm_module,
        arg: encode_one(&caller).unwrap(), // Pass owner as init arg
    };

    install_code(&install_args)
        .await
        .expect("Failed to install code");

    // Track the child canister
    CHILD_CANISTERS.with(|canisters| {
        canisters.borrow_mut().insert(
            caller.as_slice().to_vec(),
            canister_id.as_slice().to_vec(),
        );
    });

    canister_id
}

#[ic_cdk::query]
fn get_child_canister(owner: Principal) -> Option<Principal> {
    CHILD_CANISTERS.with(|canisters| {
        canisters.borrow().get(&owner.as_slice().to_vec())
            .map(|bytes| Principal::from_slice(&bytes))
    })
}
```

#### Production Readiness: Canister Factory

The factory examples above are intentionally kept simple to demonstrate the canister creation pattern. They lack several things that would be needed for production use:

- **Cycle-drain protection.** Any non-anonymous principal can call `createChildCanister` repeatedly, each call consuming 1T cycles from the factory. Add an allowlist of authorized callers, enforce a per-user creation limit, and check the factory's cycle balance before creating a canister (e.g., `ExperimentalCycles.balance()` in Motoko, `ic_cdk::api::canister_balance128()` in Rust).
- **WASM module validation.** The WASM module is caller-supplied, meaning any authenticated user can deploy arbitrary code. Do not accept WASM from arbitrary callers in production. Instead, hardcode a known WASM module (or its hash) in the factory canister, or verify the module hash against an allowlist before installing. Whitelist principals that are allowed to deploy through the factory to avoid unauthorized use. 
- **Reentrancy protection.** The factory performs two sequential awaits (`create_canister`, then `install_code`) with no locking. Concurrent calls from the same caller can create orphaned canisters that the factory loses track of. Add a lock (e.g., a `Set` of principals with in-flight calls) that prevents concurrent creation for the same caller.
- **Partial failure handling.** If `create_canister` succeeds but `install_code` fails, the canister exists and has cycles but is untracked by the factory. Track the canister ID immediately after creation (before attempting `install_code`) so the factory can retry installation or clean up on failure.

## Upgrade Strategy for Multi-Canister Systems

### Ordering

1. Deploy shared dependencies first (e.g., `user_service` before `content_service`).
2. Never change Candid interfaces in a breaking way. Add new fields as `opt` types.
3. Test upgrades locally before mainnet.

### Safe Upgrade Checklist

- Never remove or rename fields in existing types shared across canisters.
- Add new fields as optional (`?Type` in Motoko, `Option<T>` in Rust).
- If a canister's Candid interface changes, upgrade consumers after the provider.
- Always have both `#[init]` and `#[post_upgrade]` in Rust canisters.
- In Motoko, `persistent actor` handles stable storage automatically.

### Upgrade Commands

```bash
# Upgrade canisters in dependency order
icp deploy user_service

# Rust content_service requires the user_service principal on every upgrade (post_upgrade arg)
USER_SERVICE_ID=$(icp canister id user_service)
icp deploy content_service --argument "(principal \"$USER_SERVICE_ID\")"

npm run build
icp deploy frontend
```

## Deploy & Test

### Local Development

```bash
# Start the local replica
icp network start -d

# Deploy in dependency order
icp deploy user_service

# content_service (Rust) requires the user_service canister ID as an init argument
USER_SERVICE_ID=$(icp canister id user_service)
icp deploy content_service --argument "(principal \"$USER_SERVICE_ID\")"

# Build and deploy frontend
npm run build
icp deploy frontend
```

### Test Inter-Canister Calls (Motoko)

```bash
# Register a user
PRINCIPAL=$(icp identity principal)
icp canister call user_service register "(\"alice\")"

# Verify user exists
icp canister call user_service isValidUser "(principal \"$PRINCIPAL\")"
# Expected: (true)

# Create a post (triggers inter-canister call to user_service)
icp canister call content_service createPost "(\"Hello World\", \"My first post\")"
# Expected: (variant { ok = record { id = 0; author = principal "..."; ... } })

# Get all posts
icp canister call content_service getPosts
# Expected: (vec { record { id = 0; ... } })
```

### Test Inter-Canister Calls (Rust)

Rust canisters use snake_case function names:

```bash
PRINCIPAL=$(icp identity principal)
icp canister call user_service register "(\"alice\")"

icp canister call user_service is_valid_user "(principal \"$PRINCIPAL\")"
# Expected: (true)

# content_service must have been deployed with --argument "(principal \"<user_service_id>\")"
icp canister call content_service create_post "(\"Hello World\", \"My first post\")"
# Expected: (variant { ok = record { id = 0 : nat64; author = principal "..."; ... } })

icp canister call content_service get_posts
# Expected: (vec { record { id = 0 : nat64; ... } })
```

## Verify It Works

### Verify User Registration

```bash
icp canister call user_service register '("testuser")'
# Expected: (variant { ok = record { id = principal "..."; username = "testuser"; created = ... } })
```

### Verify Inter-Canister Call

```bash
# This call should succeed (user is registered)
# Motoko: createPost / Rust: create_post
icp canister call content_service createPost '("Test Title", "Test Body")'
# Expected: (variant { ok = record { ... } })

# Create a new identity that is NOT registered
icp identity new unregistered --storage plaintext
icp identity use unregistered
icp canister call content_service createPost '("Should Fail", "No user")'
# Expected: (variant { err = "User not registered" })

# Switch back
icp identity use default
```

### Verify Cross-Canister Query

```bash
PRINCIPAL=$(icp identity principal)
# Motoko: getPostsWithAuthor / Rust: get_posts_with_author
icp canister call content_service getPostsWithAuthor "(principal \"$PRINCIPAL\")"
# Expected: (opt record { id = ...; username = "testuser"; ... }, vec { record { ... } })
```

### Verify Canister Factory

```bash
# Read the wasm file for the child canister
# (In practice you'd upload or reference a wasm blob)
icp canister call factory createChildCanister '(blob "...")'
# Expected: (principal "NEW-CANISTER-ID")

icp canister call factory getChildCanister "(principal \"$PRINCIPAL\")"
# Expected: (opt principal "NEW-CANISTER-ID")
```
