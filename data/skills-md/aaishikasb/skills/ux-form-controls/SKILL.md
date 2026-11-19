---
name: ux-form-controls
description: Specify or audit how a form turns a person's answer into a stored value. Use for choosing inputs, handling formatted or uploaded values, and helping people correct a rejected submission.
license: MIT
---

# Design from a sample submission

Ask what someone filling out this form has in front of them. A warehouse worker can copy a bin label from the shelf. They may need to look up the replacement part that belongs in that bin. Both fields could store IDs, but only one calls for typing the ID.

Inspect the actual form, its submit handler, and any rules the receiving service applies. For a design without code, work from the supplied data contract and identify assumptions. Pick a value that a careless implementation would change, such as a bin labeled `04-B` or a part name shared by two suppliers.

Start with the project's existing native or shared controls. When a custom widget is necessary, specify its accessible name, value, state, and keyboard operation together. A visual resemblance to a control does not supply its behavior.

1. **Choose how to answer.** Decide whether the person supplies a value, picks an existing record, or changes a preference. Check whether an empty answer is allowed and whether the change takes effect now or after Save. Use the [entry cases](references/field-choices.md) for decisions about individual controls.
2. **Follow the value.** Write down what the user enters, what the control displays, and what the service should receive. Try pasting an answer and changing its middle characters. Formatting that moves the caret, drops a leading zero, or changes the unit can make a valid answer impossible to enter.
3. **Design the correction.** Give the field a persistent label. Put a necessary constraint where it can be read before entry. Wait until a rule can be evaluated fairly before reporting a mistake. On rejection, name the affected field and a correction the person can make. Associate the error with the field, expose its invalid state, and retain the rest of the safe draft. Move focus to the first problem or a linked error summary when submission fails. Revalidate submitted values on the server, including rules that depend on current availability or permissions.
4. **Finish the round trip.** Submit the corrected example, inspect the accepted value, and reopen the form. Distinguish a blank answer from zero, a saved change from a pending one, and a returned error from a second submission.

For a proposal, show the control and one worked entry-to-save example for each disputed choice. For a review, give the failing input, the observed result, and the smallest fix. For implementation, run that example through the supported submission path, including keyboard entry and error recovery. Check that enlarged text and a narrow viewport leave labels, focus, and correction actions visible. Identify any behavior you could only inspect in code.
