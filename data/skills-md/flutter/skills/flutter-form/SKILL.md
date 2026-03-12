---
name: "flutter-form"
description: "Build a form with validation"
metadata:
  model: "models/gemini-3.1-pro-preview"
  last_modified: "Wed, 11 Mar 2026 16:47:50 GMT"

---
# Flutter Form Validation

## Goal
Implements stateful form validation in Flutter using `Form`, `TextFormField`, and `GlobalKey<FormState>`. Manages validation state efficiently without unnecessary key regeneration and handles user input validation workflows. Assumes a pre-existing Flutter environment with Material Design dependencies available.

## Decision Logic
When implementing form validation, follow this decision tree to determine the flow of state and UI updates:
1. **User triggers submit action:**
   - Call `_formKey.currentState!.validate()`.
2. **Does `validate()` return `true`?**
   - **Yes (Valid):** Proceed with data processing (e.g., API call, local storage). Trigger success UI feedback (e.g., `SnackBar`, navigation).
   - **No (Invalid):** The `FormState` automatically rebuilds the `TextFormField` widgets to display the `String` error messages returned by their respective `validator` functions. Halt submission.

## Instructions

1. **Initialize the Stateful Form Container**
   Create a `StatefulWidget` to hold the form. Instantiate a `GlobalKey<FormState>` exactly once within the `State` class to prevent resource-expensive key regeneration during `build` cycles.
   ```dart
   import 'package:flutter/material.dart';

   class CustomValidatedForm extends StatefulWidget {
     const CustomValidatedForm({super.key});

     @override
     State<CustomValidatedForm> createState() => _CustomValidatedFormState();
   }

   class _CustomValidatedFormState extends State<CustomValidatedForm> {
     // Instantiate the GlobalKey once in the State object
     final _formKey = GlobalKey<FormState>();

     @override
     Widget build(BuildContext context) {
       return Form(
         key: _formKey,
         child: Column(
           crossAxisAlignment: CrossAxisAlignment.start,
           children: <Widget>[
             // Form fields will be injected here
           ],
         ),
       );
     }
   }
   ```

2. **Implement TextFormFields with Validation Logic**
   Inject `TextFormField` widgets into the `Form`'s widget tree. Provide a `validator` function for each field.
   ```dart
   TextFormField(
     decoration: const InputDecoration(
       hintText: 'Enter your email',
       labelText: 'Email',
     ),
     validator: (String? value) {
       if (value == null || value.isEmpty) {
         return 'Please enter an email address';
       }
       if (!value.contains('@')) {
         return 'Please enter a valid email address';
       }
       // Return null if the input is valid
       return null; 
     },
     onSaved: (String? value) {
       // Handle save logic here
     },
   )
   ```

3. **Implement the Submit Action and Validation Trigger**
   Create a button that accesses the `FormState` via the `GlobalKey` to trigger validation.
   ```dart
   Padding(
     padding: const EdgeInsets.symmetric(vertical: 16.0),
     child: ElevatedButton(
       onPressed: () {
         // Validate returns true if the form is valid, or false otherwise.
         if (_formKey.currentState!.validate()) {
           // Save the form fields if necessary
           _formKey.currentState!.save();
           
           // Provide success feedback
           ScaffoldMessenger.of(context).showSnackBar(
             const SnackBar(content: Text('Processing Data')),
           );
         }
       },
       child: const Text('Submit'),
     ),
   )
   ```

4. **STOP AND ASK THE USER:**
   Pause implementation and ask the user for the following context:
   * "What specific fields do you need in this form?"
   * "What are the exact validation rules for each field (e.g., regex patterns, minimum lengths)?"
   * "What action should occur upon successful validation (e.g., API payload submission, navigation)?"

5. **Validate-and-Fix Loop**
   After generating the form, verify the following:
   * Ensure `_formKey.currentState!.validate()` is null-checked properly using the bang operator (`!`) or safe calls if the key might be detached.
   * Verify that every `validator` function explicitly returns `null` on success. Returning an empty string (`""`) will trigger an error state with no text.

## Constraints
* **DO NOT** instantiate the `GlobalKey<FormState>` inside the `build` method. It must be a persistent member of the `State` class.
* **DO NOT** use a `StatelessWidget` for the form container unless the `GlobalKey` is being passed down from a stateful parent.
* **DO NOT** use standard `TextField` widgets if you require built-in form validation; you must use `TextFormField` (which wraps `TextField` in a `FormField`).
* **ALWAYS** return `null` from a `validator` function when the input is valid.
* **ALWAYS** ensure the `Form` widget is a common ancestor to all `TextFormField` widgets that need to be validated together.
