---
name: routeros-certificates
description: Managing X.509 certificates on MikroTik RouterOS 7. Covers certificate templates, creating a private CA and signing server and client certificates, importing and exporting PEM, DER and PKCS12, Let's Encrypt and other ACME certificates, SCEP, revocation lists, key usage and trust stores, and assigning a certificate to a service (HTTPS, SSTP, OpenVPN, IPsec, API-SSL). Use when a service needs a certificate, when issuing or renewing one, when a browser, VPN client or fetch complains about trust, or when exporting keys safely.
---

# RouterOS certificates

Certificates live in `/certificate`. A **template** describes the certificate you want; **signing** turns it into a real
certificate and deletes the template; the result can be used by services that take a `certificate=` property. Private keys never
leave the router unless you export them with a passphrase, which needs the `sensitive` user policy.

## Create a private CA and a server certificate

```ros
/certificate/add name=CA-Template common-name=my-ca key-usage=key-cert-sign,crl-sign days-valid=3650
/certificate/add name=Server-Template common-name=vpn.example.com subject-alt-name=DNS:vpn.example.com days-valid=825
/certificate/sign CA-Template name=my-ca
/certificate/sign Server-Template ca=my-ca name=vpn-server
/certificate/print detail
```

- Defaults: RSA 2048 (`key-size` can also be an EC curve such as `prime256v1`), SHA-256, 365 days, key usage including
  `tls-server` and `tls-client`. A 4096-bit key or larger can take a long time to sign on weak CPUs.
- Use `subject-alt-name` (`DNS:`, `IP:`, `email:`) for the names clients connect to; modern clients ignore the common name.
- Add `ca-crl-host=<address>` when signing if a CRL URL should be embedded.
- Use the real CA name in `ca=`; signing the CA template first produces the `A` (authority) and `T` (trusted) flags.
- Flags in `print`: `K` private key present, `L` CRL, `A` authority, `I` issued, `R` revoked, `E` expired, `T` trusted.

## Use a certificate in a service

Set the service's `certificate` property to the certificate name:

```ros
/ip/service/set www-ssl certificate=vpn-server disabled=no
/interface/sstp-server/server/set certificate=vpn-server enabled=yes
```

Other consumers: OpenVPN server, IPsec identities, the API-SSL service, CAPsMAN and User Manager. A client that must trust your CA
needs the CA certificate (`export-certificate my-ca` and copy the `.crt` out of `/file`).

## Import and export

```ros
/certificate/import file-name=server.pem passphrase="FILE-PASSPHRASE" name=imported
/certificate/export-certificate vpn-server type=pem export-passphrase="REPLACE-ME"
/certificate/export-certificate my-ca            # no passphrase: only the public certificate (.crt)
```

- Upload files to `/file` first. Import takes PEM, DER, CRT and PKCS12 (AES and 3DES). The output tells how many certificates and
  private keys were imported and whether decryption failed.
- With `export-passphrase` the encrypted private key is exported too (a `.key` file for PEM, or inside the `.p12` for PKCS12).
  Treat such files like passwords and delete them from `/file` after copying.
- `trusted=yes` (the import default) marks the certificate as trusted; `trust-store` limits which services may use it for
  verification (`all`, `www`, `sstp`, `ipsec`, `fetch`, `ovpn`, ...).

## ACME and Let's Encrypt

```ros
/certificate/add-acme domain-names=router.example.com
/certificate/add-acme domain-names=[/ip/cloud/get dns-name]       # IP Cloud name: DNS-01 challenge
/certificate/acme-renew numbers=0
```

The domain must resolve to the router and TCP 80 must reach it from the internet (HTTP-01), so allow it in the `input` chain while
the certificate is obtained (`routeros-firewall`). Renewal starts when 80 percent of the validity has passed. Let's Encrypt is the
default directory; set `directory-url` and, if needed, `eab-kid` and `eab-hmac-key` for another ACME service. ACME-managed
certificates carry the `a` flag.

## SCEP, CRL, trust stores

- SCEP: the client fetches the CA certificate, verify its fingerprint yourself, requests a certificate and polls; only RSA keys;
  renewal at three quarters of the lifetime. A SCEP server issues one certificate per request.
- Revocation: off by default. `/certificate/settings/set crl-use=yes crl-download=yes` checks every certificate in a chain, so the
  whole chain (root, intermediates, leaf) must be installed or validation fails.
- The built-in trust store holds public root CAs; `builtin-trust-store` in `/certificate/settings` chooses which services use it.
  Services like `fetch` and email use it to verify servers.

## Common problems

1. Client says "untrusted": the CA certificate is not installed on the client, or the server presents only the leaf. Install the
   CA; for chains, import all certificates.
2. Name mismatch: the certificate lacks a SAN for the address clients use (IP versus DNS name).
3. Expired or "not yet valid": the router clock is wrong; fix NTP first (`routeros-system-utilities`).
4. IPsec rejects the certificate: it must carry the SubjectKeyIdentifier extension (`routeros-ipsec`).
5. `fetch` or another tool cannot verify a server: add the CA to the router and check `trust-store`.

## Where to look

| Need | Open |
| --- | --- |
| Templates, properties, signing, export, import, CRL, ACME, SCEP, built-in CA list | `references/guides/authentication-authorization-accounting/certificates.md` |
| Every property of `/certificate` and its sub-menus | `references/cli/certificate.md` and `references/cli/certificate/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-ipsec`, `routeros-vpn` (SSTP, OpenVPN), `routeros-management-tools` (HTTPS for WebFig), `routeros-hotspot`,
`routeros-user-manager`, `routeros-users-aaa`.
