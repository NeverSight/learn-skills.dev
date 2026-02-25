---
name: recipe-card-creator
description: Formatted digital recipe card generation with ingredient scaling, nutritional information, and organized collections. Use when creating recipe cards, meal plans, grocery lists, or recipe collections.
---

# Recipe Card Creator

Comprehensive frameworks for structured recipe creation, ingredient management, meal planning, and recipe collection organization.

## Recipe Card Format Standards

### Standard Recipe Card Template

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [RECIPE TITLE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Prep Time: XX min | Cook Time: XX min | Total: XX min
Servings: X       | Difficulty: [1-5 stars]
Cuisine: [Type]   | Course: [Meal type]

DIETARY: [Vegan] [GF] [DF] [NF] [Vegetarian] [Keto] [Paleo]

━━ INGREDIENTS ━━━━━━━━━━━━━━━━━━━━━━━━━

[Group Name (if applicable)]
  [ ] 2 cups     all-purpose flour
  [ ] 1 tsp      baking powder
  [ ] 1/2 tsp    salt

[Group Name]
  [ ] 3 large    eggs, room temperature
  [ ] 1 cup      whole milk
  [ ] 2 tbsp     unsalted butter, melted

━━ INSTRUCTIONS ━━━━━━━━━━━━━━━━━━━━━━━━

1. [Action verb] [what to do] [how to do it].
   Tip: [Optional helpful note]

2. [Action verb] [what to do] [until what result].
   ⏱ [Time indicator if applicable]

3. [Action verb] [what to do].

━━ NOTES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Storage: [How to store and for how long]
Make Ahead: [What can be prepped in advance]
Variations: [Alternative versions or substitutions]
Source: [Original recipe attribution]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Instruction Writing Guidelines

| Principle | Example Good | Example Bad |
|-----------|-------------|-------------|
| **Start with verb** | "Whisk the flour and salt" | "The flour and salt should be whisked" |
| **Specify doneness** | "Saute until golden, about 5 min" | "Saute the onions" |
| **Include visual cues** | "Stir until thick enough to coat a spoon" | "Stir until thick" |
| **Group by station** | "Dry ingredients, then wet ingredients" | Random order |
| **Note timing** | "Bake 25-30 min until top springs back" | "Bake until done" |

### Difficulty Rating System

| Rating | Label | Description |
|--------|-------|-------------|
| 1 | Beginner | No special skills, simple techniques, common ingredients |
| 2 | Easy | Basic cooking skills, straightforward timing |
| 3 | Intermediate | Some technique required, multi-step, timing-sensitive |
| 4 | Advanced | Technical skills, precision required, complex assembly |
| 5 | Expert | Professional techniques, specialty equipment, extensive prep |

## Ingredient Scaling

### Scaling Calculation Rules

```
SCALING FORMULA:
  Scaled amount = Original amount x (Target servings / Original servings)

SCALING FACTOR TABLE:
  Half (0.5x):    Divide all by 2
  Double (2x):    Multiply all by 2
  Triple (3x):    Multiply all by 3
  Custom (Nx):    Multiply all by (target / original)

SPECIAL SCALING RULES:
  Eggs: Round to nearest whole (1.5 → 2 eggs)
  Yeast: Scale by 75% of factor (doubling? use 1.75x yeast, not 2x)
  Salt: Scale by 80-90% of factor (taste and adjust)
  Baking powder/soda: Scale by 90% of factor for >2x
  Spices: Scale by 75% of factor for >2x (intensify gradually)
  Cooking oil (for frying): Do not scale — use enough to cover
  Pan sauces/glazes: Scale by 50-75% when doubling
```

### Common Scaling Conversions

| Original | Half | Double | Triple |
|----------|------|--------|--------|
| 1/4 cup | 2 tbsp | 1/2 cup | 3/4 cup |
| 1/3 cup | 2 tbsp + 2 tsp | 2/3 cup | 1 cup |
| 1/2 cup | 1/4 cup | 1 cup | 1-1/2 cups |
| 3/4 cup | 6 tbsp | 1-1/2 cups | 2-1/4 cups |
| 1 cup | 1/2 cup | 2 cups | 3 cups |
| 1 tbsp | 1-1/2 tsp | 2 tbsp | 3 tbsp |
| 1 tsp | 1/2 tsp | 2 tsp | 1 tbsp |

### Pan Size Adjustment for Scaling

| Original Pan | For 1.5x | For 2x |
|-------------|----------|--------|
| 8" round | 9" round | 10" round or 2x 8" |
| 9x13" baking dish | — | Sheet pan (18x13") |
| 8x8" square | 9x9" square | 9x13" |
| 9" pie plate | 10" pie plate | 2x 9" |
| 12-muffin tin | 18-muffin | 2x 12-muffin |

## Measurement Conversions

### Volume Conversions

| US Customary | Metric | Tablespoons | Teaspoons |
|-------------|--------|-------------|-----------|
| 1 cup | 240 ml | 16 tbsp | 48 tsp |
| 3/4 cup | 180 ml | 12 tbsp | 36 tsp |
| 2/3 cup | 160 ml | 10 tbsp + 2 tsp | 32 tsp |
| 1/2 cup | 120 ml | 8 tbsp | 24 tsp |
| 1/3 cup | 80 ml | 5 tbsp + 1 tsp | 16 tsp |
| 1/4 cup | 60 ml | 4 tbsp | 12 tsp |
| 1 tbsp | 15 ml | 1 tbsp | 3 tsp |
| 1 tsp | 5 ml | 1/3 tbsp | 1 tsp |

### Weight Conversions

| US | Metric |
|----|--------|
| 1 oz | 28 g |
| 4 oz (1/4 lb) | 113 g |
| 8 oz (1/2 lb) | 227 g |
| 12 oz (3/4 lb) | 340 g |
| 16 oz (1 lb) | 454 g |

### Temperature Conversions

| Fahrenheit | Celsius | Gas Mark | Description |
|-----------|---------|----------|-------------|
| 250 F | 120 C | 1/2 | Very low |
| 300 F | 150 C | 2 | Low |
| 325 F | 165 C | 3 | Moderate low |
| 350 F | 175 C | 4 | Moderate |
| 375 F | 190 C | 5 | Moderate high |
| 400 F | 200 C | 6 | Hot |
| 425 F | 220 C | 7 | Hot |
| 450 F | 230 C | 8 | Very hot |
| 475 F | 245 C | 9 | Very hot |
| 500 F | 260 C | 10 | Extremely hot |

## Nutritional Information Estimation

### Macro Estimation Framework

```
NUTRITIONAL ESTIMATION APPROACH:

1. List each ingredient with its weight/volume
2. Look up per-100g nutritional values (USDA FoodData Central)
3. Calculate based on actual amount used
4. Sum all ingredients for total recipe nutrition
5. Divide by number of servings

PER-SERVING LABEL FORMAT:
  Calories:      XXX kcal
  Total Fat:     XX g
    Saturated:   XX g
  Cholesterol:   XX mg
  Sodium:        XXX mg
  Total Carbs:   XX g
    Dietary Fiber: XX g
    Sugars:      XX g
  Protein:       XX g

ESTIMATION RULES:
  - Round to nearest 5 for calories
  - Round to nearest 0.5g for macros
  - Always note "approximate" — not lab-tested
  - Exclude cooking oil absorbed during frying (estimate ~15% absorption)
```

### Common Ingredient Quick Reference (per 100g)

| Ingredient | Calories | Protein | Carbs | Fat |
|-----------|----------|---------|-------|-----|
| Chicken breast (cooked) | 165 | 31g | 0g | 3.6g |
| White rice (cooked) | 130 | 2.7g | 28g | 0.3g |
| Pasta (cooked) | 131 | 5g | 25g | 1.1g |
| Whole egg | 155 | 13g | 1.1g | 11g |
| All-purpose flour | 364 | 10g | 76g | 1g |
| Butter | 717 | 0.9g | 0.1g | 81g |
| Olive oil | 884 | 0g | 0g | 100g |
| Whole milk | 61 | 3.2g | 4.8g | 3.3g |
| Cheddar cheese | 403 | 25g | 1.3g | 33g |
| Broccoli | 34 | 2.8g | 7g | 0.4g |

## Dietary Restriction Labels

### Standard Dietary Labels

| Label | Code | Excludes |
|-------|------|----------|
| **Vegan** | VG | All animal products (meat, dairy, eggs, honey) |
| **Vegetarian** | V | Meat, poultry, fish, seafood |
| **Gluten-Free** | GF | Wheat, barley, rye, triticale, and derivatives |
| **Dairy-Free** | DF | Milk, cheese, butter, cream, yogurt |
| **Nut-Free** | NF | Tree nuts and peanuts |
| **Egg-Free** | EF | Eggs and egg-derived ingredients |
| **Soy-Free** | SF | Soy, soy sauce, tofu, edamame |
| **Keto** | K | High-carb ingredients (>20g net carbs/day) |
| **Paleo** | P | Grains, dairy, legumes, refined sugar |
| **Low-FODMAP** | LF | High-FODMAP foods (garlic, onion, wheat, etc.) |
| **Whole30** | W30 | Sugar, alcohol, grains, dairy, legumes |

### Labeling Rules

```
RECIPE LABELING PROTOCOL:
  1. Check EVERY ingredient against each diet's exclusion list
  2. Include hidden ingredients (broths, sauces, seasonings)
  3. Mark only if recipe is FULLY compliant (not "almost")
  4. Note "easily adaptable" if 1 substitution makes it compliant
  5. Cross-contamination note for allergy-critical diets

LABEL FORMAT:
  Primary labels:  [VG] [GF] [DF]
  Adaptable:       "Easily made GF — substitute GF flour 1:1"
  Contains:        "Contains: wheat, dairy, eggs"
```

## Meal Planning Integration

### Weekly Meal Plan Template

```
WEEKLY MEAL PLAN: Week of [Date]
Serves: [N] people

         | Breakfast      | Lunch          | Dinner         | Snack
---------|----------------|----------------|----------------|--------
MON      | [Recipe/Ref]   | [Recipe/Ref]   | [Recipe/Ref]   | [Item]
TUE      | [Recipe/Ref]   | [Recipe/Ref]   | [Recipe/Ref]   | [Item]
WED      | [Recipe/Ref]   | [Recipe/Ref]   | [Recipe/Ref]   | [Item]
THU      | [Recipe/Ref]   | [Recipe/Ref]   | [Recipe/Ref]   | [Item]
FRI      | [Recipe/Ref]   | [Recipe/Ref]   | [Recipe/Ref]   | [Item]
SAT      | [Recipe/Ref]   | [Recipe/Ref]   | [Recipe/Ref]   | [Item]
SUN      | [Recipe/Ref]   | [Recipe/Ref]   | [Recipe/Ref]   | [Item]

PREP DAY (Sunday):
  - Batch cook: [Grains, proteins]
  - Wash and chop: [Vegetables]
  - Make ahead: [Sauces, dressings]
  - Portion: [Snacks, lunches]

ESTIMATED WEEKLY GROCERY COST: $___
ESTIMATED DAILY CALORIES: ___ kcal/person
```

### Grocery List Generation

```
GROCERY LIST: Week of [Date]

PRODUCE:
  [ ] __________ — Qty: ____ — Est: $____
  [ ] __________ — Qty: ____ — Est: $____

PROTEINS:
  [ ] __________ — Qty: ____ — Est: $____
  [ ] __________ — Qty: ____ — Est: $____

DAIRY & EGGS:
  [ ] __________ — Qty: ____ — Est: $____

GRAINS & BREAD:
  [ ] __________ — Qty: ____ — Est: $____

CANNED & DRY GOODS:
  [ ] __________ — Qty: ____ — Est: $____

FROZEN:
  [ ] __________ — Qty: ____ — Est: $____

CONDIMENTS & SPICES (check pantry first):
  [ ] __________ — Qty: ____ — Est: $____

ESTIMATED TOTAL: $____

SHOPPING NOTES:
  - Buy [ingredient] in bulk for multiple recipes
  - Substitute [A] for [B] if unavailable
  - Check pantry for: [staples likely already owned]
```

## Recipe Organization and Categorization

### Collection Taxonomy

```
RECIPE ORGANIZATION SYSTEM:

BY COURSE:
  Breakfast | Lunch | Dinner | Appetizer | Dessert | Snack | Beverage

BY CUISINE:
  Italian | Mexican | Asian | Mediterranean | American | Indian | French

BY METHOD:
  Baking | Grilling | Stovetop | Slow Cooker | Instant Pot | No-Cook | Air Fryer

BY TIME:
  Under 15 min | Under 30 min | Under 60 min | Meal Prep | Weekend Project

BY DIETARY:
  Vegan | Vegetarian | Gluten-Free | Keto | Paleo | Dairy-Free

BY SEASON:
  Spring | Summer | Fall | Winter | Holiday | Year-Round

BY PROTEIN:
  Chicken | Beef | Pork | Fish | Tofu | Beans | Eggs
```

### Recipe Metadata Schema

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `title` | String | Yes | Recipe name |
| `source` | String | Yes | Attribution |
| `servings` | Number | Yes | Yield |
| `prep_time` | Minutes | Yes | Active prep |
| `cook_time` | Minutes | Yes | Cooking/baking |
| `total_time` | Minutes | Yes | End to end |
| `difficulty` | 1-5 | Yes | Skill level |
| `cuisine` | String | Yes | Cuisine type |
| `course` | String | Yes | Meal category |
| `dietary` | String[] | Yes | Diet labels |
| `tags` | String[] | No | Custom tags |
| `rating` | 1-5 | No | Personal rating |
| `notes` | String | No | Personal notes |
| `last_made` | Date | No | Tracking |

## Cooking Technique Reference

### Essential Techniques

| Technique | Temperature | Medium | Best For |
|-----------|------------|--------|----------|
| **Saute** | Medium-high | Small amount of fat | Vegetables, thin proteins |
| **Sear** | High | Thin layer of oil | Steaks, chops, fish |
| **Braise** | Low (300F) | Liquid (partial) | Tough cuts, root vegetables |
| **Roast** | 375-450F | Dry heat, oven | Whole proteins, vegetables |
| **Broil** | 500F+ | Radiant top heat | Finishing, melting, charring |
| **Simmer** | 180-200F | Full liquid | Soups, sauces, stews |
| **Boil** | 212F | Full liquid | Pasta, blanching vegetables |
| **Steam** | 212F | Water vapor | Vegetables, dumplings, fish |
| **Poach** | 160-180F | Full liquid, gentle | Eggs, delicate fish, fruit |

### Internal Temperature Guide

| Protein | Minimum Safe Temp | Ideal (Quality) | Rest Time |
|---------|------------------|-----------------|-----------|
| Chicken/Turkey | 165F / 74C | 165F | 5-10 min |
| Ground beef | 160F / 71C | 160F | 3-5 min |
| Beef steak (medium-rare) | 145F / 63C | 130F (carryover to 135F) | 5-10 min |
| Beef steak (medium) | 145F / 63C | 140F (carryover to 145F) | 5-10 min |
| Pork chop | 145F / 63C | 145F | 5 min |
| Fish | 145F / 63C | 125-140F (varies) | 3-5 min |

## Substitution Guide

### Common Allergen Substitutions

| Ingredient | Substitution | Ratio | Notes |
|-----------|-------------|-------|-------|
| **All-purpose flour** | GF flour blend (1:1) | 1:1 | Add 1/4 tsp xanthan gum if not included |
| **Butter** | Coconut oil | 1:1 | Solid at room temp, slight coconut flavor |
| **Butter** | Vegan butter (Earth Balance) | 1:1 | Best for baking |
| **Milk** | Oat milk | 1:1 | Best for baking, creamiest |
| **Milk** | Almond milk | 1:1 | Lighter, good for savory |
| **Heavy cream** | Full-fat coconut cream | 1:1 | Chill can, use solids |
| **Eggs (binding)** | Flax egg (1 tbsp ground + 3 tbsp water) | 1 egg | Let sit 5 min to gel |
| **Eggs (leavening)** | 1/4 cup applesauce | 1 egg | Adds moisture and sweetness |
| **Eggs (moisture)** | 1/4 cup mashed banana | 1 egg | Adds banana flavor |
| **Soy sauce** | Coconut aminos | 1:1 | Less sodium, slightly sweeter |
| **Cheese** | Nutritional yeast (for flavor) | 2 tbsp per 1/4 cup cheese | Not a texture substitute |
| **Breadcrumbs** | Crushed GF crackers or almond meal | 1:1 | Almond meal adds richness |

### Emergency Pantry Substitutions

| Missing | Substitute | Ratio |
|---------|-----------|-------|
| Buttermilk (1 cup) | 1 cup milk + 1 tbsp lemon juice | Sit 5 min |
| Self-rising flour (1 cup) | 1 cup AP flour + 1.5 tsp BP + 1/4 tsp salt | Mix well |
| Brown sugar (1 cup) | 1 cup white sugar + 1 tbsp molasses | Mix well |
| Honey | Maple syrup | 1:1 |
| Fresh herbs | Dried herbs | 1 tsp dried = 1 tbsp fresh |
| Shallot | Red onion (smaller amount) | 1/2 onion per shallot |
| Wine (cooking) | Broth + 1 tsp vinegar | Same volume |
| Cornstarch (thickener) | 2x all-purpose flour | Cooks out floury taste |

## See Also

- [Health & Wellness](../health-wellness/SKILL.md)
- [Travel Planner](../travel-planner/SKILL.md)
