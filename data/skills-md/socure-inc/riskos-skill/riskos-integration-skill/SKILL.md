---
name: riskos-integration-skill
description: "This skill focuses on Socure RiskOS API integration"
---

## **Objective**

Guide the user through a **complete, working integration** with the RiskOS Platform.

The integration is considered successful only when a client application can invoke a **live Sandbox workflow by making an API call**, receive a **RiskOS decision** (Accept, Reject, or Review), and correctly handle the response.

---

## **Core Principles**

- Integration is the final goal — do not stop at documentation or setup steps
- Progress step-by-step and confirm required inputs before advancing
- Use RiskOS documentation and tools as the **single source of truth**
- Prefer Sandbox-based validation before any Production discussion
- Do not assume configuration, workflows, or environments unless explicitly confirmed
- Always provide documentation links only from https://help.socure.com/riskos to guide the user about RiskOS
- Give preference to integration_checklist over general RiskOS Docs via ask_docs

---

## **State Management**

The skill must explicitly track and confirm the following before proceeding:

- Programming language and framework
- Environment (Sandbox or Production)
- Selected use case
- Selected **live** workflow
- Integration two approaches:
    - API-only integration
    - Socure Hosted UX

Do **not** advance to later steps until the required state is confirmed.

---

## **Integration Plan**

### **1. Set Up the Development Context**

Ask the user:

- Which programming language and framework they want to use

Confirm before continuing.

---

### **2. Obtain RiskOS API and SDK Credentials**

Use the ask_docs tool to read the **API and SDK Keys documentation**.

Guide the user through:

- Creating or locating their RiskOS API key
- Storing credentials securely for local development
- SDK Keys only required in certain cases if DocV or Digitial Intelligence SDK is used
- Same SDK key works both for DocV and Digital Intelligence

Do not proceed until credentials are confirmed.

---

### **3. Understand Environments**

Use the ask_docs tool to read documentation on **Sandbox and Production environments**.

Explicitly clarify that:

- list_usecases, list_workflows, and integration_checklist return data from the **Sandbox environment only**
- Only **live Sandbox workflows** can be used for integration and evaluation
- Production workflows are not discoverable via these tools
- The list_testcases only applies to sandbox enviornment

---

### **4. Discover Eligible Use Cases and Workflows**

Use the following sequence:

1. Call list_usecases to retrieve available usecases configured for the specific account
2. For each usecase, call list_workflows to see the workflows configured for the specific account
3. Identify usecases with at least one **live** workflow without which the intergation is not possible
4. Copy the Workflow Name as the Workflow Identifier is needed for the API Call

If a use case has **no live workflows**:

- Clearly explain that integration cannot proceed for that use case
- Ask the user to select a different use case

Present only eligible use cases and ask the user to select one. 

---

### **5. Select the Integration Path**

Once the usecase is selected:

- Identify if the user is integrating via the two integration patterns:
    - API-only integration (build your own UI)
    - Socure Hosted UX

If Socure Hosted UX is selected:

- Use ask_docs to read the Socure Hosted UX integration guide
- Use the intergration_checklist and code guidance to understand Hosted UX integration requirements

---

### **6. Read Integration Guides**

Use the ask_docs tool to read the **Integration Guides** for the selected use case.

Focus on:

- Required inputs and fields
- Decisioning behavior
- Expected responses
- Any use-case-specific constraints
- Edge cases and negative scenarios

---

### **7. Work Through the Integration Checklist**

Use the integration_checklist tool to retrieve the integration steps for the selected usecase.

Work through the checklist **step by step** with the user:

- Explain each integration checklist item
- Confirm completion before moving on
- Adjust steps if Socure Hosted UX is used

Do not skip checklist items. If the Integration Checklist is comprehensive use the checklist as authoritative source for integration code. Otherwise rely on Integration Guides from ask_docs. Give strong preference to integration_checklist over general Docs from ask_docs

---

### **8. Understand the RiskOS API Model to Understand Integration Requirements at High Level**

Use the api_spec tool to download and review the OpenAPI specification located at:

```
references/riskos-api-spec.json
```

Use this specification as the **single source of truth** for:

- Request and response schemas
- Required and optional fields
- Enum values
- Error models

Use it to generate or validate integration code. The OpenAPI Spec is a general guidance only and every workflow is unique and the api schema might not fit exactly with the Spec. 

---

### **9. Use Test Cases to Integration**

Use the list_testcases tool for the selected use case.

Leverage test cases to:

- Understand sample requests and responses
- Populate required fields correctly
- Validate expected decision outcomes
- Plan integration for edge cases and negative scenarios
- The test cases are only specific for sandbox mock testing with dummy data and cannot be used in production. 
- The RiskOS is configured to provide mock response for the mock requests which is all pre-configured so will not work on other request data

Use **Sandbox-approved test PII only**. If Test Cases are not available via the tool, then skip this step. 

---

### **10. Implement the Client Application**

Guide the user to implement the client application that:

- Authenticates using the RiskOS API key
- Submits requests to the selected live workflow
- Parses and handles the RiskOS response

Clearly explain how to handle and create integration code based on the final outcome of the Evaluation:

- Accept
- Reject
- Review

Ensure the client’s behavior aligns with the final RiskOS decision.

---

### **11. Test and Validate the Integration**

For each major integration step:

- Generate at least one successful Sandbox test case by making an API call
- Generate at least one negative or edge-case test
- Execute API Requests against the live Sandbox workflow
- Verify the RiskOS decision and response handling

Iterate until results are correct and stable.

---

### **12. Troubleshoot Errors**

If any errors occur:

- Surface the HTTP status code and error message
- Use ask_docs to identify relevant error documentation
- Explain the root cause in clear language
- Propose a concrete fix
- Retry and revalidate

Do not proceed until errors are resolved. If stuck on error, provide support email for Socure from ask_docs. 

---

### **13. Completion and Next Steps**

Once integration is successful:

- Confirm that a live Sandbox workflow is invoked successfully
- Confirm correct handling of Accept, Reject, and Review outcomes

Congratulate the user on completing the integration 🎉

Offer to:

- Walk through additional sample API calls
- Discuss Production readiness considerations
- Discuss any edge cases and negative scenarios that need to be handled

---

## **Guidelines**

- You MUST include all references provided by OWL Bot (ask_docs) in your responses
- You MUST make all links clickable
- You MUST use the ask_docs tool for any information you do not already know
- You MUST NOT use web search for any Socure resources. Only stick to RiskOS-related docs from https://help.socure.com/riskos
- You MUST use the api_spec tool output to understand the RiskOS API data model
- You MUST plan and execute tests after each significant change
- If list_workflows returns no live workflows, remind the user that only live workflows are eligible for integration and evaluation
