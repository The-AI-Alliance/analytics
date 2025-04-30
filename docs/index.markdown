---
layout: default
title: Home
nav_order: 10
has_children: false
---

# MICROSITE_TITLE

[GitHub Repo](https://github.com/The-AI-Alliance/REPO_NAME){:target="repo" .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 .no-glyph}
[The AI Alliance](https://thealliance.ai){:target="ai-alliance" .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 .no-glyph} 

| **Authors**     | [WORK_GROUP_NAME](WORK_GROUP_URL){:target="ai-alliance-wg"} (See the [Contributors]({{site.baseurl}}/contributing/#contributors)) |
| **Last Update** | V0.0.1, YMD_TSTAMP |

Welcome to the **The AI Alliance**: **MICROSITE_TITLE**.

> **Tip:** Use the search box at the top of this page to find specific content.

> **TODO:** This is a work-in-progress website for the MICROSITE_TITLE.

> **NOTE:** The "boilerplate" text on this page mixes content you might want to use, as well as tips on writing Markdown.

TODO: add more "welcome" content for your site here...

This site is organized into the following sections [^1] (with an example footnote):

* [TODO - second top-level page]({{site.baseurl}}/second_page)
    * [alternative link](second_page)
* [TODO - nested]({{site.baseurl}}/nested/nested)

Note how relative links are written. For siblings (like the next set of bullets...) or subpages, you don't have to use the `{{site.baseurl}}` prefix (like the `alternative link`), but use `{{site.baseurl}}` instead of relative navigation hacks like `../../foo/bar`.

Additional links: [^2]

* [Contributing]({{site.baseurl}}/contributing): We welcome your contributions! Here's how you can contribute.
* [About Us]({{site.baseurl}}/about): More about the AI Alliance and this project.
* [The AI Alliance](https://thealliance.ai){:target="ai-alliance"}: The AI Alliance website.
* [Project GitHub Repo](https://github.com/The-AI-Alliance/REPO_NAME){:target="repo"}

Note our convention that external URLs include a target, specified with `{:target="some_name"}`. In fact, Jekyll is configured in `_config.yml` to use the `jekyll-target-blank` plugin, which automatically opens external links in a new tab, named `blank`. This is good enough, but it also means that every link you click will open in the same tab. So, explicitly specifying a `:target` provides a nicer experience. You will also notice that external links get a little box and arrow adornment. This is done automatically through a clever CSS hack in `docs/_includes/css/custom.scss.liquid`.

A table example using standard Markdown and showing how to set the desired alignment. (The extra whitespace in the source is only for easier readability.):

| Column 1 (Left Aligned) | Column 2 (Centered) | Column 3 (Numbers - Right Aligned) |
| :------- | :------------------: | -----: |
| text 1   | centered             | 1      |
| text 2   | also centered        | 20     |
| text 3   | and this is centered | 300    |

### Version History

| Version  | Date       |
| :------- | :--------- |
| V0.0.1   | YMD_TSTAMP |

[^1]: Use `[^N]` (for increasing `N` values) to mark "footnote #N" in text, as shown above. This is an example footnote with a link to it from above, and a link at the end of the footnote to go back to the point in the text (the "curled" arrow). **WARNING**, you must include the colon in the footnote definition as shown here, `[^1]:`.
[^2]: A second example footnote. Note that you don't need to put a blank line between them; they work like lists.

<!-- 
Use the following construct to automatically show a table of
contents (ToC) for the child pages.
For this page, you already have a "manual" ToC in the bullet 
lists above.
-->
{:toc}
