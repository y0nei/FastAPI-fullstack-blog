## Article structure

You have probably already seen the placeholder articles shown on the website
upon accessing the platform.

The articles live in the `posts`[^1] directory in the root of the project, each
article should have its own folder labeled with a numeric ID.

Each folder holds a Markdown file, the name of which should be `content.md`.[^1]

```py title="Example"
.
├── src
└── posts/
    ├── 1/
    │   └── content.md
    ├── 2
    ├── 3
    └── ...
```

---

If you wish to have links to local images in your article, just store them in
the same folder as the `content.md` file.

```py title="Example" hl_lines="6"
.
├── src
└── posts/
    ├── 1/
    │   ├── content.md  # Article about cats
    │   └── cat_image.jpg
    └── ...
```

**Note**: When linking a local image, specify the ID prefix in the link, eg.
`![epic cat pic][1/cat_image.jpg]`  
*(This is because the `pymdownx.b64` extension uses the `posts` directory as the
  base path used to resolve relative links)*

## Editing an article

Thanks to the power of Markdown, each article is just a file, no need to keep
that content in a database. The articles can be easily backed up and edited
when needed in your favourite markdown editor.

**Note**: When the `HOTRELOAD`[^2] setting is enabled, you get a live preview of
the edited changes.

### Markdown syntax

As the `Python-Markdown` library states:

>This is a Python implementation of John Gruber’s [Markdown][2].
>It is almost completely compliant with the reference implementation, though
>there are a few very minor [differences][3]. See John’s
>[Syntax Documentation][4] for the syntax rules.

Of course this is not all there is, thanks to various Markdown extensions, we
can have modern and flexible features in our articles.  
For a complete list of additional functionality, see the [extensions][5] section
of the article. *(Not implemented yet)*

### Metadata

Each article should have defined frontmatter metadata, this allows articles to
be actually viewed on the article list, have its titles displayed and be sorted
by tags or dates.

```markdown title="Example" hl_lines="1-7"
---
title: My awesome article
date: 10-3-2023
tags: cats
      pets
      workout
---

# Awesome article
**totally** awesome
```
For more information on how to structure metadata fields, refer to the docs of
the [Python-Markdown Meta-data extension][1]

[1]: https://python-markdown.github.io/extensions/meta_data/#syntax
[2]: https://daringfireball.net/projects/markdown/
[3]: https://python-markdown.github.io/#differences
[4]: https://daringfireball.net/projects/markdown/syntax
[5]: /extensions

[^1]: This name will be configurable in the future, for now this is statically
      defined.
[^2]: See [Configure the environment](../configure_the_environment)
