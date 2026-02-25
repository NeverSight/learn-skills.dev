---

name: angular-frontend-clean-architecture
description: Angular 21 standalone frontend with Clean Architecture, vertical slice (pages by feature), signals, OnPush, and ng-zorro. Use when creating or refactoring Angular apps, adding pages, components, services, directives, pipes, or when the user mentions Angular frontend, standalone components, or signals.
---

# Frontend Angular – Clean Architecture + Standalone

Guia para criar e manter frontends Angular com estrutura por **features** (vertical slice), componentes standalone, signals e ng-zorro-antd.

## Quando usar esta skill

- Adicionar nova **página/feature** (nova pasta em `pages/` com listagem, formulário, service, modelos).
- Criar **componente** reutilizável em `shared/components/`, **diretiva** em `shared/directives/`, **pipe** em `shared/pipes/`.
- Adicionar **service** (HTTP, estado global), **guard**, **interceptor**.
- Definir ou alterar **rotas** em `app.routes.ts`.
- Revisar ou refatorar código para seguir a estrutura e convenções do boilerplate.

## Estrutura do projeto

```
frontend/src/app/
├── app.ts                    # Bootstrap, providers (HTTP, interceptors)
├── app.config.ts             # provideRouter, provideHttpClient, etc.
├── app.routes.ts             # Rotas (guards quando necessário)
├── layout/                   # Layout principal (header, drawer, outlet)
│   └── main-layout/
├── pages/                    # Features por domínio (vertical slice)
│   └── products/
│       ├── product.model.ts
│       ├── product.service.ts
│       └── products-list/    # Uma tela = uma pasta com tudo junto
│           ├── products-list.component.ts
│           ├── products-list.component.html
│           ├── products-list.component.scss
│           └── products-list.component.spec.ts
├── shared/
│   ├── components/           # Componentes reutilizáveis (page-header, loading, etc.)
│   ├── directives/           # Diretivas (autofocus, currency-mask, etc.)
│   ├── pipes/
│   ├── services/             # Serviços globais (loading, layout)
│   ├── guards/
│   ├── interceptors/
│   └── utils/
└── environments/             # environment.apiBaseUrl, etc.
```

Regra: **pages/** contém uma pasta por domínio (ex.: products). Dentro da feature ficam o modelo, o service e uma pasta por **tela** (cada tela com component, html, scss e spec juntos). Nem toda feature tem listagem ou formulário — cria-se só as telas que existirem. **shared/** contém apenas o que é reutilizado entre páginas.

## Checklist – Nova feature (ex.: Orders)

Use este checklist e crie os itens na ordem indicada.

**Modelo e service**

- [ ] `pages/orders/order.model.ts`: interfaces (ex.: `Order`, `OrderCreateRequest`).
- [ ] `pages/orders/order.service.ts`: `@Injectable({ providedIn: 'root' })`, `inject(HttpClient)`, métodos que retornam `Observable<T>` (list, getById, create, update, delete). Usar `environment.apiBaseUrl` para base da API.

**Telas da feature (cada uma em sua pasta, tudo junto)**

- [ ] Uma pasta por tela em `pages/orders/` (ex.: `orders-list/`), com `*.component.ts`, `*.component.html`, `*.component.scss`, `*.component.spec.ts` na mesma pasta.
- [ ] Componente: `ChangeDetectionStrategy.OnPush`, `host: { class: 'app-orders-list' }`, `inject(OrderService)`, signals/computed conforme a tela. Template: `@if` / `@for`, `[class.x]` ou `[style.x]`, `track item.id` no `@for`.
- [ ] Se a tela for formulário: form reativo, `FormBuilder`, validações; helper opcional (validação/build request) na mesma pasta; diretivas compartilhadas (ex.: `appCurrencyMask`) quando aplicável.

**Rotas**

- [ ] Em `app.routes.ts`: uma rota por tela que existir na feature, com `canActivate: [authGuard]` quando necessário.

**Shared (somente se reutilizável)**

- [ ] Componente/diretiva/pipe em `shared/` apenas quando usado em mais de uma feature ou quando for UI genérica (ex.: page-header, loading).

## Padrões de código

**Componente standalone (sem `standalone: true` – é padrão no Angular 21)**

```typescript
import { ChangeDetectionStrategy, Component, inject, input, signal } from '@angular/core';

@Component({
  selector: 'app-page-header',
  changeDetection: ChangeDetectionStrategy.OnPush,
  host: { class: 'app-page-header' },
  imports: [RouterLink, NzBreadCrumbModule],
  templateUrl: './page-header.component.html',
  styleUrl: './page-header.component.scss'
})
export class PageHeaderComponent {
  title = input.required<string>();
  subtitle = input<string>();
  breadcrumb = input<BreadcrumbItem[]>([]);
}
```

**Service com HttpClient**

```typescript
@Injectable({ providedIn: 'root' })
export class ProductService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiBaseUrl}/api/products`;

  list(): Observable<Product[]> {
    return this.http.get<Product[]>(this.baseUrl);
  }
}
```

**Template – controle de fluxo e bindings**

```html
@if (loading()) {
  <nz-spin nzSimple></nz-spin>
} @else {
  @for (item of items(); track item.id) {
    <div [class.active]="item.isActive">{{ item.name }}</div>
  }
}
```

**Diretiva com signal input e host**

```typescript
@Directive({
  selector: '[appAutofocus]',
  host: {
    '(focus)': 'onFocus($event)'
  }
})
export class AutofocusDirective {
  readonly appAutofocus = input(true, { transform: booleanAttribute });
}
```

## Convenções

- **Componentes:** OnPush, `host: { class: 'app-<nome>' }`, signal `input()`/`output()` quando fizer sentido; evitar `@Input()`/`@Output()` em código novo.
- **Templates:** `@if`, `@for`, `@switch`; `track item.id` (ou estável) no `@for`; sem `ngClass`/`ngStyle`.
- **Serviços:** `inject()` em vez de constructor injection; `providedIn: 'root'` para serviços globais.
- **Rotas:** um arquivo `app.routes.ts`; guards em `shared/guards/`, importados nas rotas.
- **Nomes:** kebab-case para pastas e arquivos; prefixo `app` para seletores de componentes/diretivas do app.

## Tratamento de erros e loading

- Chamadas HTTP: usar `catchError`, `finalize`, `timeout` nos subscribes; mensagens via `NzMessageService` quando fizer sentido.
- Loading: signal `loading` no componente; `[nzLoading]="loading()"` ou overlay compartilhado via `LoadingService` quando for global.

## Recursos adicionais

- Estrutura detalhada e fluxo de dados: [reference.md](reference.md).
