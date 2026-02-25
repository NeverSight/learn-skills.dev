---
name: art-of-comment
description: This is your guide for giving a comments within the codebase, whether it's a inline comment or a comprehensive JSDoc style comment. Use this skill when you generate a code for bugs fixing, building a new components, refactoring and implementing new features.  
---

# Overview 
When you need to comment a specific code part, a function, or a component, always refer to this skill. Create a comments that actually provide additional context, not just for the sake of giving a comments. Create a comments that actually make others think the comment is useful enough and doesn't want to outright delete it after reading it the first time. Comments are useful when necessary, especially a comprehensive yet concise JSDoc that explains something. But overdoing it, especially an inline comment, it just make the code even harder to read. Comments, while adding more stuff to read, should enhance readability of the overall codebase by providing useful context and guidance, yet not stating the obvious. 

# Guidelines 
- Not every component or functions (or even every lines!) need to be given a comment or a JSDoc. Unless you're being explicitly told to giving a comments or create a JSDoc style documentation.
- Create an inline comments that is clear and concise, an inline comment shouldn't goes beyond 2 lines. 
- Create a JSDoc documentation that is comprehensive, yet concise and clear in wording. Not every part of the components or functions need to be explained on the JSDoc, includes only the useful part that provided additional context that the readers need to know or usage examples if needed.
- Don't state any assumptions in your comments and JSDoc, always refer to the libraries documentation, project standards on [Copilot Instructions](), and best practices. Ask for clarification if you're not sure about your comments. 
- If the current implementation of a code have a trade-offs, explain them in the comments, why it's worth taking, and why the decision being  made in the first place. 
- Refer to any existing comments and JSDoc when you create a new ones, this will ensure consistency across different comments. Never state any contradictory statements. 

# Example

From the code snippet below, there is several comments that worth examining.
1.  This first one is a good example of clear and concise comment. It explain what the function does and what its output. But, it will better to use an multi line comment syntax `/** ... */` instead of `//`, because the functions is used in other part of the file, when the user hover over it, they will see the information.
2. This one is not needed, it stated the obvious. There is no additional context that the comment provides, the code section already self-explanatory.
3. This one most likely in the same category as (2), but this can be useful for when debugging or explaining why the code is changed when fixing a bug, refactoring, or code improvement. 
4. This point just repeating what already stated in the (1), don't duplicate information like this. Always refer to previous comment for any duplicated context. 
5. This is a good example of concise and contextual comment, explain why the code written in that specific ways and the result/effect of the code.  

```typescript

// (1) Calculate chart segments based on priority: verified > registered > rejected
  const getChartSegments = (): {
    value: number
    color: string
    backgroundColor?: string
    badgeLabel?: string
  }[] => {
    const verified = data?.verified ?? 0
    const registered = data?.registered ?? 0
    const rejected = data?.rejected ?? 0
    const total = verified + registered + rejected

    // (2) If all values are 0, show full gray circle
    if (total === 0) {
      return [{ value: 1, color: colors.palette.lightGray }]
    }

    // (3) Filter out zero values to prevent empty segments
    const segments = []

    // (4) Priority order: verified > registered > rejected
    if (verified > 0) {
      segments.push({
        value: verified,
        color: '#01C58A',
        backgroundColor: '#D6F6EC',
        badgeLabel: `${verified} Aset Terdata`,
      })
    }
    if (registered > 0) {
      segments.push({
        value: registered,
        color: '#FF9E00',
        backgroundColor: '#FFF1DB',
        badgeLabel: `${registered} Belum Diverif`,
      })
    }
    if (rejected > 0) {
      segments.push({
        value: rejected <= 2 ? 2 : rejected, // (5) Workaround to cap the visible segment to 2
        color: '#FF5264',
        backgroundColor: '#FFECEC',
        badgeLabel: `${rejected} Ditolak`,
      })
    }
```
