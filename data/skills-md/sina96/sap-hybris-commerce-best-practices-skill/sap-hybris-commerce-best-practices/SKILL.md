---
name: sap-hybris-commerce-best-practices
description: When users ask about SAP Commerce Cloud (Hybris) best practices, provide actionable guidance, checklists, and examples.
---

# SAP Hybris Commerce Best Practices

Comprehensive development guidelines and best practices for SAP Commerce Cloud (formerly Hybris).
This skill covers the complete development lifecycle from data modeling to frontend and backoffice configuration.

## Version Context

- **SAP Commerce Cloud**: 2211+ (September 2025 update)
- **JDK**: 21
- **Spring Framework**: 6.2
- **Architecture**: Service Layer (Jalo layer deprecated)

## Quick Reference

### Core Concepts

- **Extension-based architecture**: modular design with custom extensions
- **Type System**: metadata-driven data model defined in items.xml
- **Service Layer**: primary API for business logic (ModelService, FlexibleSearchService)
- **ImpEx**: CSV-based data import/export tool
- **Spring Integration**: DI, AOP, and bean management

### Development Workflow

1. Define data model in `*-items.xml`
2. Run `ant clean all` to generate model classes
3. Perform system update to apply schema changes
4. Implement services with Spring DI
5. Create facades with DTOs for frontend
6. Build controllers for web/REST APIs
7. Create JSP views or use headless APIs
8. Configure Solr for search functionality
9. Write automated tests (unit + integration)

## Topics

### Backend Development

- [Code Conventions](./references/00-code-conventions.md) - SAP Commerce coding style and formatting rules
- [Java Development Guidelines](./references/01-java-guidelines.md) - Coding standards, Spring patterns, service layer
- [Create Extensions](./references/02-extensions.md) - Extension structure, types, and configuration
- [Define Data Types](./references/03-data-types.md) - items.xml structure, types, relations
- [Using ImpEx](./references/04-impex.md) - Data import/export syntax and patterns
- [Dynamic Attributes](./references/05-dynamic-attributes.md) - Computed attributes without DB storage
- [Services](./references/06-services.md) - Business logic implementation with Spring
- [Properties Configuration](./references/07-properties.md) - Externalize configuration
- [Events](./references/08-events.md) - Event-driven architecture patterns
- [Interceptors](./references/09-interceptors.md) - Model lifecycle hooks
- [Validation Framework](./references/10-validation.md) - Declarative validation constraints
- [Automated Testing](./references/11-testing.md) - Unit and integration testing
- [Code Quality](./references/12-code-quality.md) - SOLID principles, extensibility, upgradability

### Frontend Development

- [Facades](./references/13-facades.md) - Facade pattern, DTOs, converters
- [Controllers](./references/14-controllers.md) - Spring MVC and REST controllers
- [WCMS Components](./references/15-wcms-components.md) - CMS content management
- [JSP Tags](./references/16-jsp-tags.md) - Custom tag libraries
- [JSP Views](./references/17-jsp-views.md) - View templates with JSTL

### Search & Indexing

- [Solr Integration](./references/18-solr.md) - Search configuration, indexing, facets

### Background Processing

- [Tasks and CronJobs](./references/19-tasks-and-cronjobs.md) - Background task scheduling and execution

### Backoffice

- [Backoffice Configuration](./references/20-backoffice-configuration.md) - cockpitng/backoffice config patterns (editor area, list view, search, wizards)

## Common Patterns

### Service + Facade Pattern

```java
// Service (backend logic)
public interface ProductService {
	ProductModel findByCode(String code);
}

@Service
public class DefaultProductService implements ProductService {

	private final FlexibleSearchService flexibleSearchService;

	public DefaultProductService(final FlexibleSearchService flexibleSearchService) {
		this.flexibleSearchService = flexibleSearchService;
	}

	@Override
	public ProductModel findByCode(final String code) {
		// ...
		return null;
	}
}

// Facade (frontend API)
public interface ProductFacade {
	ProductData getProduct(String code);
}

@Service
public class DefaultProductFacade implements ProductFacade {

	private final ProductService productService;
	private final Converter<ProductModel, ProductData> converter;

	public DefaultProductFacade(final ProductService productService,
			final Converter<ProductModel, ProductData> converter) {
		this.productService = productService;
		this.converter = converter;
	}

	@Override
	public ProductData getProduct(final String code) {
		return converter.convert(productService.findByCode(code));
	}
}
```

### Model Lifecycle

```
Create -> InitDefaults -> Prepare -> Validate -> Save
Load   -> LoadInterceptor
Delete -> RemoveInterceptor
```

### Extension Dependencies

```
core -> facades -> storefront
     -> backoffice
     -> occ (REST API)
```

## Best Practices Summary

### DO

- Use Service Layer APIs (ModelService, FlexibleSearchService)
- Follow interface + implementation pattern
- Prefer constructor injection (Spring 6)
- Externalize configuration to properties files
- Write unit and integration tests
- Use facades with DTOs for frontend
- Validate input with interceptors or the validation framework
- Use ImpEx for data management
- Configure Solr for search functionality
- Follow SOLID principles

### DON'T

- Use Jalo layer directly (deprecated)
- Use field injection (`@Autowired` on fields)
- Hardcode configuration values
- Expose models directly to frontend
- Modify generated model classes
- Skip system update after items.xml changes
- Perform heavy operations in interceptors
- Use embedded Solr in production

## Quick Commands

```bash
# Build and generate models
ant clean all

# Run tests
ant alltests
ant unittests
ant integrationtests

# Solr management
ant startSolrServer
ant stopSolrServer

# Initialize/update system
ant initialize
ant updatesystem
```

## Resources

- SAP Help Portal (requires authentication)
- SAP Community (forums and blogs)
- Local HAC: `http://localhost:9001/hac`

---

Note: this skill is based on SAP Commerce Cloud 2211+ (September 2025). For earlier versions, some features and APIs may differ.
