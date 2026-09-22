---
name: packs-guide
description: Use when the user asks about packs, how automating AI photoshoots works or help about creating photoshoots. This product has two different target personas — Creative artists and directors who create packs and are AI savvy, and end users who want to use packs to create images but are not AI savvy. For the first group, focus on how to create packs, how to write good prompt templates, and how to create references. For the second group, focus on how to choose packs, how to upload reference images, and how to generate images from packs.
---

# Astria Packs Guide

## What Are Packs?
Packs are themed collections of prompt templates for generating consistent, professional images. Each pack contains curated prompts for a specific use case (headshots, fashion, products, etc.).

> **"Pack" = "Template".** "Template" is the label used in the GUI; "pack" is the term used in the API, CLI, and URLs (`/p/:pack-slug`). They are interchangeable — when a user says "template" they mean a pack. (Not to be confused with the *prompt templates* — the individual prompts — that a pack contains.)

Users upload reference images, then the pack's prompt templates generate images in the pack's theme using that reference.

## How Packs are used
1. User selects a pack (e.g. "Corporate Headshots")
2. User uploads reference images (shirt, shoes, dress, photos of themselves, product, pet, etc.)
3. A reference is created
4. The pack's prompt templates are automatically filled in with the reference
5. Generated images appear automatically


## How to create packs
1. Generate a few prompts with the same references (i.e: same man/woman or same shirt/shoes/dress) 
2. Once the user is happy about them - add them to a pack with a clear name and description
3. Once added - suggest navigation to the pack page /p/:pack-slug so the user can easily find it and use it again

## Publicly Available Packs by Category
Used for recommending users packs based on their needs and guiding them to the right pack for their use case.

### Fashion — Apparel
| Pack Slug | Category | Gender Support |
|-----------|----------|---------------|
| basic-shirt | Shirts | girl |
| sport-shirt-2 | Shirts | man |
| sweater-lookbook | Shirts/Sweaters | woman, product |
| basic-pants2 | Pants | woman |
| basic-jacket-men | Jackets | man |
| sport-jacket | Jackets | — |

### Fashion — Footwear
| Pack Slug | Category | Gender Support |
|-----------|----------|---------------|
| shoes-pack-shots | Shoes (product only) | product |
| casual-shoes | Casual Shoes | woman, product |
| studio-shoes-collection | Studio Shoes | woman, product |
| sport-shoes | Sport Shoes | boy |
| outdoors-trekking | Boots/Trekking | man, product |
| modern-flats | Flats | — |
| men-s-leather-shoes | Leather Shoes | — |
| sandals | Sandals | woman, product |

### Fashion — Jewelry & Accessories
| Pack Slug | Category | Gender Support |
|-----------|----------|---------------|
| jewelry-ring | Rings | product/hand |
| jewelry-necklace | Necklaces | woman, product |
| necklace | Necklaces | product |
| jewelry-earring | Earrings | woman, product |
| glasses | Glasses | woman, man |
| sunglasses | Sunglasses | woman, man |
| womens-bag | Bags | — |

### Portrait — Professional
| Pack Slug | Category | Gender Support |
|-----------|----------|---------------|
| corporate-headshots | Corporate | woman, man |
| partners-headshots | Partners/Team | woman, man |
| realtor | Real Estate | woman, man |
| md-doctor | Medical | woman, man |
| speaker | Speaker/Events | — |

### Portrait — Personal
| Pack Slug | Category | Gender Support |
|-----------|----------|---------------|
| natural-headshots | Natural | woman |
| dating | Dating Profile | woman, man |
| photoshoot | General Photo | woman, man, girl, boy |
| glamour-shot | Glamour | woman, man |

### Portrait — Events
| Pack Slug | Category | Gender Support |
|-----------|----------|---------------|
| birthday-party-save-the-date | Birthday (adults) | woman, man |
| kids-bday | Birthday (kids) | girl, boy |
| halloween | Halloween | — |
| halloween-2024 | Halloween 2024 | — |
| kids-halloween | Kids Halloween | — |
| christmas-sweater | Christmas | — |

### Creative & Themed
| Pack Slug | Category |
|-----------|----------|
| cyberpunk | Cyberpunk style |
| vikings | Viking themed |
| barbie | Barbie themed |
| game-of-thrones-style | GoT themed |
| wednesday-adams | Wednesday Addams |
| mythical-creatures | Fantasy creatures |
| wrestlemania | Wrestling themed |
| red-carpet | Red carpet style |
| annie-leibovitz | Annie Leibovitz style |
| famous-photographers | Photographer styles |
| americana | Americana style |
| botanical-illustration | Botanical art |
| whimsical-wes-anderson | Wes Anderson style |
| korean-chic-han | Korean fashion |
| tattoos | Tattoo designs |
| eurovision | Eurovision themed |
| j-crew | J.Crew style |
| youtube-thumbnail-reaction | YouTube thumbnails |
| inspiration-board | Mood/inspiration boards |

### Pets
| Pack Slug | Category |
|-----------|----------|
| dog-art | Dog portraits/art |
| cat-meowgic | Cat portraits/art |
| everyday-onesies | Pet onesies |
