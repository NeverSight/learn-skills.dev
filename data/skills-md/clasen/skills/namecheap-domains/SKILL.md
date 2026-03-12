---
name: namecheap-domains
description: Manage domains through the Namecheap API — register, renew, transfer, configure DNS, and manage nameservers. Use when the user mentions "namecheap", "register domain", "domain DNS", "nameservers", "domain transfer", "renew domain", "check domain availability", "DNS records", "email forwarding", "WHOIS", or any domain registrar operations. Also use when managing A records, CNAME, MX records, or TXT records for Namecheap domains.
metadata:
  author: Martin Clasen
  version: 1.0.0
  category: infrastructure
  tags: [domains, dns, namecheap, registrar, nameservers]
---

# Namecheap Domains

Skill for managing domains through the Namecheap API. Covers domain registration, DNS configuration, nameserver management, and domain transfers.

These methods work only for domains registered with Namecheap that are present in the user's account.

## Prerequisites

The user needs these credentials configured as environment variables:

| Variable | Description |
|----------|-------------|
| `NAMECHEAP_API_USER` | API username |
| `NAMECHEAP_API_KEY` | API key from Namecheap account |
| `NAMECHEAP_USERNAME` | Namecheap account username (usually same as API user) |
| `NAMECHEAP_CLIENT_IP` | Whitelisted IP address for API access |

If any are missing, ask the user to set them. API access must be enabled in the Namecheap account dashboard and the client IP must be whitelisted.

## API Basics

**Base URL:** `https://api.namecheap.com/xml.response`
**Sandbox URL:** `https://api.sandbox.namecheap.com/xml.response`

Every request requires these global parameters:

| Parameter | Description |
|-----------|-------------|
| `ApiUser` | Username required to access the API |
| `ApiKey` | API key |
| `UserName` | Account username (use ApiUser if managing own account) |
| `ClientIp` | Whitelisted IP address |
| `Command` | API command to run (e.g., `namecheap.domains.getList`) |

### Making requests

Use HTTP GET for read operations and HTTP POST for write operations (especially `domains.create` due to the large number of parameters).

```bash
# GET example — list domains
curl -s "https://api.namecheap.com/xml.response?\
ApiUser=${NAMECHEAP_API_USER}&\
ApiKey=${NAMECHEAP_API_KEY}&\
UserName=${NAMECHEAP_USERNAME}&\
ClientIp=${NAMECHEAP_CLIENT_IP}&\
Command=namecheap.domains.getList"
```

```bash
# POST example — create domain
curl -s -X POST "https://api.namecheap.com/xml.response" \
  -d "ApiUser=${NAMECHEAP_API_USER}" \
  -d "ApiKey=${NAMECHEAP_API_KEY}" \
  -d "UserName=${NAMECHEAP_USERNAME}" \
  -d "ClientIp=${NAMECHEAP_CLIENT_IP}" \
  -d "Command=namecheap.domains.create" \
  -d "DomainName=example.com" \
  -d "Years=1" \
  # ... additional parameters
```

### Parsing XML responses

All responses are XML. Check the `Status` attribute on `ApiResponse`:

```xml
<ApiResponse Status="OK">    <!-- Success -->
<ApiResponse Status="ERROR"> <!-- Failure — check <Errors> -->
```

Use `xmllint` to extract values:

```bash
# Check response status
echo "$response" | xmllint --xpath "string(//ApiResponse/@Status)" -

# Extract error messages
echo "$response" | xmllint --xpath "//Errors/Error/text()" - 2>/dev/null

# Extract specific attributes
echo "$response" | xmllint --xpath "string(//DomainCreateResult/@Registered)" -
```

If `xmllint` is not available, use `grep` and `sed` for basic extraction, or Python's `xml.etree.ElementTree`.

## API Quick Reference

### domains.*

| Command | Description |
|---------|-------------|
| `namecheap.domains.getList` | List domains in the account |
| `namecheap.domains.getContacts` | Get contact info for a domain |
| `namecheap.domains.create` | Register a new domain |
| `namecheap.domains.getTldList` | List available TLDs |
| `namecheap.domains.setContacts` | Update contact info for a domain |
| `namecheap.domains.check` | Check domain availability |
| `namecheap.domains.reactivate` | Reactivate an expired domain |
| `namecheap.domains.renew` | Renew an expiring domain |
| `namecheap.domains.getRegistrarLock` | Get lock status |
| `namecheap.domains.setRegistrarLock` | Set lock status |
| `namecheap.domains.getInfo` | Get domain details |

See [references/api-domains.md](references/api-domains.md) for full parameter details.

### domains.dns.*

| Command | Description |
|---------|-------------|
| `namecheap.domains.dns.setDefault` | Use Namecheap default DNS servers |
| `namecheap.domains.dns.setCustom` | Use custom DNS servers |
| `namecheap.domains.dns.getList` | Get DNS servers for a domain |
| `namecheap.domains.dns.getHosts` | Get DNS host records |
| `namecheap.domains.dns.getEmailForwarding` | Get email forwarding settings |
| `namecheap.domains.dns.setEmailForwarding` | Set email forwarding |
| `namecheap.domains.dns.setHosts` | Set DNS host records |

See [references/api-dns.md](references/api-dns.md) for full parameter details.

### domains.ns.*

| Command | Description |
|---------|-------------|
| `namecheap.domains.ns.create` | Create a nameserver |
| `namecheap.domains.ns.delete` | Delete a nameserver |
| `namecheap.domains.ns.getInfo` | Get nameserver info |
| `namecheap.domains.ns.update` | Update nameserver IP |

See [references/api-nameservers.md](references/api-nameservers.md) for full parameter details.

### domains.transfer.*

| Command | Description |
|---------|-------------|
| `namecheap.domains.transfer.create` | Transfer domain to Namecheap |
| `namecheap.domains.transfer.getStatus` | Check transfer status |
| `namecheap.domains.transfer.updateStatus` | Update/resubmit transfer |
| `namecheap.domains.transfer.getList` | List domain transfers |

See [references/api-transfers.md](references/api-transfers.md) for full parameter details.

## Common Workflows

### 1. Check availability and register a domain

```bash
# Step 1: Check availability
curl -s "https://api.namecheap.com/xml.response?\
ApiUser=${NAMECHEAP_API_USER}&ApiKey=${NAMECHEAP_API_KEY}&\
UserName=${NAMECHEAP_USERNAME}&ClientIp=${NAMECHEAP_CLIENT_IP}&\
Command=namecheap.domains.check&DomainList=example.com,example.net"

# Look for: <DomainCheckResult Domain="example.com" Available="true" />

# Step 2: Register (use POST)
curl -s -X POST "https://api.namecheap.com/xml.response" \
  -d "ApiUser=${NAMECHEAP_API_USER}" \
  -d "ApiKey=${NAMECHEAP_API_KEY}" \
  -d "UserName=${NAMECHEAP_USERNAME}" \
  -d "ClientIp=${NAMECHEAP_CLIENT_IP}" \
  -d "Command=namecheap.domains.create" \
  -d "DomainName=example.com" \
  -d "Years=1" \
  -d "RegistrantFirstName=John" \
  -d "RegistrantLastName=Smith" \
  -d "RegistrantAddress1=123 Main St" \
  -d "RegistrantCity=San Francisco" \
  -d "RegistrantStateProvince=CA" \
  -d "RegistrantPostalCode=94102" \
  -d "RegistrantCountry=US" \
  -d "RegistrantPhone=+1.4155551234" \
  -d "RegistrantEmailAddress=john@example.com" \
  -d "TechFirstName=John" \
  -d "TechLastName=Smith" \
  -d "TechAddress1=123 Main St" \
  -d "TechCity=San Francisco" \
  -d "TechStateProvince=CA" \
  -d "TechPostalCode=94102" \
  -d "TechCountry=US" \
  -d "TechPhone=+1.4155551234" \
  -d "TechEmailAddress=john@example.com" \
  -d "AdminFirstName=John" \
  -d "AdminLastName=Smith" \
  -d "AdminAddress1=123 Main St" \
  -d "AdminCity=San Francisco" \
  -d "AdminStateProvince=CA" \
  -d "AdminPostalCode=94102" \
  -d "AdminCountry=US" \
  -d "AdminPhone=+1.4155551234" \
  -d "AdminEmailAddress=john@example.com" \
  -d "AuxBillingFirstName=John" \
  -d "AuxBillingLastName=Smith" \
  -d "AuxBillingAddress1=123 Main St" \
  -d "AuxBillingCity=San Francisco" \
  -d "AuxBillingStateProvince=CA" \
  -d "AuxBillingPostalCode=94102" \
  -d "AuxBillingCountry=US" \
  -d "AuxBillingPhone=+1.4155551234" \
  -d "AuxBillingEmailAddress=john@example.com" \
  -d "AddFreeWhoisguard=yes" \
  -d "WGEnabled=yes"

# Step 3: Verify
# Check response for: <DomainCreateResult Registered="true" />
```

When the user provides contact info once, reuse it for all four contact types (Registrant, Tech, Admin, AuxBilling) unless they specify different contacts.

### 2. Configure DNS records

```bash
# Step 1: Verify domain uses Namecheap DNS
curl -s "https://api.namecheap.com/xml.response?\
ApiUser=${NAMECHEAP_API_USER}&ApiKey=${NAMECHEAP_API_KEY}&\
UserName=${NAMECHEAP_USERNAME}&ClientIp=${NAMECHEAP_CLIENT_IP}&\
Command=namecheap.domains.dns.getList&SLD=example&TLD=com"

# If using custom nameservers, switch to default first (required for host records)
# Command=namecheap.domains.dns.setDefault&SLD=example&TLD=com

# Step 2: Get current records
curl -s "https://api.namecheap.com/xml.response?\
ApiUser=${NAMECHEAP_API_USER}&ApiKey=${NAMECHEAP_API_KEY}&\
UserName=${NAMECHEAP_USERNAME}&ClientIp=${NAMECHEAP_CLIENT_IP}&\
Command=namecheap.domains.dns.getHosts&SLD=example&TLD=com"

# Step 3: Set all records (setHosts replaces ALL records — include existing ones)
curl -s -X POST "https://api.namecheap.com/xml.response" \
  -d "ApiUser=${NAMECHEAP_API_USER}" \
  -d "ApiKey=${NAMECHEAP_API_KEY}" \
  -d "UserName=${NAMECHEAP_USERNAME}" \
  -d "ClientIp=${NAMECHEAP_CLIENT_IP}" \
  -d "Command=namecheap.domains.dns.setHosts" \
  -d "SLD=example" \
  -d "TLD=com" \
  -d "HostName1=@" \
  -d "RecordType1=A" \
  -d "Address1=1.2.3.4" \
  -d "TTL1=1800" \
  -d "HostName2=www" \
  -d "RecordType2=CNAME" \
  -d "Address2=example.com" \
  -d "TTL2=1800"
```

**Critical:** `setHosts` replaces ALL existing records. Always fetch current records first with `getHosts`, then include them alongside new records in the `setHosts` call. Omitting existing records will delete them.

### 3. Transfer a domain to Namecheap

```bash
# Step 1: Initiate transfer
curl -s "https://api.namecheap.com/xml.response?\
ApiUser=${NAMECHEAP_API_USER}&ApiKey=${NAMECHEAP_API_KEY}&\
UserName=${NAMECHEAP_USERNAME}&ClientIp=${NAMECHEAP_CLIENT_IP}&\
Command=namecheap.domains.transfer.create&\
DomainName=example.com&Years=1&EPPCode=AUTH_CODE_HERE"

# Step 2: Monitor transfer status
curl -s "https://api.namecheap.com/xml.response?\
ApiUser=${NAMECHEAP_API_USER}&ApiKey=${NAMECHEAP_API_KEY}&\
UserName=${NAMECHEAP_USERNAME}&ClientIp=${NAMECHEAP_CLIENT_IP}&\
Command=namecheap.domains.transfer.getStatus&TransferID=TRANSFER_ID"
```

Transferable TLDs: .biz, .ca, .cc, .co, .co.uk, .com, .com.es, .com.pe, .es, .in, .info, .me, .me.uk, .mobi, .net, .net.pe, .nom.es, .org, .org.es, .org.pe, .org.uk, .pe, .tv, .us

## Important Notes

- **SLD/TLD splitting:** Many endpoints require `SLD` and `TLD` as separate parameters. For `example.com`, SLD=`example` and TLD=`com`. For `example.co.uk`, SLD=`example` and TLD=`co.uk`.
- **Phone format:** Always use `+NNN.NNNNNNNNNN` (e.g., `+1.4155551234`).
- **IDN domains:** Send the domain name in Punycode format (e.g., `xn--sdkhjsdhfkdh.com`) and include the `IdnCode` parameter.
- **Premium domains:** Set `IsPremiumDomain=True` and provide `PremiumPrice` and optionally `EapFee`.
- **Rate limiting:** Namecheap may throttle requests. If you receive errors, wait before retrying.
- **Sandbox:** Use the sandbox URL for testing. Sandbox credentials are separate from production.

## Error Handling

Common error patterns in the XML response:

```xml
<ApiResponse Status="ERROR">
  <Errors>
    <Error Number="2016166">Domain is not associated with your account</Error>
  </Errors>
</ApiResponse>
```

Always check `Status="OK"` before processing results. If `Status="ERROR"`:
1. Extract the error number and message
2. Check the error codes listed in the relevant reference file
3. Common issues:
   - **Authentication errors:** Verify credentials and whitelisted IP
   - **Domain not found (2019166):** Check domain name and account association
   - **Invalid phone (2015182):** Use format `+NNN.NNNNNNNNNN`
   - **Domain not available (3019166/4019166):** Domain already registered
   - **TLD not supported (2030280):** Check supported TLDs

## Troubleshooting

**Error: Connection refused or timeout**
Cause: Client IP not whitelisted or API access not enabled.
Solution: Check Namecheap dashboard → Profile → Tools → API Access. Verify the IP matches `NAMECHEAP_CLIENT_IP`.

**Error: Empty or malformed response**
Cause: Missing required parameters.
Solution: Verify all global parameters are present. Check that `Command` value is spelled correctly.

**Error: DNS changes not taking effect**
Cause: Domain may be using custom nameservers instead of Namecheap default.
Solution: Call `domains.dns.setDefault` first, then set host records. URL forwarding, email forwarding, and dynamic DNS only work with Namecheap default nameservers.
