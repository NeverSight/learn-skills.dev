---
name: biblatex
description: "LaTeX biblatex/biber packages for modern bibliography management. Use when helping users cite references, manage .bib files, choose citation styles, or troubleshoot bibliography compilation."
---

# biblatex + biber — Modern Bibliography Management

**CTAN:** https://ctan.org/pkg/biblatex  
**Manual:** `texdoc biblatex`

## Setup

```latex
\usepackage[
  backend=biber,        % modern backend (not bibtex)
  style=authoryear,     % citation + bibliography style
  sorting=nyt,          % name-year-title
  maxbibnames=99,       % show all authors in bibliography
  maxcitenames=2,       % truncate in citations
]{biblatex}

\addbibresource{references.bib}   % .bib file (include extension!)

% At end of document:
\printbibliography
```

## Compilation Workflow

```bash
pdflatex  main.tex    # 1. Generate .bcf file
biber     main        # 2. Process bibliography (no extension!)
pdflatex  main.tex    # 3. Resolve references
pdflatex  main.tex    # 4. Final pass (page numbers, back-refs)
```

Or with latexmk: `latexmk -pdf main.tex` (handles everything automatically).

## .bib File Format

```bibtex
@article{einstein1905,
  author    = {Einstein, Albert},
  title     = {On the Electrodynamics of Moving Bodies},
  journal   = {Annalen der Physik},
  year      = {1905},
  volume    = {322},
  number    = {10},
  pages     = {891--921},
  doi       = {10.1002/andp.19053221004},
}

@book{knuth1984,
  author    = {Knuth, Donald E.},
  title     = {The {\TeX}book},
  publisher = {Addison-Wesley},
  year      = {1984},
  isbn      = {0-201-13447-0},
}

@inproceedings{smith2023,
  author    = {Smith, John and Doe, Jane},
  title     = {Deep Learning for Everything},
  booktitle = {Proceedings of ICML},
  year      = {2023},
  pages     = {100--110},
  doi       = {10.1234/icml.2023.100},
}

@online{wiki2024,
  author    = {{Wikipedia contributors}},
  title     = {LaTeX},
  url       = {https://en.wikipedia.org/wiki/LaTeX},
  urldate   = {2024-01-15},
  year      = {2024},
}

@thesis{jones2020,
  author    = {Jones, Alice},
  title     = {Quantum Computing Applications},
  type      = {phdthesis},
  institution = {MIT},
  year      = {2020},
}

@manual{pgfmanual,
  author    = {Tantau, Till},
  title     = {The TikZ and PGF Packages},
  year      = {2023},
  url       = {https://ctan.org/pkg/pgf},
}
```

### Common Entry Types

| Type | Use for |
|------|---------|
| `@article` | Journal articles |
| `@book` | Books |
| `@inproceedings` | Conference papers |
| `@incollection` | Chapter in edited book |
| `@thesis` | PhD/Master's thesis (use `type` field) |
| `@online` | Websites, web resources |
| `@manual` | Technical documentation |
| `@techreport` | Technical reports |
| `@misc` | Anything else |
| `@unpublished` | Unpublished manuscripts |
| `@patent` | Patents |
| `@software` | Software packages |

### Common Fields

| Field | Description |
|-------|-------------|
| `author` | Author(s) — `{Last, First and Last, First}` |
| `title` | Title — protect caps with `{NASA}` |
| `year`/`date` | Publication year or full date (`2023-06-15`) |
| `journal` | Journal name |
| `booktitle` | Conference/collection title |
| `publisher` | Publisher |
| `volume`/`number` | Volume and issue |
| `pages` | Page range (`10--20`) |
| `doi` | Digital Object Identifier |
| `url` | Web URL |
| `urldate` | Access date for online sources |
| `isbn`/`issn` | Identifiers |
| `editor` | Editor(s) |
| `edition` | Edition (`{2nd}`) |
| `note` | Additional notes |
| `abstract` | Abstract (not printed by default) |
| `keywords` | Keywords for filtering |
| `langid` | Language (`english`, `german`) — for hyphenation |

### Author Name Formats

```bibtex
author = {Last, First},                    % single
author = {Last, First and Last, First},    % multiple
author = {Last, Jr., First},               % suffix
author = {{World Health Organization}},    % corporate (double braces)
author = {da Silva, João},                 % name particles
```

## Citation Commands

| Command | Output (authoryear) | Output (numeric) |
|---------|--------------------|--------------------|
| `\cite{key}` | Einstein 1905 | [1] |
| `\parencite{key}` | (Einstein 1905) | [1] |
| `\textcite{key}` | Einstein (1905) | Einstein [1] |
| `\autocite{key}` | Style-dependent | Style-dependent |
| `\fullcite{key}` | Full bibliography entry inline | — |
| `\footcite{key}` | Footnote citation | — |
| `\citeauthor{key}` | Einstein | Einstein |
| `\citeyear{key}` | 1905 | 1905 |
| `\citetitle{key}` | On the Electro... | — |

### With Options

```latex
\parencite[see][p.~42]{einstein1905}
% Output: (see Einstein 1905, p. 42)

\parencite[p.~42]{einstein1905}
% Output: (Einstein 1905, p. 42)

% Multiple citations
\parencite{einstein1905, knuth1984}
% Output: (Einstein 1905; Knuth 1984)
```

## Bibliography Styles

| Style | Citation | Bibliography | Use for |
|-------|----------|-------------|---------|
| `authoryear` | Einstein (1905) | Alphabetical by author | Humanities, social sciences |
| `numeric` | [1] | Numbered by citation order | Sciences, engineering |
| `alphabetic` | [Ein05] | Alphabetical labels | Math, CS |
| `authortitle` | Einstein, "On the..." | Author-title | Humanities |
| `verbose` | Full cite in footnotes | Detailed | Law, history |
| `ieee` | [1] | IEEE format | Engineering (needs `biblatex-ieee`) |
| `apa` | (Einstein, 1905) | APA 7th ed | Psychology (needs `biblatex-apa`) |
| `chicago-authordate` | (Einstein 1905) | Chicago | Humanities (needs `biblatex-chicago`) |
| `nature` | ¹ | Nature format | Natural sciences (`biblatex-nature`) |

```latex
% For IEEE:
\usepackage[style=ieee, backend=biber]{biblatex}

% For APA:
\usepackage[style=apa, backend=biber]{biblatex}
% Also needs: \DeclareLanguageMapping{english}{english-apa}
```

## Sorting Options

| Value | Sorting order |
|-------|---------------|
| `nty` | Name, title, year (default for authoryear) |
| `nyt` | Name, year, title |
| `none` | Citation order (for numeric) |
| `ynt` | Year, name, title |
| `anyt` | Alphabetic label, name, year, title |

## Printing the Bibliography

```latex
% Simple
\printbibliography

% With title
\printbibliography[title={References}]

% As section (not chapter)
\printbibliography[heading=subbibliography]

% Filtered
\printbibliography[type=article, title={Journal Articles}]
\printbibliography[keyword=primary, title={Primary Sources}]
\printbibliography[notkeyword=primary, title={Secondary Sources}]
```

### Multiple Bibliographies

```latex
% By type
\printbibliography[type=book, heading=subbibliography, title={Books}]
\printbibliography[type=article, heading=subbibliography, title={Articles}]

% By keyword
% In .bib: keywords = {primary}
\printbibliography[keyword=primary, title={Primary Sources}]
\printbibliography[notkeyword=primary, title={Other Sources}]

% Per chapter (refsection)
\begin{refsection}
\chapter{First Chapter}
Text \cite{something}.
\printbibliography[heading=subbibliography]
\end{refsection}
```

## Useful Options

```latex
\usepackage[
  backend=biber,
  style=authoryear,
  sorting=nyt,
  maxbibnames=99,      % all authors in bibliography
  maxcitenames=2,      % "Smith et al." after 2 authors
  mincitenames=1,      % show at least 1 before "et al."
  uniquelist=false,    % don't disambiguate with more names
  uniquename=false,    % don't disambiguate with initials
  dashed=false,        % repeat author name (vs dash for same author)
  doi=true,            % print DOIs
  isbn=false,          % hide ISBNs
  url=false,           % hide URLs (except @online)
  eprint=false,        % hide eprint info
  date=year,           % show only year
]{biblatex}
```

## Comparison: biblatex vs natbib/BibTeX

| Feature | biblatex + biber | natbib + BibTeX |
|---------|-----------------|-----------------|
| Unicode | ✅ Full support | ❌ Limited |
| Styles | Flexible (LaTeX macros) | .bst files (hard to edit) |
| Entry types | More (`@online`, `@software`) | Fewer |
| Filtering | `keyword`, `type` filters | Manual |
| Multiple bibliographies | Built-in | Needs multibib/etc |
| Fine-grained citations | `\textcite`, `\parencite`, etc | `\citet`, `\citep` |
| Date handling | Full dates, ranges | Year only |
| Name handling | Sophisticated | Basic |
| Compilation | pdflatex → biber → pdflatex² | pdflatex → bibtex → pdflatex² |
| Journal requirement | Some require BibTeX | ✅ Traditional |

**Recommendation:** Use biblatex for new documents. Use natbib only if a journal template requires it.

## Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| "I found no \citation commands" | biber not run | Run biber after first pdflatex |
| "I found no \bibstyle command" | Mixing bibtex with biblatex | Use `biber`, not `bibtex` |
| Citation shows [key] | biber hasn't run / error | Check biber log, re-run |
| `.bib` file not found | Missing extension in `\addbibresource` | Include `.bib` extension |
| Unicode in .bib fails | Using BibTeX backend | Use `backend=biber` |
| Author "et al." wrong | maxcitenames too low | Adjust `maxcitenames` |
| Style not found | Missing package | Install `biblatex-ieee`, `biblatex-apa`, etc. |
| Refsection empty | Citations outside refsection | Each refsection is independent |
| Name sorting wrong | Particles (van, de) | Use `\DeclareNameAlias` or check `useprefix` |
| "Runaway argument" | Missing comma in .bib | Check .bib syntax (commas between fields) |
