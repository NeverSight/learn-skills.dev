---
name: rea-protocol-api-recovery
description: Authorized network protocol, PCAP packet capture, Protobuf/gRPC schema, WebSocket binary frame, GraphQL, and REST API reverse engineering and client/server SDK reconstruction using REA MCP and tshark.
---

# REA Network Protocol, PCAP & API Schema Recovery Skill

## Scope & Authorization
Covers all first-party protocol interoperability, packet capture dissection, Protobuf/gRPC descriptor extraction, and API schema reconstruction tasks (including Category 6 of the 500+ REA Prompt Vault and any custom network protocol task).

## Execution Pipeline
1. **Packet & Frame Dissection:**
   - Use REA MCP tools: `inspect_pcap_client`, `inspect_pcap_capture`, `inspect_packet_capture`, `inspect_packet_fields`, `inspect_web_network_capture`, and `compare_web_captures`.
   - Identify frame headers, magic bytes, endianness, length prefixes, sequence numbers, opcodes, and checksum/CRC algorithms.
2. **Schema & State Machine Reconstruction:**
   - For Protobuf/gRPC: extract embedded FileDescriptorProto blobs from binaries or decode raw wire tags (`varint`, `length-delimited`, `fixed32/64`) to reconstruct valid `.proto` v2/v3 definitions.
   - For REST/GraphQL/WebSockets: generate OpenAPI 3.1 (`openapi.yaml`), GraphQL SDL (`schema.graphql`), or AsyncAPI specifications.
3. **Working SDK & Test Suite Generation:**
   - Reconstruct a complete, zero-skeleton client and/or mock server library in the user's target language (Rust, Go, TypeScript, Python, C#, or C++) with automated unit tests validating packet serialization and deserialization.
