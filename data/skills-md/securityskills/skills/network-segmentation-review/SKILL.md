---
name: network-segmentation-review
description: Review network segmentation designs and verify enforcement — VLANs, firewalls, cloud security groups, and zero-trust boundaries. Use when assessing internal network architecture.
---

# Network Segmentation Review

Verify that intended segmentation boundaries actually hold.

## 1. Understand the Intended Design

- Obtain the network diagram: zones (DMZ, internal, production, corporate, OT), trust levels, intended flows
- Map documented allowed flows vs "everything else should be denied"

## 2. Verify Layer 2/3 Boundaries

- VLAN hopping: double-tagging, DTP negotiation on user ports, native VLAN mismatches on trunks
- Inter-VLAN routing: which SVIs exist, ACLs between them
- Private VLANs / port isolation where host-to-host traffic is unnecessary

## 3. Firewall and Router Policy

- Rulebase review: any-any rules, overly broad source/destination (any→internal), rules by IP instead of objects
- Shadowed and unused rules; logging disabled on deny rules
- Management access: SSH/admin planes reachable from user segments?

## 4. Cloud Boundaries

- Security groups: per-role groups, no `0.0.0.0/0` ingress on non-web ports
- NACLs vs SGs layering; peering/transit gateway route tables leaking broader CIDRs
- Egress control: can compromised workload reach arbitrary internet (data exfil path)?

## 5. Active Validation (authorized testing)

- From representative hosts in each zone, attempt connections across boundaries: allowed (should work), denied (should fail and log)
- Test both directions and return traffic for stateful devices
- Use `nmap -PN -sT -p <port>` style targeted probes; record device logging the block

## Output

A verified flow matrix (source zone × destination zone × port × expected × observed), gaps with device-level evidence, and remediation per boundary.
