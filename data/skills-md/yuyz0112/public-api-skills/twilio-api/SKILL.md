---
name: twilio-api
description: This is the public Twilio REST API.. Use when working with the Twilio - Api or when the user needs to interact with this API.
license: Apache 2.0 (https://www.apache.org/licenses/LICENSE-2.0.html)
metadata:
  api-version: "1.0.0"
  openapi-version: "3.0.1"
  contact: "support@twilio.com"
---

# Twilio - Api

This is the public Twilio REST API.

## How to Use This Skill

This API documentation is split into multiple files for on-demand loading.

**Directory structure:**
```
references/
├── resources/      # 75 resource index files
├── operations/     # 197 operation detail files
└── schemas/        # 57 schema groups, 148 schema files
```

**Navigation flow:**
1. Find the resource you need in the list below
2. Read `references/resources/<resource>.md` to see available operations
3. Read `references/operations/<operation>.md` for full details
4. If an operation references a schema, read `references/schemas/<prefix>/<schema>.md`

## Base URL

- `https://api.twilio.com`

## Authentication

Supported methods: **accountSid_authToken**. See `references/authentication.md` for details.

## Resources

- **Api20100401Address** → `references/resources/Api20100401Address.md` (5 ops)
- **Api20100401Application** → `references/resources/Api20100401Application.md` (5 ops)
- **Api20100401Call** → `references/resources/Api20100401Call.md` (5 ops)
- **Api20100401CallRecording** → `references/resources/Api20100401CallRecording.md` (5 ops)
- **Api20100401IncomingPhoneNumber** → `references/resources/Api20100401IncomingPhoneNumber.md` (5 ops)
- **Api20100401Message** → `references/resources/Api20100401Message.md` (5 ops)
- **Api20100401Participant** → `references/resources/Api20100401Participant.md` (5 ops)
- **Api20100401Queue** → `references/resources/Api20100401Queue.md` (5 ops)
- **Api20100401Credential** → `references/resources/Api20100401Credential.md` (5 ops)
- **Api20100401CredentialList** → `references/resources/Api20100401CredentialList.md` (5 ops)
- **Api20100401Domain** → `references/resources/Api20100401Domain.md` (5 ops)
- **Api20100401IpAccessControlList** → `references/resources/Api20100401IpAccessControlList.md` (5 ops)
- **Api20100401SipIpAddress** → `references/resources/Api20100401SipIpAddress.md` (5 ops)
- **Api20100401Trigger** → `references/resources/Api20100401Trigger.md` (5 ops)
- **Api20100401Account** → `references/resources/Api20100401Account.md` (4 ops)
- **Api20100401ConferenceRecording** → `references/resources/Api20100401ConferenceRecording.md` (4 ops)
- **Api20100401ConnectApp** → `references/resources/Api20100401ConnectApp.md` (4 ops)
- **Api20100401AssignedAddOn** → `references/resources/Api20100401AssignedAddOn.md` (4 ops)
- **Api20100401Key** → `references/resources/Api20100401Key.md` (4 ops)
- **Api20100401SigningKey** → `references/resources/Api20100401SigningKey.md` (4 ops)
- **Api20100401OutgoingCallerId** → `references/resources/Api20100401OutgoingCallerId.md` (4 ops)
- **Api20100401AuthCallsCredentialListMapping** → `references/resources/Api20100401AuthCallsCredentialListMapping.md` (4 ops)
- **Api20100401AuthCallsIpAccessControlListMapping** → `references/resources/Api20100401AuthCallsIpAccessControlListMapping.md` (4 ops)
- **Api20100401AuthRegistrationsCredentialListMapping** → `references/resources/Api20100401AuthRegistrationsCredentialListMapping.md` (4 ops)
- **Api20100401CredentialListMapping** → `references/resources/Api20100401CredentialListMapping.md` (4 ops)
- **Api20100401IpAccessControlListMapping** → `references/resources/Api20100401IpAccessControlListMapping.md` (4 ops)
- **Api20100401Conference** → `references/resources/Api20100401Conference.md` (3 ops)
- **Api20100401Member** → `references/resources/Api20100401Member.md` (3 ops)
- **Api20100401Recording** → `references/resources/Api20100401Recording.md` (3 ops)
- **Api20100401AddOnResult** → `references/resources/Api20100401AddOnResult.md` (3 ops)
- **Api20100401Payload** → `references/resources/Api20100401Payload.md` (3 ops)
- **Api20100401RecordingTranscription** → `references/resources/Api20100401RecordingTranscription.md` (3 ops)
- **Api20100401ShortCode** → `references/resources/Api20100401ShortCode.md` (3 ops)
- **Api20100401Transcription** → `references/resources/Api20100401Transcription.md` (3 ops)
- **Api20100401AuthorizedConnectApp** → `references/resources/Api20100401AuthorizedConnectApp.md` (2 ops)
- **Api20100401AvailablePhoneNumberCountry** → `references/resources/Api20100401AvailablePhoneNumberCountry.md` (2 ops)
- **Api20100401CallNotification** → `references/resources/Api20100401CallNotification.md` (2 ops)
- **Api20100401AssignedAddOnExtension** → `references/resources/Api20100401AssignedAddOnExtension.md` (2 ops)
- **Api20100401IncomingPhoneNumberLocal** → `references/resources/Api20100401IncomingPhoneNumberLocal.md` (2 ops)
- **Api20100401IncomingPhoneNumberMobile** → `references/resources/Api20100401IncomingPhoneNumberMobile.md` (2 ops)
- **Api20100401IncomingPhoneNumberTollFree** → `references/resources/Api20100401IncomingPhoneNumberTollFree.md` (2 ops)
- **Api20100401MediaInstance** → `references/resources/Api20100401MediaInstance.md` (2 ops)
- **Api20100401Notification** → `references/resources/Api20100401Notification.md` (2 ops)
- **Api20100401Payment** → `references/resources/Api20100401Payment.md` (2 ops)
- **Api20100401CallTranscription** → `references/resources/Api20100401CallTranscription.md` (2 ops)
- **Api20100401Siprec** → `references/resources/Api20100401Siprec.md` (2 ops)
- **Api20100401Stream** → `references/resources/Api20100401Stream.md` (2 ops)
- **Api20100401UserDefinedMessageSubscription** → `references/resources/Api20100401UserDefinedMessageSubscription.md` (2 ops)
- **Api20100401Local** → `references/resources/Api20100401Local.md` (1 ops)
- **Api20100401MachineToMachine** → `references/resources/Api20100401MachineToMachine.md` (1 ops)
- **Api20100401Mobile** → `references/resources/Api20100401Mobile.md` (1 ops)
- **Api20100401National** → `references/resources/Api20100401National.md` (1 ops)
- **Api20100401SharedCost** → `references/resources/Api20100401SharedCost.md` (1 ops)
- **Api20100401TollFree** → `references/resources/Api20100401TollFree.md` (1 ops)
- **Api20100401Voip** → `references/resources/Api20100401Voip.md` (1 ops)
- **Api20100401Balance** → `references/resources/Api20100401Balance.md` (1 ops)
- **Api20100401Event** → `references/resources/Api20100401Event.md` (1 ops)
- **Api20100401DependentPhoneNumber** → `references/resources/Api20100401DependentPhoneNumber.md` (1 ops)
- **Api20100401NewKey** → `references/resources/Api20100401NewKey.md` (1 ops)
- **Api20100401Media** → `references/resources/Api20100401Media.md` (1 ops)
- **Api20100401Feedback** → `references/resources/Api20100401Feedback.md` (1 ops)
- **Api20100401NewSigningKey** → `references/resources/Api20100401NewSigningKey.md` (1 ops)
- **Api20100401ValidationRequest** → `references/resources/Api20100401ValidationRequest.md` (1 ops)
- **Api20100401Data** → `references/resources/Api20100401Data.md` (1 ops)
- **Api20100401Token** → `references/resources/Api20100401Token.md` (1 ops)
- **Api20100401Record** → `references/resources/Api20100401Record.md` (1 ops)
- **Api20100401AllTime** → `references/resources/Api20100401AllTime.md` (1 ops)
- **Api20100401Daily** → `references/resources/Api20100401Daily.md` (1 ops)
- **Api20100401LastMonth** → `references/resources/Api20100401LastMonth.md` (1 ops)
- **Api20100401Monthly** → `references/resources/Api20100401Monthly.md` (1 ops)
- **Api20100401ThisMonth** → `references/resources/Api20100401ThisMonth.md` (1 ops)
- **Api20100401Today** → `references/resources/Api20100401Today.md` (1 ops)
- **Api20100401Yearly** → `references/resources/Api20100401Yearly.md` (1 ops)
- **Api20100401Yesterday** → `references/resources/Api20100401Yesterday.md` (1 ops)
- **Api20100401UserDefinedMessage** → `references/resources/Api20100401UserDefinedMessage.md` (1 ops)
