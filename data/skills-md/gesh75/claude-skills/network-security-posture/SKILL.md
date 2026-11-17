---
name: network-security-posture
description: Network security posture — segmentation, 802.1X/NAC, Zero Trust overlays, vendor remote access, management plane, medical-device isolation. Use for ZTA, NAC design, "flatten this campus", or CISA HPH exposure. Pair with healthcare-network when ePHI is in play.
origin: snm-pack
---

# Network security posture

The network is a control plane for identity and blast radius, not a
very expensive patch cable. Default-deny east-west. Management is a
separate world.

## When to use

- Segmentation / microseg / SGT / ACI / NGFW brokers
- NAC (802.1X, MAB, posture), guest, contractor
- Vendor remote access / PAM
- Internet exposure of infrastructure
- Zero Trust network overlay

Healthcare: also load `healthcare-network`. Device changes: `netops-mcp`.

## Priority order (do not skip)

1. **Know the assets** (cannot isolate ghosts)
2. **Management plane** isolated, MFA, no public SSH/HTTPS
3. **Internet attack surface** (CISA HPH CPG): no device GUIs on 0.0.0.0/0
4. **Named east-west flows** through a broker
5. **NAC** for users; MAB only with inventory + expiry
6. **Vendor access** time-bound, recorded, BAA if PHI
7. Overlay / ZTA tunnels — after the above, not instead of

Details: [reference/nac-and-mgmt.md](reference/nac-and-mgmt.md).

## Management plane

- OOB preferred; in-band mgmt VRF if OOB is impossible
- AAA per-person, command authorization, session log
- No default creds, no SNMP v2c on clinical, v3 or stream
- Jump / PAM for humans and vendors
- Config backup off-box, unauthorized diff = incident

## Vendor access

Persistent site-to-site into biomedical or EHR is a defect. Replace
with: ticket → expiry → PAM → record → revoke. If the vendor refuses,
that is a contract issue for the SNM, not a firewall any-any.

## Output

```text
EXPOSURE
- public mgmt · open flows · vendor tunnels

SEGMENTATION
- as-is vs named zones · top exceptions

NAC
- 802.1X coverage · MAB count · expiry hygiene

TREATMENTS
- ranked · owner · CAB
```

Do not recommend "install more tools" before closing public management
and unnamed any-any rules.

## Reference Files
- [reference/nac-and-mgmt.md](reference/nac-and-mgmt.md)
