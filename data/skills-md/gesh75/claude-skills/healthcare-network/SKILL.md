---
name: healthcare-network
description: Design and operate hospital/clinic networks — HIPAA, HITRUST, HHS 405(d), CISA HPH CPGs, clinical segmentation, biomedical IoT, EHR paths, PHI-safe ops. Use for health-system campuses, PACS, RTLS, nurse call, or any ePHI on the wire.
origin: snm-pack
---

# Healthcare network

Clinical safety outranks uptime theater. A network event that delays
care is a **patient-safety event**, not just a Sev1. Treat PHI as toxic
in tickets, captures, and chat.

## When to use

- Hospital, clinic, imaging, lab, pharmacy, telehealth, research
- HIPAA / HITRUST / Joint Commission / CMS / 42 CFR Part 2
- Biomedical devices, EHR (Epic/Oracle Health), PACS/DICOM, RTLS, Vocera
- Vendor remote access to clinical systems
- Segmentation, wireless for voice/location, clinical change windows

Always pair with `network-security-posture` for NAC/ZTA and
`network-change-cab` for production changes.

## Non-negotiables

1. **Map the ePHI path** before you touch a VLAN. If you cannot name where
   PHI rides, you do not change that path.
2. **No full packet capture** on clinical or biomedical segments. Metadata
   (NetFlow, SNMP, telemetry) only. Redact IPs that map to a patient room
   if the ticket would identify a patient.
3. **BAAs** for every vendor who can see PHI or manage a box in the path.
4. **Clinical windows** — not "after hours". Avoid first-case (≈06:30–09:30)
   and turnover (≈15:00–19:00) unless the CMO/clinical engineering agrees.
   Imaging and pharmacy have their own calendars.
5. **Medical devices are not laptops.** Do not domain-join, do not dump
   them on the user VLAN, do not force a TLS version they cannot speak.
   Isolate, monitor, compensate. See [reference/biomedical-iot.md](reference/biomedical-iot.md).
6. **Break-glass** is designed, logged, and reviewed — not a sticky note
   with the local-admin password.

## Segmentation default (health system)

| VRF / zone | What lives there | East-west |
|------------|------------------|-----------|
| Biomedical / clinical engineering | Infusion, vents, monitoring, imaging modalities | Deny to user/guest; broker to EHR/PACS |
| Clinical workstation | EHR, Pyxis, nurse station | Brokered only |
| Voice / RTLS / nurse call | QoS EF; location SSIDs | Isolated |
| Guest / patient wifi | Internet only | No corp, no biomedical |
| Building / OT | BAS, HVAC, cameras | No clinical |
| Cardholder / PCI | Gift shop, cafeteria | Isolated |
| Research / 42 CFR Part 2 | Extra consent + tighter logging | Separate |
| Management / OOB | Network + server ILO | No in-band user |

Details: [reference/clinical-segmentation.md](reference/clinical-segmentation.md).

## HIPAA technical safeguards (network-relevant)

Map every design to 45 CFR 164.312 and NIST SP 800-66r2. Minimum:

- Access control + unique IDs + auto-logoff on shared clinical workstations
  (network enforces 802.1X / NAC; do not rely on the app alone)
- Audit controls on management plane, VPN, NAC, firewall
- Integrity + transmission security for ePHI in motion (TLS, no cleartext
  DICOM/HL7 on user or guest VLANs)
- Person/entity authentication for admins and vendors (no shared TACACS
  "cisco/cisco")

HITRUST and HHS 405(d) HICP are how you **evidence** this, not a substitute.
CISA HPH Cybersecurity Performance Goals are the floor for internet exposure
and MFA on remote access.

Full control table: [reference/hipaa-technical-safeguards.md](reference/hipaa-technical-safeguards.md).

## EHR / imaging path checks

- Epic Interconnect, Hyperspace, Kuiper, Care Everywhere, MyChart — list
  the **actual** flows (not "the Epic VLAN"). Print, ROE, MyChart, and
  Care Everywhere have different blast radii.
- PACS/VNA/DICOM: modality → PACS is high-bandwidth, often multicast or
  jumbo; do not put it through a user firewall policy that times out.
- Identity: clinical SSO outage is a care outage. Dual path to IdP.
- Printers, WOWs, scanners: NAC exceptions must be ticketed and expire.

## Output

```text
CLINICAL SAFETY
- could this delay care? which units?

ePHI PATH
- systems · protocols · segments · BAA status

CONTROLS
- HIPAA 164.312 / HICP / CPG mapping (gaps only)

SEGMENTATION
- as-is vs default zones · exceptions

CHANGE WINDOW
- clinical calendar · rollback · verifier (network + clinical eng)

EVIDENCE
- what an auditor / Joint Commission would want to see
```

## Reference Files
- [reference/hipaa-technical-safeguards.md](reference/hipaa-technical-safeguards.md)
- [reference/clinical-segmentation.md](reference/clinical-segmentation.md)
- [reference/biomedical-iot.md](reference/biomedical-iot.md)
