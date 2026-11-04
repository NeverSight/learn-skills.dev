---
name: elementor-form-action
description: Build a custom submit action for the Elementor Pro Form widget (send to CRM, post to webhook, write to custom table, fire side effect). Use when the user wants to add a new "After Submit" action to Elementor Pro forms.
---

# elementor-form-action

Pro-only. Requires Elementor Pro Forms module active. Source anchors:

- Abstract: `elementor-pro/modules/forms/classes/action-base.php` (abstract class `Action_Base` lines 10-44).
- Reference action: `elementor-pro/modules/forms/actions/webhook.php`.
- Registrar: `elementor-pro/modules/forms/module.php` (`$this->actions_registrar->register( $instance, $id )`).

## Required methods (extend Action_Base)

- `get_name()` — slug used in the form's `submit_actions` multi-select.
- `get_label()` — human label shown in the action checkbox list.
- `register_settings_section( $widget )` — add controls. Always gate them with `'condition' => [ 'submit_actions' => $this->get_name() ]` so they only show when the action is enabled. Wrap in `start_controls_section` / `end_controls_section`.
- `run( $record, $ajax_handler )` — invoked after a successful submission. `$record` is `Form_Record` (see `classes/form-record.php`): `$record->get( 'fields' )`, `$record->get( 'form_settings' )`, `$record->get( 'meta' )`. Use `$ajax_handler->add_error( $field, $msg )` / `->add_response_data( $key, $value )` to influence the JSON response.
- `on_export( $element )` — strip API keys / secrets from the element data when a template is exported. Return the cleaned element array (or void if no-op).

## Registration

Hook the registrar from your plugin bootstrap. The actions registrar fires on `elementor_pro/forms/actions/register`:

```php
add_action( 'elementor_pro/forms/actions/register', function( $actions_registrar ) {
    require_once __DIR__ . '/actions/my-action.php';
    $actions_registrar->register( new \My_Plugin\Forms\My_Action() );
} );
```

Do not call the deprecated `Plugin::instance()->modules_manager->get_modules('forms')->add_form_action()` — see `forms/module.php:156` (deprecated since 3.5.0).

## Common gotchas

- Settings only show when their action is enabled — always set the `submit_actions` condition.
- Sensitive controls (API key, secret): set `'ai' => [ 'active' => false ]` and `'render_type' => 'none'`. Strip them in `on_export()`.
- For long-running calls (webhook, CRM), don't block — short timeout on `wp_remote_post`, log failures via `error_log` or a custom logger. The submission already ran; throwing here only matters if you call `$ajax_handler->add_error_message()`.
- Fields are keyed by `custom_id` (or auto id). Use the label only for display.
- Honeypot / reCAPTCHA / akismet run before your action — by the time `run()` fires, the submission is considered valid.

## Integration_Base (only if you also need an OAuth/REST panel)

For full CRM-style integrations with a "Connect" panel and remote field mapping, extend `Integration_Base` (`forms/classes/integration-base.php`) instead of plain `Action_Base`. It adds `handle_panel_request()` callbacks routed via the `pro_forms_panel_action_data` ajax action (`forms/module.php:179-181`). Mailchimp / ActiveCampaign / GetResponse handlers in `forms/classes/*-handler.php` are working examples.

For a custom form *field type* (not an action), register on the parallel `fields_registrar` instead (`module.php:144`).

## Deploy & verify

To install the action on a live Pro site and confirm it registered, use `elementor-deploy-verify` (asserts `actions_registrar->get('<name>')`).
