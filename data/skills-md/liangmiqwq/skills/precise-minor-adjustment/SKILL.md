---
name: precise-minor-adjustment
description: Load this skill when you are modifying existing code, or doing small patch and adjustment. Load this skill when you are reviewing an implementation or a diff, to judge whether this change is clear and consistent with other parts in codebase.
---

## Consistent Change

When you are required to make a patch for a problem or a feature, you need to find the related part of the code.

It might be a function, a object or a class.

Before doing any change, you should quickly look through how the original maintainer organize the code, you can take a look at its code style, comment writing style and test style.

And when you modifying the code, you should also follow its code style and organize method. For example, if the original maintainer used a `for` loop to find a thing, you shouldn't modify it to other functions unless you have to do it. You aren't supposed to remove the original comments, unless they are outdated.

## Helper Style

Helper is not so helpful as you think for some cases.

We should follow the `consistent change` rule above. When you look through the original code style, you can take a look that whether the original code like to use helpers. If they prefer just inline code, you should also inline code. If they prefer put helpers in another file, each file contains only one helper, you should also follow it.

## Fill TODO

Sometimes, you are required to just finish a todo in codebase. This way, you should do changes like doing operation.

That means, you are not to supposed refactor the function's internal logic, or adjust its models, instead you should only care about the part marked as `TODO` (maybe a comment or a macro/function call). Focus on this and do not disturb other parts. Like this is a `TODO` in for loop, you shouldn't change this for loop to a while loop unless you have to do it.
