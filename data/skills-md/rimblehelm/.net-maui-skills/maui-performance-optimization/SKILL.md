---
name: maui-performance-optimization
description: A brief description of what this skill does
---

# .NET MAUI — Performance Optimization Skill

## Purpose

This skill provides agents with best practices, patterns, and diagnostics for improving performance in .NET MAUI applications. It covers startup time, layout efficiency, memory usage, rendering performance, compiled bindings, AOT, image optimization, and responsiveness across platforms.

The goal is to ensure that all generated MAUI code is fast, efficient, and production-ready.

## Core Principles

1. **Minimize layout complexity**
   Avoid deep nesting and prefer efficient containers like Grid.
2. **Use compiled bindings**
   Reduce reflection overhead and improve rendering speed.
3. **Optimize startup**
   Defer heavy work, preload only what’s necessary, and use AOT where appropriate.
4. **Reduce memory pressure**
   Dispose resources, unload pages, and avoid large in-memory objects.
5. **Optimize images**
   Use correct resolutions, caching, and vector assets when possible.
6. **Measure, don’t guess**
   Use profiling tools and performance diagnostics.

## Key Optimization Areas

- Startup time
- XAML rendering
- Navigation performance
- Memory usage
- Image loading
- Threading and async patterns
- AOT compilation
- Resource cleanup

## Agent Usage Guidelines

- When generating XAML, apply compiled bindings and avoid unnecessary nesting.
- When generating services, ensure async methods are properly awaited.
- When asked to “improve performance,” apply rules from this skill before others.
- When generating image-heavy UI, use caching and correct image formats.
- When generating navigation code, avoid creating multiple page instances unnecessarily.

## Out of Scope

- UI design (covered in `maui-ui-best-practices`)
- Authentication (covered in `maui-authentication`)
- Database performance (covered in `maui-data-storage`)
