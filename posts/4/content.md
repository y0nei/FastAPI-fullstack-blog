---
title: Test Markdown file
description: This article is used to test the markdown functionality of this app.
tags: development
      markdown
date: 12-10-2023
---

> This file showcases various features of the Markdown parser while also serving
> as a testing ground for extensions.  
> To stay up-to-date with the latest enhancements and additions, please refer to this article.

Table of contents
=================
The `toc` extension auto-generates a table of contents when the `[TOC]` element
is specified, the heading levels taken into concideration are specified with the
`toc_depth` option in the markdown helper file

<br>

[TOC]

***

Headings
========
Each heading has a permalink

# h1 heading
## h2 heading
### h3 heading
#### h4 heading
##### h5 heading
###### h6 heading

---

Inline styles
=============
The ^superscript^ and ~subscript~ functionality is provided by 
the `markdown_sub_sup` extension, and the ~~deleted~~ and ++inserted++ 
functionality by `markdown_del_ins`

<br>

This text is **bold**, *italic*, ~~deleted~~ and ++inserted++  
You can also use underscores for __bold__ or _italic_ text.

Here is a `code` element, ^sup^ and ~sub~

---

Lists
=====
This is enabled by the builtin python markdown `sane_lists` extension.

<br>

#### Unordered

+ Create a list by starting a line with `+`, `-`, or `*`
    - Sub-lists are made by indenting 4 spaces:
        * Very easy!

#### Ordered

1. Look at me I'm ordered!
    - You can also mix and match
2. Buy bread

1. You can use sequential numbers...
1. ...or keep all the numbers as `1.`

#### Or even start numbering with offset

57. foo
1. bar

---

Links
=====

[I'm an inline-style link](https://example.com)  
[I'm an inline-style link with title](https://example.com "Example page")

[I'm a reference-style link][Arbitrary case-insensitive reference text]  
[You can use numbers for reference-style link definitions][1]

Or leave it empty and use the [link text itself].

<br>

##### Thanks to `pymdownx.magiclink`, we can auto-link HTML, FTP, and email links:

- Just paste links directly in the document like this: https://example.com.
    - URLs in angle brackets work too <https://example.com>
- An email address: fake.email@email.com.

[arbitrary case-insensitive reference text]: https://www.mozilla.org
[1]: https://example.com
[link text itself]: https://example.com

---

Tables
======
This is enabled by the builtin python markdown `tables` extension.

<br>

Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

There must be at least 3 dashes separating each header cell.
The outer pipes (|) are optional, and you don't need to make the
raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

| Command | Description |
| --- | --- |
| git status | List all new or modified files |
| git diff | Show file differences that haven't been staged |

| Command | Description |
| --- | --- |
| `git status` | List all *new or modified* files |
| `git diff` | Show file differences that **haven't been** staged |

| Left-aligned | Center-aligned | Right-aligned |
| :---         |     :---:      |          ---: |
| git status   | git status     | git status    |
| git diff     | git diff       | git diff      |

| Name     | Character |
| ---      | ---       |
| Backtick | `         |
| Pipe     | \|        |

---

Typographic replacements
========================
This is enabled by the `pymdownx.smartsymbols` extension.

| Markdown       | Result       |
| -------------- | ------------ |
| `(tm)`         | ™            |
| `(c)`          | ©            |
| `(r)`          | ®            |
| `c/o`          | ℅            |
| `+/-`          | ±            |
| `-->`          | →            |
| `<--`          | ←            |
| `<-->`         | ↔            |
| `=/=`          | ≠            |
| `1/4, etc.`    | ¼, etc.      |
| `1st 2nd etc.` | 1st 2nd etc. |

---

Checklists
==========
This is enabled by the `markdown_checklist` extension.

<br>

- [ ] Task 1
- [x] Task 2
- [ ] **Look**, `i` *can* ^also^ ~~have~~ ++styling++
- [x] Buy bread

---

Footnotes
=========
This is enabled by the builtin python markdown `footnotes` extension.

Footnote 1 link[^first]  
Footnote 2 link[^second]  
Duplicated footnote reference[^second]

I am a very handsome boy^[citation&nbsp;needed]^

[^first]: Footnotes **can have markup**

    and multiple paragraphs.

[^second]: Footnote text.

---

Blockquotes
===========

> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> Blockquotes can also be nested...
>> ...by using additional greater-than signs right next to each other...
> > > ...or with spaces between arrows.
>
> > It can also have code blocks in them:
>
> ```python
> if __name__ == "__main__":
>   print("Hello, World!")
> ```

---

Code and Syntax Highlighting
============================
The code block functionality is provided by `pymdownx.superfences`,
the highlighting is done in the backend by `pymdownx.highlight` and `pygments`

<br>

#### Example CSS code
```css
@font-face {
    font-family: Chunkfive; src: url('Chunkfive.otf');
}

body, .usertext {
    color: #F0F0F0; background: #600;
    font-family: Chunkfive, sans;
}

@import url(print.css);
@media print {
    a[href^=http]::after {
        content: attr(href)
    }
}
```

#### Example JavaScript code
(with highlighted lines)
```{.js hl_lines="1 3 9-11"}
function $initHighlight(block, cls) {
    try {
        if (cls.search(/\bno\-highlight\b/) != -1)
            return process(block, true, 0x0F) +
                ` class="${cls}"`;
    } catch (e) {
        /* handle exception */
    }
    for (var i = 0 / 2; i < classes.length; i++) {
        if (checkCondition(classes[i]) === undefined)
            console.log('undefined');
    }
}

export $initHighlight;
```

---

Images
======

Here's a logo (hover to see the title text):

Inline-style:
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

Reference-style:
![alt text][logo]

[logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"

![Kitten](https://placekitten.com/840/360)
![Kitten](https://placekitten.com/640/360 "A verry cute cat")

Like links, Images also have a footnote style syntax  
With a reference later in the document defining the URL location

![Alt text][id]

[id]: https://placekitten.com/400/380  "Another totally bonkers cat"

Base64 embedded images
----------------------

Thanks to `pymdownx.b64`, we can have embedded local images  
![puter with code on em](4/fotis-fotopoulos-DuHKoV44prg-unsplash.jpg "src: https://unsplash.com/photos/DuHKoV44prg")

and embedded GIFs too!  
![cat licking camera](4/cta_lcik_camera.gif)
