---
name: easy-admin-bundle
version: 1.1.0
compatibility:
  easyadmin: "^4.0"
  php: ">=8.1"
  symfony: ">=5.4"
updated: 2026-02-23
description: "Rapid Symfony admin panel development with EasyAdminBundle. Capabilities: CRUD generation, dashboard creation, entity management, form customization, menu configuration, field configuration, action customization, filters, permissions, batch actions, custom themes, file uploads, image handling, associations, submenus, custom queries, event listeners. Use for: admin panels, backend interfaces, content management, data administration, CRUD operations, user management, product catalogs, blog administration, e-commerce backends. Triggers: easyadmin, symfony admin, crud, admin panel, dashboard, backend, entity crud, admin interface, symfony backend, easyadmin, easyadmin bundle, admin generator, backend panel"
allowed-tools: Bash(composer *, symfony *, php bin/console *), Read, Write, Edit, Glob, Grep
---

# EasyAdmin Bundle Skill

Build powerful Symfony admin panels quickly with EasyAdminBundle. This skill provides complete examples and patterns for creating production-ready admin interfaces.

> **Version:** This skill covers EasyAdminBundle 4.x (current stable)
> **Requirements:** PHP 8.1+, Symfony 5.4/6.x/7.x/8.x, Doctrine ORM
> **Official Docs:** https://github.com/EasyCorp/EasyAdminBundle/tree/4.x/doc
> **Repository:** https://github.com/EasyCorp/EasyAdminBundle
>
> **📚 Quick Reference:** See [API Reference](#api-reference) section for complete field types, actions, and CRUD configuration methods

## Quick Start

```bash
# Install EasyAdmin bundle
composer require easycorp/easyadmin-bundle

# Create a dashboard controller
php bin/console make:admin:dashboard

# Create CRUD controllers for your entities
php bin/console make:admin:crud
```

## Complete Dashboard Setup

### Basic Dashboard Controller

```php
// src/Controller/Admin/DashboardController.php
namespace App\Controller\Admin;

use App\Entity\User;
use App\Entity\Post;
use App\Entity\Category;
use App\Entity\Comment;
use EasyCorp\Bundle\EasyAdminBundle\Config\Dashboard;
use EasyCorp\Bundle\EasyAdminBundle\Config\MenuItem;
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractDashboardController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class DashboardController extends AbstractDashboardController
{
    #[Route('/admin', name: 'admin')]
    public function index(): Response
    {
        return $this->render('admin/dashboard.html.twig');
    }

    public function configureDashboard(): Dashboard
    {
        return Dashboard::new()
            ->setTitle('My Admin Panel')
            ->setFaviconPath('favicon.ico')
            ->setTranslationDomain('admin')
            ->setTextDirection('ltr')
            ->renderContentMaximized()
            ->renderSidebarMinimized()
            ->disableDarkMode();
    }

    public function configureMenuItems(): iterable
    {
        yield MenuItem::linkToDashboard('Dashboard', 'fa fa-home');

        yield MenuItem::section('Content');
        yield MenuItem::linkToCrud('Posts', 'fa fa-newspaper', Post::class);
        yield MenuItem::linkToCrud('Categories', 'fa fa-tags', Category::class);
        yield MenuItem::linkToCrud('Comments', 'fa fa-comments', Comment::class);

        yield MenuItem::section('Users');
        yield MenuItem::linkToCrud('Users', 'fa fa-user', User::class);

        yield MenuItem::section('External');
        yield MenuItem::linkToUrl('Homepage', 'fa fa-globe', '/');
        yield MenuItem::linkToLogout('Logout', 'fa fa-sign-out');
    }
}
```

### Dashboard with Submenus

```php
public function configureMenuItems(): iterable
{
    yield MenuItem::linkToDashboard('Dashboard', 'fa fa-home');

    // Submenu example
    yield MenuItem::subMenu('Content', 'fa fa-file')->setSubItems([
        MenuItem::linkToCrud('Posts', 'fa fa-newspaper', Post::class),
        MenuItem::linkToCrud('Pages', 'fa fa-file-text', Page::class),
        MenuItem::linkToCrud('Media', 'fa fa-images', Media::class),
    ]);

    yield MenuItem::subMenu('E-commerce', 'fa fa-shopping-cart')->setSubItems([
        MenuItem::linkToCrud('Products', 'fa fa-box', Product::class),
        MenuItem::linkToCrud('Orders', 'fa fa-shopping-bag', Order::class),
        MenuItem::linkToCrud('Customers', 'fa fa-users', Customer::class),
    ]);
}
```

## Field Types Reference

### Basic Fields

```php
use EasyCorp\Bundle\EasyAdminBundle\Field\TextField;
use EasyCorp\Bundle\EasyAdminBundle\Field\TextEditorField;
use EasyCorp\Bundle\EasyAdminBundle\Field\TextareaField;
use EasyCorp\Bundle\EasyAdminBundle\Field\NumberField;
use EasyCorp\Bundle\EasyAdminBundle\Field\IntegerField;
use EasyCorp\Bundle\EasyAdminBundle\Field\EmailField;
use EasyCorp\Bundle\EasyAdminBundle\Field\UrlField;
use EasyCorp\Bundle\EasyAdminBundle\Field\TelephoneField;

public function configureFields(string $pageName): iterable
{
    yield TextField::new('title')->setMaxLength(255);
    yield TextEditorField::new('content'); // Rich text editor
    yield TextareaField::new('description')->setMaxLength(500);
    yield NumberField::new('price')->setNumDecimals(2);
    yield IntegerField::new('quantity');
    yield EmailField::new('email');
    yield UrlField::new('website');
    yield TelephoneField::new('phone');
}
```

### Date and Time Fields

```php
use EasyCorp\Bundle\EasyAdminBundle\Field\DateField;
use EasyCorp\Bundle\EasyAdminBundle\Field\DateTimeField;
use EasyCorp\Bundle\EasyAdminBundle\Field\TimeField;

public function configureFields(string $pageName): iterable
{
    yield DateField::new('publishedAt')
        ->setFormat('dd/MM/yyyy');

    yield DateTimeField::new('createdAt')
        ->setFormat('dd/MM/yyyy HH:mm')
        ->hideOnForm();

    yield TimeField::new('openingTime')
        ->setFormat('HH:mm');
}
```

### Boolean and Choice Fields

```php
use EasyCorp\Bundle\EasyAdminBundle\Field\BooleanField;
use EasyCorp\Bundle\EasyAdminBundle\Field\ChoiceField;

public function configureFields(string $pageName): iterable
{
    yield BooleanField::new('isPublished')
        ->renderAsSwitch();

    yield ChoiceField::new('status')
        ->setChoices([
            'Draft' => 'draft',
            'Published' => 'published',
            'Archived' => 'archived',
        ])
        ->renderAsBadges([
            'draft' => 'warning',
            'published' => 'success',
            'archived' => 'secondary',
        ]);

    yield ChoiceField::new('roles')
        ->setChoices([
            'User' => 'ROLE_USER',
            'Editor' => 'ROLE_EDITOR',
            'Admin' => 'ROLE_ADMIN',
        ])
        ->allowMultipleChoices()
        ->renderExpanded(); // Show as checkboxes
}
```

### Association Fields

```php
use EasyCorp\Bundle\EasyAdminBundle\Field\AssociationField;

public function configureFields(string $pageName): iterable
{
    // Many-to-One
    yield AssociationField::new('category')
        ->setRequired(true);

    // One-to-Many / Many-to-Many
    yield AssociationField::new('tags')
        ->setFormTypeOptions([
            'by_reference' => false,
        ])
        ->autocomplete(); // Ajax autocomplete for large datasets

    // Custom query for association
    yield AssociationField::new('author')
        ->setQueryBuilder(
            fn (QueryBuilder $qb) => $qb
                ->andWhere('entity.isActive = :active')
                ->setParameter('active', true)
        );
}
```

### File and Image Fields

```php
use EasyCorp\Bundle\EasyAdminBundle\Field\ImageField;
use EasyCorp\Bundle\EasyAdminBundle\Field\FileField;

public function configureFields(string $pageName): iterable
{
    yield ImageField::new('thumbnail')
        ->setBasePath('uploads/images')
        ->setUploadDir('public/uploads/images')
        ->setUploadedFileNamePattern('[randomhash].[extension]')
        ->setRequired(false);

    yield ImageField::new('gallery')
        ->setBasePath('uploads/gallery')
        ->setUploadDir('public/uploads/gallery')
        ->setUploadedFileNamePattern('[slug]-[timestamp].[extension]')
        ->setFormTypeOptions(['multiple' => true]);

    yield FileField::new('attachment')
        ->setBasePath('uploads/files')
        ->setUploadDir('public/uploads/files');
}
```

### Money and Percent Fields

```php
use EasyCorp\Bundle\EasyAdminBundle\Field\MoneyField;
use EasyCorp\Bundle\EasyAdminBundle\Field\PercentField;

public function configureFields(string $pageName): iterable
{
    yield MoneyField::new('price')
        ->setCurrency('USD')
        ->setStoredAsCents(false);

    yield MoneyField::new('priceInCents')
        ->setCurrency('EUR')
        ->setStoredAsCents(true);

    yield PercentField::new('discount')
        ->setNumDecimals(2);
}
```

### Other Useful Fields

```php
use EasyCorp\Bundle\EasyAdminBundle\Field\SlugField;
use EasyCorp\Bundle\EasyAdminBundle\Field\ColorField;
use EasyCorp\Bundle\EasyAdminBundle\Field\CountryField;
use EasyCorp\Bundle\EasyAdminBundle\Field\LanguageField;
use EasyCorp\Bundle\EasyAdminBundle\Field\LocaleField;
use EasyCorp\Bundle\EasyAdminBundle\Field\TimezoneField;
use EasyCorp\Bundle\EasyAdminBundle\Field\CodeEditorField;

public function configureFields(string $pageName): iterable
{
    yield SlugField::new('slug')
        ->setTargetFieldName('title');

    yield ColorField::new('brandColor');

    yield CountryField::new('country');

    yield LanguageField::new('language');

    yield LocaleField::new('locale');

    yield TimezoneField::new('timezone');

    yield CodeEditorField::new('customCss')
        ->setLanguage('css')
        ->setNumOfRows(10);
}
```

## Complete CRUD Controller Examples

### User CRUD with All Features

```php
namespace App\Controller\Admin;

use App\Entity\User;
use EasyCorp\Bundle\EasyAdminBundle\Config\Action;
use EasyCorp\Bundle\EasyAdminBundle\Config\Actions;
use EasyCorp\Bundle\EasyAdminBundle\Config\Crud;
use EasyCorp\Bundle\EasyAdminBundle\Config\Filters;
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractCrudController;
use EasyCorp\Bundle\EasyAdminBundle\Field\ArrayField;
use EasyCorp\Bundle\EasyAdminBundle\Field\BooleanField;
use EasyCorp\Bundle\EasyAdminBundle\Field\DateTimeField;
use EasyCorp\Bundle\EasyAdminBundle\Field\EmailField;
use EasyCorp\Bundle\EasyAdminBundle\Field\IdField;
use EasyCorp\Bundle\EasyAdminBundle\Field\ImageField;
use EasyCorp\Bundle\EasyAdminBundle\Field\TextField;
use EasyCorp\Bundle\EasyAdminBundle\Filter\BooleanFilter;
use EasyCorp\Bundle\EasyAdminBundle\Filter\DateTimeFilter;

class UserCrudController extends AbstractCrudController
{
    public static function getEntityFqcn(): string
    {
        return User::class;
    }

    public function configureCrud(Crud $crud): Crud
    {
        return $crud
            ->setEntityLabelInSingular('User')
            ->setEntityLabelInPlural('Users')
            ->setPageTitle('index', 'User Management')
            ->setPageTitle('new', 'Create User')
            ->setPageTitle('edit', 'Edit %entity_label_singular%')
            ->setSearchFields(['username', 'email', 'firstName', 'lastName'])
            ->setDefaultSort(['createdAt' => 'DESC'])
            ->setPaginatorPageSize(30)
            ->setEntityPermission('ROLE_ADMIN');
    }

    public function configureFields(string $pageName): iterable
    {
        yield IdField::new('id')->hideOnForm();

        yield TextField::new('username')
            ->setColumns(6);

        yield EmailField::new('email')
            ->setColumns(6);

        yield TextField::new('firstName')
            ->setColumns(6)
            ->hideOnIndex();

        yield TextField::new('lastName')
            ->setColumns(6)
            ->hideOnIndex();

        yield ImageField::new('avatar')
            ->setBasePath('uploads/avatars')
            ->setUploadDir('public/uploads/avatars')
            ->setUploadedFileNamePattern('[slug]-[timestamp].[extension]')
            ->hideOnIndex();

        yield ArrayField::new('roles')
            ->hideOnIndex();

        yield BooleanField::new('isVerified')
            ->renderAsSwitch(false);

        yield BooleanField::new('isActive')
            ->renderAsSwitch(false);

        yield DateTimeField::new('createdAt')
            ->hideOnForm();

        yield DateTimeField::new('lastLoginAt')
            ->hideOnForm()
            ->hideOnIndex();
    }

    public function configureFilters(Filters $filters): Filters
    {
        return $filters
            ->add('username')
            ->add('email')
            ->add(BooleanFilter::new('isActive'))
            ->add(BooleanFilter::new('isVerified'))
            ->add(DateTimeFilter::new('createdAt'))
            ->add(DateTimeFilter::new('lastLoginAt'));
    }

    public function configureActions(Actions $actions): Actions
    {
        $impersonate = Action::new('impersonate', 'Impersonate')
            ->linkToCrudAction('impersonate')
            ->setCssClass('btn btn-warning')
            ->displayIf(fn (User $user) => $this->isGranted('ROLE_SUPER_ADMIN'));

        return $actions
            ->add(Crud::PAGE_INDEX, Action::DETAIL)
            ->add(Crud::PAGE_INDEX, $impersonate)
            ->update(Crud::PAGE_INDEX, Action::DELETE, function (Action $action) {
                return $action->displayIf(fn (User $user) => $user->getId() !== $this->getUser()->getId());
            });
    }
}
```

### Product CRUD with Categories and Images

```php
namespace App\Controller\Admin;

use App\Entity\Product;
use EasyCorp\Bundle\EasyAdminBundle\Config\Crud;
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractCrudController;
use EasyCorp\Bundle\EasyAdminBundle\Field\AssociationField;
use EasyCorp\Bundle\EasyAdminBundle\Field\BooleanField;
use EasyCorp\Bundle\EasyAdminBundle\Field\DateTimeField;
use EasyCorp\Bundle\EasyAdminBundle\Field\IdField;
use EasyCorp\Bundle\EasyAdminBundle\Field\ImageField;
use EasyCorp\Bundle\EasyAdminBundle\Field\IntegerField;
use EasyCorp\Bundle\EasyAdminBundle\Field\MoneyField;
use EasyCorp\Bundle\EasyAdminBundle\Field\SlugField;
use EasyCorp\Bundle\EasyAdminBundle\Field\TextEditorField;
use EasyCorp\Bundle\EasyAdminBundle\Field\TextField;

class ProductCrudController extends AbstractCrudController
{
    public static function getEntityFqcn(): string
    {
        return Product::class;
    }

    public function configureCrud(Crud $crud): Crud
    {
        return $crud
            ->setEntityLabelInSingular('Product')
            ->setEntityLabelInPlural('Products')
            ->setSearchFields(['name', 'sku', 'description'])
            ->setDefaultSort(['createdAt' => 'DESC']);
    }

    public function configureFields(string $pageName): iterable
    {
        yield IdField::new('id')->onlyOnIndex();

        yield TextField::new('name')
            ->setColumns(8);

        yield SlugField::new('slug')
            ->setTargetFieldName('name')
            ->setColumns(4)
            ->hideOnIndex();

        yield TextField::new('sku')
            ->setColumns(6);

        yield MoneyField::new('price')
            ->setCurrency('USD')
            ->setColumns(6);

        yield IntegerField::new('stock')
            ->setColumns(6);

        yield AssociationField::new('category')
            ->setColumns(6)
            ->autocomplete();

        yield AssociationField::new('tags')
            ->hideOnIndex()
            ->autocomplete();

        yield TextEditorField::new('description')
            ->hideOnIndex();

        yield ImageField::new('image')
            ->setBasePath('uploads/products')
            ->setUploadDir('public/uploads/products')
            ->setUploadedFileNamePattern('[slug]-[timestamp].[extension]');

        yield BooleanField::new('isFeatured')
            ->renderAsSwitch(false);

        yield BooleanField::new('isActive')
            ->renderAsSwitch(false);

        yield DateTimeField::new('createdAt')
            ->hideOnForm();
    }
}
```

### Blog Post CRUD with Rich Content

```php
namespace App\Controller\Admin;

use App\Entity\Post;
use EasyCorp\Bundle\EasyAdminBundle\Config\Crud;
use EasyCorp\Bundle\EasyAdminBundle\Controller\AbstractCrudController;
use EasyCorp\Bundle\EasyAdminBundle\Field\AssociationField;
use EasyCorp\Bundle\EasyAdminBundle\Field\ChoiceField;
use EasyCorp\Bundle\EasyAdminBundle\Field\DateTimeField;
use EasyCorp\Bundle\EasyAdminBundle\Field\IdField;
use EasyCorp\Bundle\EasyAdminBundle\Field\ImageField;
use EasyCorp\Bundle\EasyAdminBundle\Field\SlugField;
use EasyCorp\Bundle\EasyAdminBundle\Field\TextEditorField;
use EasyCorp\Bundle\EasyAdminBundle\Field\TextField;

class PostCrudController extends AbstractCrudController
{
    public static function getEntityFqcn(): string
    {
        return Post::class;
    }

    public function configureCrud(Crud $crud): Crud
    {
        return $crud
            ->setEntityLabelInSingular('Post')
            ->setEntityLabelInPlural('Blog Posts')
            ->setSearchFields(['title', 'content', 'excerpt'])
            ->setDefaultSort(['publishedAt' => 'DESC']);
    }

    public function configureFields(string $pageName): iterable
    {
        yield IdField::new('id')->onlyOnIndex();

        yield TextField::new('title');

        yield SlugField::new('slug')
            ->setTargetFieldName('title')
            ->hideOnIndex();

        yield TextField::new('excerpt')
            ->setMaxLength(200)
            ->hideOnIndex();

        yield TextEditorField::new('content')
            ->hideOnIndex();

        yield ImageField::new('featuredImage')
            ->setBasePath('uploads/posts')
            ->setUploadDir('public/uploads/posts');

        yield AssociationField::new('author')
            ->autocomplete();

        yield AssociationField::new('category');

        yield AssociationField::new('tags')
            ->hideOnIndex()
            ->autocomplete();

        yield ChoiceField::new('status')
            ->setChoices([
                'Draft' => 'draft',
                'Published' => 'published',
                'Archived' => 'archived',
            ])
            ->renderAsBadges([
                'draft' => 'warning',
                'published' => 'success',
                'archived' => 'secondary',
            ]);

        yield DateTimeField::new('publishedAt')
            ->hideOnIndex();

        yield DateTimeField::new('createdAt')
            ->hideOnForm();

        yield DateTimeField::new('updatedAt')
            ->hideOnForm()
            ->hideOnIndex();
    }
}
```

## Custom Actions

### Add Custom Action to CRUD

```php
use EasyCorp\Bundle\EasyAdminBundle\Config\Action;
use EasyCorp\Bundle\EasyAdminBundle\Config\Actions;
use EasyCorp\Bundle\EasyAdminBundle\Config\Crud;
use Symfony\Component\HttpFoundation\Response;

class ProductCrudController extends AbstractCrudController
{
    public function configureActions(Actions $actions): Actions
    {
        // Create custom action
        $exportAction = Action::new('export', 'Export CSV')
            ->linkToCrudAction('exportCsv')
            ->setCssClass('btn btn-success')
            ->createAsGlobalAction(); // Shows in index page header

        $duplicateAction = Action::new('duplicate', 'Duplicate')
            ->linkToCrudAction('duplicateProduct')
            ->setCssClass('btn btn-info');

        return $actions
            ->add(Crud::PAGE_INDEX, $exportAction)
            ->add(Crud::PAGE_DETAIL, $duplicateAction)
            ->add(Crud::PAGE_INDEX, Action::DETAIL)
            ->reorder(Crud::PAGE_INDEX, [Action::DETAIL, Action::EDIT, 'duplicate', Action::DELETE]);
    }

    public function exportCsv(): Response
    {
        $products = $this->entityManager->getRepository(Product::class)->findAll();

        // Generate CSV content
        $csv = "ID,Name,SKU,Price\n";
        foreach ($products as $product) {
            $csv .= sprintf("%d,%s,%s,%.2f\n",
                $product->getId(),
                $product->getName(),
                $product->getSku(),
                $product->getPrice()
            );
        }

        return new Response($csv, 200, [
            'Content-Type' => 'text/csv',
            'Content-Disposition' => 'attachment; filename="products.csv"',
        ]);
    }

    public function duplicateProduct(AdminContext $context): Response
    {
        $product = $context->getEntity()->getInstance();

        $newProduct = clone $product;
        $newProduct->setName($product->getName() . ' (Copy)');
        $newProduct->setSku($product->getSku() . '-copy');

        $this->entityManager->persist($newProduct);
        $this->entityManager->flush();

        $this->addFlash('success', 'Product duplicated successfully');

        return $this->redirect($context->getReferrer());
    }
}
```

### Batch Actions

```php
use EasyCorp\Bundle\EasyAdminBundle\Config\Action;
use EasyCorp\Bundle\EasyAdminBundle\Config\Actions;

public function configureActions(Actions $actions): Actions
{
    $batchPublish = Action::new('batchPublish', 'Publish selected')
        ->linkToCrudAction('batchPublish')
        ->addCssClass('btn btn-success')
        ->setIcon('fa fa-check');

    return $actions
        ->addBatchAction($batchPublish);
}

public function batchPublish(BatchActionDto $batchActionDto): Response
{
    $entityManager = $this->entityManager;

    foreach ($batchActionDto->getEntityIds() as $id) {
        $post = $entityManager->find(Post::class, $id);
        if ($post) {
            $post->setStatus('published');
            $post->setPublishedAt(new \DateTime());
        }
    }

    $entityManager->flush();

    $this->addFlash('success', sprintf('Published %d posts', count($batchActionDto->getEntityIds())));

    return $this->redirect($batchActionDto->getReferrerUrl());
}
```

## Advanced Configurations

### Conditional Field Display

```php
public function configureFields(string $pageName): iterable
{
    yield TextField::new('title');

    // Show only on index page
    yield TextField::new('summary')->onlyOnIndex();

    // Show only on forms (new/edit)
    yield TextEditorField::new('content')->onlyOnForms();

    // Show only on detail page
    yield TextField::new('fullDetails')->onlyOnDetail();

    // Hide on specific pages
    yield DateTimeField::new('createdAt')
        ->hideOnForm()
        ->hideOnIndex();

    // Conditional display based on context
    if (Crud::PAGE_EDIT === $pageName) {
        yield DateTimeField::new('updatedAt')->setFormTypeOptions(['disabled' => true]);
    }
}
```

### Custom Form Layouts

```php
use EasyCorp\Bundle\EasyAdminBundle\Field\FormField;

public function configureFields(string $pageName): iterable
{
    yield FormField::addPanel('Basic Information');
    yield TextField::new('name');
    yield TextField::new('sku');

    yield FormField::addPanel('Pricing')->setIcon('fa fa-dollar-sign');
    yield MoneyField::new('price')->setCurrency('USD');
    yield MoneyField::new('costPrice')->setCurrency('USD');
    yield PercentField::new('taxRate');

    yield FormField::addPanel('Inventory');
    yield IntegerField::new('stock');
    yield IntegerField::new('minStock');
    yield BooleanField::new('trackInventory');

    yield FormField::addPanel('SEO')->setHelp('Search engine optimization settings');
    yield TextField::new('metaTitle');
    yield TextareaField::new('metaDescription');
}
```

### Security and Permissions

```php
use EasyCorp\Bundle\EasyAdminBundle\Config\Crud;

public function configureCrud(Crud $crud): Crud
{
    return $crud
        ->setEntityPermission('ROLE_ADMIN') // Required role for all operations
        ->setEntityLabelInSingular('Product')
        ->setEntityLabelInPlural('Products');
}

public function configureActions(Actions $actions): Actions
{
    return $actions
        // Only super admins can delete
        ->setPermission(Action::DELETE, 'ROLE_SUPER_ADMIN')
        // Conditional permissions
        ->update(Crud::PAGE_INDEX, Action::EDIT, function (Action $action) {
            return $action->displayIf(function (Product $product) {
                return $this->isGranted('ROLE_EDITOR') || $product->getAuthor() === $this->getUser();
            });
        });
}
```

### Custom Queries and Filters

```php
use Doctrine\ORM\QueryBuilder;
use EasyCorp\Bundle\EasyAdminBundle\Collection\FieldCollection;
use EasyCorp\Bundle\EasyAdminBundle\Collection\FilterCollection;
use EasyCorp\Bundle\EasyAdminBundle\Dto\EntityDto;
use EasyCorp\Bundle\EasyAdminBundle\Dto\SearchDto;

public function createIndexQueryBuilder(SearchDto $searchDto, EntityDto $entityDto, FieldCollection $fields, FilterCollection $filters): QueryBuilder
{
    $qb = parent::createIndexQueryBuilder($searchDto, $entityDto, $fields, $filters);

    // Only show active products
    $qb->andWhere('entity.isActive = :active')
       ->setParameter('active', true);

    // Only show products from current user's store
    if (!$this->isGranted('ROLE_ADMIN')) {
        $qb->andWhere('entity.store = :store')
           ->setParameter('store', $this->getUser()->getStore());
    }

    return $qb;
}
```

## Event Listeners and Hooks

### Modify Entity Before Persist

```php
use EasyCorp\Bundle\EasyAdminBundle\Event\BeforeEntityPersistedEvent;
use EasyCorp\Bundle\EasyAdminBundle\Event\BeforeEntityUpdatedEvent;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class ProductSubscriber implements EventSubscriberInterface
{
    public static function getSubscribedEvents(): array
    {
        return [
            BeforeEntityPersistedEvent::class => ['setCreatedAt'],
            BeforeEntityUpdatedEvent::class => ['setUpdatedAt'],
        ];
    }

    public function setCreatedAt(BeforeEntityPersistedEvent $event): void
    {
        $entity = $event->getEntityInstance();

        if ($entity instanceof Product) {
            $entity->setCreatedAt(new \DateTime());
        }
    }

    public function setUpdatedAt(BeforeEntityUpdatedEvent $event): void
    {
        $entity = $event->getEntityInstance();

        if ($entity instanceof Product) {
            $entity->setUpdatedAt(new \DateTime());
        }
    }
}
```

## Configuration Files

### Route Configuration

```yaml
# config/routes.yaml
admin:
    resource: App\Controller\Admin\DashboardController
    type: easyadmin
    prefix: /admin
```

### Security Configuration

```yaml
# config/packages/security.yaml
security:
    # ... other config

    access_control:
        - { path: ^/admin/login, roles: PUBLIC_ACCESS }
        - { path: ^/admin, roles: ROLE_ADMIN }

    role_hierarchy:
        ROLE_EDITOR: ROLE_USER
        ROLE_ADMIN: ROLE_EDITOR
        ROLE_SUPER_ADMIN: ROLE_ADMIN
```

### EasyAdmin Configuration

```yaml
# config/packages/easyadmin.yaml
easy_admin:
    site_name: 'My Admin Panel'

    formats:
        date: 'd/m/Y'
        time: 'H:i'
        datetime: 'd/m/Y H:i:s'

    design:
        brand_color: '#1976D2'
        menu:
            - { label: 'Dashboard', icon: 'fa fa-home', route: 'admin' }

    # Custom assets
    assets:
        css:
            - 'css/admin.css'
        js:
            - 'js/admin.js'
```

## Troubleshooting

### Routes Not Found
```bash
# Clear cache
php bin/console cache:clear

# Verify routes
php bin/console debug:router | grep admin
```

### Images Not Displaying
Ensure your public directory structure matches:
```
public/
  uploads/
    images/
    products/
    avatars/
```

### Association Fields Empty
Add `by_reference => false` for collections:
```php
yield AssociationField::new('tags')
    ->setFormTypeOptions(['by_reference' => false]);
```

### Autocomplete Not Working
Install and configure autocomplete:
```bash
composer require symfony/ux-autocomplete
php bin/console importmap:install
```

## Performance Tips

1. **Use pagination** - Keep default page size reasonable (20-50 items)
2. **Limit search fields** - Only include fields that need to be searchable
3. **Use autocomplete for associations** - Especially with large datasets
4. **Disable unnecessary features** - Hide detail pages if not needed
5. **Cache queries** - Use query result caching for complex filters

## Common Patterns

### Multi-Tenant CRUD
```php
public function createIndexQueryBuilder(SearchDto $searchDto, EntityDto $entityDto, FieldCollection $fields, FilterCollection $filters): QueryBuilder
{
    $qb = parent::createIndexQueryBuilder($searchDto, $entityDto, $fields, $filters);
    $qb->andWhere('entity.tenant = :tenant')
       ->setParameter('tenant', $this->getUser()->getTenant());
    return $qb;
}

public function persistEntity(EntityManagerInterface $em, $entityInstance): void
{
    $entityInstance->setTenant($this->getUser()->getTenant());
    parent::persistEntity($em, $entityInstance);
}
```

### Soft Delete Integration
```php
use Doctrine\ORM\QueryBuilder;

public function createIndexQueryBuilder(...): QueryBuilder
{
    $qb = parent::createIndexQueryBuilder(...);
    $qb->andWhere('entity.deletedAt IS NULL');
    return $qb;
}
```

### Audit Trail
```php
public function updateEntity(EntityManagerInterface $em, $entityInstance): void
{
    $entityInstance->setUpdatedBy($this->getUser());
    $entityInstance->setUpdatedAt(new \DateTime());
    parent::updateEntity($em, $entityInstance);
}
```

## Requirements

- **PHP:** 8.1 or higher
- **Symfony:** 5.4, 6.x, 7.x, or 8.x
- **Doctrine ORM:** Required for entity management
- **Twig:** Template engine

## Installation

```bash
# Install bundle (version 4.x)
composer require easycorp/easyadmin-bundle

# Optional: Install UX components for enhanced features
composer require symfony/ux-autocomplete

# Generate dashboard
php bin/console make:admin:dashboard

# Generate CRUD controllers
php bin/console make:admin:crud
```

## API Reference

Complete API reference for quick lookup. See files in `references/` directory:

### [📋 Fields](references/fields.md)
Complete list of all 31 field types with their configuration methods:
- **Common Methods**: hideOnIndex(), onlyOnForms(), setColumns(), setRequired(), etc.
- **Field Types**: TextField, AssociationField, ImageField, MoneyField, DateTimeField, BooleanField, ChoiceField, and 24 more
- **Form Layout**: FormField panels, tabs, columns, rows
- **Doctrine Mappings**: Type to field mappings

### [⚡ Actions](references/actions.md)
Actions API and configuration methods:
- **Built-in Actions**: INDEX, DETAIL, EDIT, NEW, DELETE, SAVE_AND_RETURN, etc.
- **Configuration**: add(), remove(), update(), disable(), setPermission(), reorder()
- **Custom Actions**: linkToCrudAction(), linkToRoute(), linkToUrl()
- **Batch Actions**: addBatchAction(), BatchActionDto usage

### [🔧 CRUD](references/crud.md)
CRUD controller configuration and lifecycle methods:
- **configureCrud()**: setEntityLabelInSingular(), setSearchFields(), setDefaultSort(), setPaginatorPageSize(), etc.
- **Query Builders**: createIndexQueryBuilder(), createEditQueryBuilder(), createNewQueryBuilder()
- **Lifecycle**: createEntity(), persistEntity(), updateEntity(), deleteEntity()
- **Routes & Context**: AdminContext, generateUrl(), getReferrer()

## Official Documentation

### Main Documentation
- **Repository:** https://github.com/EasyCorp/EasyAdminBundle
- **Documentation (4.x):** https://github.com/EasyCorp/EasyAdminBundle/tree/4.x/doc
- **Symfony Docs:** https://symfony.com/bundles/EasyAdminBundle/current/index.html

### Key Documentation Files
- **[CRUD Operations](https://github.com/EasyCorp/EasyAdminBundle/blob/4.x/doc/crud.rst)** - Complete CRUD configuration
- **[Dashboard](https://github.com/EasyCorp/EasyAdminBundle/blob/4.x/doc/dashboards.rst)** - Dashboard setup and configuration
- **[Fields Reference](https://github.com/EasyCorp/EasyAdminBundle/blob/4.x/doc/fields.rst)** - All available field types
- **[Actions](https://github.com/EasyCorp/EasyAdminBundle/blob/4.x/doc/actions.rst)** - Custom actions and batch operations
- **[Filters](https://github.com/EasyCorp/EasyAdminBundle/blob/4.x/doc/filters.rst)** - Filtering configuration
- **[Security](https://github.com/EasyCorp/EasyAdminBundle/blob/4.x/doc/security.rst)** - Permission and security setup
- **[Events](https://github.com/EasyCorp/EasyAdminBundle/blob/4.x/doc/events.rst)** - Event listeners and hooks
- **[Design](https://github.com/EasyCorp/EasyAdminBundle/blob/4.x/doc/design.rst)** - Customizing the UI
- **[Upgrade Guide](https://github.com/EasyCorp/EasyAdminBundle/blob/4.x/doc/upgrade.rst)** - Migration between versions

### Getting Latest Information

```bash
# Clone the repository to browse documentation locally
git clone https://github.com/EasyCorp/EasyAdminBundle.git
cd EasyAdminBundle

# Switch to 4.x branch
git checkout 4.x

# View documentation
cd doc
ls -la  # List all documentation files

# Read specific documentation
cat fields.rst
cat crud.rst
cat dashboards.rst
```

### Checking for Updates

```bash
# Check installed version
composer show easycorp/easyadmin-bundle

# Update to latest 4.x version
composer update easycorp/easyadmin-bundle

# Check for newer versions
composer outdated easycorp/easyadmin-bundle
```

### Version Notes

- **4.x (Current Stable):** Production ready, actively maintained
- **5.x (Beta):** In development, use for testing only
- This skill is based on 4.x patterns and syntax

### Community Resources

- **GitHub Issues:** https://github.com/EasyCorp/EasyAdminBundle/issues
- **GitHub Discussions:** https://github.com/EasyCorp/EasyAdminBundle/discussions
- **Symfony Community:** https://symfony.com/community
