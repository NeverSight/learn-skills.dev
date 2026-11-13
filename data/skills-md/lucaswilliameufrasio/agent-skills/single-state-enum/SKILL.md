---
name: single-state-enum
description: >-
  Controls UI status (modals, sheets, drawers, tabs, steps, view modes) with a
  single state holding a discriminated union / enum instead of many independent
  booleans, nulls, and strings. Applies to any frontend — Svelte
  ($state), Vue (ref), React (useState), and Flutter/Dart — to keep dialogs,
  overlays, and multi-step flows consistent and easy to maintain. Use whenever
  adding or reviewing any modal, dialog, confirmation, wizard, tab, or view-mode
  state.
---

# Single State, Enum (Discriminated Union)

## Regra

Nunca crie vários `$state`/`ref`/`useState` booleanos (ou `null`) para controlar
modais, abas, etapas ou modos de exibição. Use **um único estado** cujo valor é
uma **discriminated union** (um enum com payload), onde `type` (ou `status`)
identifica o estado ativo.

O `type` é sempre explícito — inclusive o estado "fechado/none". Isso elimina a
classe inteira de bugs de "dois toggles dessincronizados" e deixa explícito
qual overlay pode estar aberto (só um por vez).

## Por quê

- **Um invariante, um lugar**: se dois modais dependem de `showX` e `showY`,
  nada impede `showX && showY` ao mesmo tempo, ou o fechamento de um não limpar
  o outro. Com uma union, só existe um valor por vez.
- **Payload junto**: dados do item-alvo (ex.: qual regra deactivate, qual fee
  deletar) vivem no mesmo estado, então não há `selectedX` + `showDialog`
  dessincronizados.
- **Maintenance**: adicionar um novo modal = adicionar um case na union, não
  um par de variáveis novas.
- **Narrowing nativo**: o compilador/IDE estreita o tipo pelo `type`, então
  `dialog.rule` só é acessível quando `dialog.type === 'deactivate-rule'`.

## Padrão (Svelte 5 / Vue / React)

### Svelte 5 (runes)

```ts
type DialogState =
	| { type: 'none' }
	| { type: 'add-rule' }
	| { type: 'deactivate-rule'; rule: Rule };

let dialog = $state<DialogState>({ type: 'none' });

// abrir
dialog = { type: 'deactivate-rule', rule };
// fechar (sempre seta um estado explícito)
dialog = { type: 'none' };
```

```svelte
{#if dialog.type === 'deactivate-rule'}
	{@const rule = dialog.rule}
	<AlertDialog.Root open onOpenChange={() => (dialog = { type: 'none' })}>
		<AlertDialog.Title>Deactivate {rule.name}?</AlertDialog.Title>
		<AlertDialog.Action onclick={() => { deactivate(rule); dialog = { type: 'none' }; }}>
			Deactivate
		</AlertDialog.Action>
	</AlertDialog.Root>
{/if}
```

> Use `{#if}` + `{@const}` em volta do overlay para o `type` do TS estreitar
> dentro dos handlers. Prefira `open` (prop) com `onOpenChange` a `bind:open`
> com expressão.

### Vue 3 (composition API)

```ts
type DialogState =
	| { type: 'none' }
	| { type: 'deactivate-rule'; rule: Rule };

const dialog = ref<DialogState>({ type: 'none' });
```

```vue
<AlertDialog :open="dialog.type === 'deactivate-rule'"
             @update:open="v => v || (dialog = { type: 'none' })">
  <template v-if="dialog.type === 'deactivate-rule'">
    <AlertDialogTitle>Deactivate {{ dialog.rule.name }}?</AlertDialogTitle>
  </template>
</AlertDialog>
```

### React

```ts
type DialogState =
	| { type: 'none' }
	| { type: 'deactivate-rule'; rule: Rule };

const [dialog, setDialog] = useState<DialogState>({ type: 'none' });
```

### Flutter/Dart

```dart
sealed class DialogState {}
class DialogNone extends DialogState {}
class DialogDeactivateRule extends DialogState {
  final Rule rule;
  DialogDeactivateRule(this.rule);
}

DialogState dialog = DialogNone();
// switch (dialog) { case DialogDeactivateRule(): ... }
```

## Convenções

- O valor de `type`/`status` usa **kebab-case** (`'deactivate-rule'`,
  `'add-rule'`, `'refund'`, `'none'`) — legível em logs e no estado.
- O estado "fechado" é **sempre `{ type: 'none' }`**, nunca `null`/`undefined`
  — assim os handlers de fechamento são idênticos (atribuem `{ type: 'none' }`).
- **Um overlay por vez**: se abrir um segundo modal a partir de outro (ex.:
  "Issue Refund" dentro do inspector), troque o `type` do mesmo estado em vez
  de empilhar.
- **Fechamento**: nos `onOpenChange`/`@update:open`, quando `open` for `false`,
  atribua `{ type: 'none' }` — nunca preserve um estado fantasma.

## Quando NÃO usar

- Estado **boolean real** (uma única condição on/off que nunca cresce) pode ser
  um boolean simples: ex. `loading`, `showPassword`, `expanded`.
- Estado que representa **dado** (não status de UI): ex. `editingFeeId` (o alvo
  da edição) pode ser um id separado; a union descreve o *overlay/status*.
- Estado de **multiseleção** não cabe em union de status.

## Exemplo completo (fechar = reset)

```ts
type PaymentDialog =
	| { type: 'none' }
	| { type: 'inspector'; payment: Payment }
	| { type: 'refund'; payment: Payment };

let dialog = $state<PaymentDialog>({ type: 'none' });

function openInspector(p: Payment) {
	dialog = { type: 'inspector', payment: p };
}
function openRefund(p: Payment) {
	dialog = { type: 'refund', payment: p };
}
function closeDialog() {
	dialog = { type: 'none' };
}
```

## Checklist

- [ ] Um único estado para cada "zona de overlays" (modais/dialogs que não podem
      coexistir) — não um boolean por modal.
- [ ] Tipo `{ type: 'none' } | { type: '...'; ... }` (discriminated union).
- [ ] Fechar sempre atribui `{ type: 'none' }`.
- [ ] Payload (regra/fee/payment alvo) no mesmo objeto da union.
- [ ] `type` em kebab-case.
- [ ] Narrowing via `{#if dialog.type === '...'}` + `{@const}` (ou `switch`).