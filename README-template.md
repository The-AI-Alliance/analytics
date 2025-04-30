# How to Use `microsite-template`

This repo is used as a template to create AI Alliance &ldquo;microsites&rdquo;. It is setup as a GitHub _template repo_, which you can use to create a new repo. Even if you aren't creating a microsite, you can use this procedure to create a new AI Alliance repo for other purposes. 

## Creating Your Repo

These are the main steps:

1. Create your repo from the [this template repo](https://github.com/The-AI-Alliance/microsite-template).
1. Convert placeholder _variables_ to the correct values, using the [`finish-microsite.sh`](https://github.com/The-AI-Alliance/microsite-template/blob/main/finish-microsite.sh) script.
1. Add your initial content for the repo.
1. Merge changes to the `latest` branch.
1. Push all updates upstream, `git push --all`.
1. On the repo's home page in GitHub, click the "gear" next to "About" (upper right-hand side). In the _Edit repository details_ that pops up, check the box to _Use your GitHub Pages website_ and enter appropriate _Topics_.
1. Add the website to the Alliance GitHub organization [landing page](https://github.com/The-AI-Alliance/) and the Alliance GitHub Pages [website](https://the-ai-alliance.github.io/#the-ai-alliance-projects).
1. When finished, delete this file!

> [!NOTE] 
> We are planning to automate as many of the manual steps as we can.

Let's look at these steps in more detail.

### 1. Create your repo from the `microsite-template`.

Pick a name for your new repo and follow [these GitHub instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) to create a new repo from the [`microsite-template`](https://github.com/The-AI-Alliance/microsite-template) repo.

### 2. Convert the placeholder _variables_.

After step 1., your repo will have placeholder values for the project name, etc. Next, change to the repo root directory and run the script [`finish-microsite.sh`](https://github.com/The-AI-Alliance/microsite-template/blob/main/finish-microsite.sh) to replace the placeholder _variables_ with appropriate strings for your project.

> [!WARN]
> The `finish-microsite.sh` script uses `zsh`. If you don't have `zsh` available, then use `bash` version 5 or later, e.g., `bash finish-microsite.sh ...`.

At the time of this writing, here are the required arguments shown with example values for a repo named `ai-for-evil-project` under the auspices of the _FA2 Trust and Safety_ focus area work group:

```shell
./finish-microsite.sh \
  --microsite-title "AI for Evil Project" \
  --work-group fa2
```

Referring to a focus area, like `fa2` or `FA2` is expanded as follows:

| Abbreviation | Full name |
| :----------- | :-------- |
| `FA1`        | FA1: Skills and Education |
| `FA2`        | FA2: Trust and Safety |
| `FA3`        | FA3: Applications and Tools |
| `FA4`        | FA4: Hardware Enablement |
| `FA5`        | FA5: Foundation Models and Datasets |
| `FA6`        | FA6: Advocacy |

> [!NOTE]
> 1. Run the script with `zsh`, **_not_** `bash`.
> 2. To see the current list of required arguments and optional argument, run the script with the `--help` flag.

> [!WARN]
> After running the script, your changes are only in your local repo, not pushed upstream. We'll fix that in step 5 below.

### 3. Add your initial content for the repo.

> [!NOTE]
> If you are creating a repo for code, not a microsite, delete the `docs` directory, but do the following steps that make sense. 

There are other placeholder texts in the `docs/**/*.markdown`, README, and other files that you should replace with your real content as soon as possible, e.g.,

1. Find and replace all occurrences of `TODO` with appropriate content.
1. Rename or delete the `second_page.markdown`. Copy it to add more top-level pages, but change the `nav_order` field to control the order of the pages shown in the left-hand side navigation view. 
> [!TIP]
> Start with `10`, `20`, etc. for the `nav_order` of top-level pages, giving yourself room to insert new pages in between existing pages. For nested pages, e.g., under `20`, use `210`, `220`, etc.
3. See the `nested` directory content as an example of how to do nesting, or delete it if you don't need it. Note the metadata fields at the top, such as the `parent` and `has_children` fields.
4. Make any changes you want to make in the `docs/_config.yml` file. (None are mandatory.)

For more tips and guidance on development tasks, see also the links for more information in the `README.md` in your new repo. Add a project-specific description at the beginning of that file.

### 4. Merge changes to the `latest` branch.

> [!NOTE]
> If you are creating a repo for code, not a microsite, delete the `latest` branch:
>
> ```shell
> git br -D latest
> ``` 
>
> Also delete the upstream branch in the GitHub page for your repo. Then ignore the following steps.

As discussed in [`GITHUB_PAGES.md`](https://github.com/The-AI-Alliance/the-ai-alliance.github.io/blob/main/GITHUB_PAGES.md), by default we publish the "microsite" from the `latest` branch, using `main` as the pre-publishing integration branch. Assuming you made all the edits above on the `main` branch, merge them to `latest`.

```shell
git checkout latest
git merge main
```

### 5. Push all updates upstream.

Run the following command:

```shell
git push --all
```

Adding `--all` pushes the `main` and `latest` branches upstream.

### 6. Add Your website to the Alliance GitHub Pages and the Alliance Website.

> [!NOTE]
> If you are creating a repo for code, not a microsite, ignore this section.

When you are ready for broader exposure for your site, there are a few places where we have an index to all the &ldquo;microsites&rdquo;. Add your site in the table shown in each of the following locations. Note how the rows are grouped by focus area. Put your new row with the others in your focus area.

* https://github.com/The-AI-Alliance/.github/blob/main/profile/README.md
* https://github.com/The-AI-Alliance/the-ai-alliance.github.io/blob/main/docs/index.markdown

You can just edit the page directly in GitHub and submit a PR. Note that for the second link, the `index.markdown` page for the `the-ai-alliance.github.io` site, we add `{:target="..."}` annotations to each link. Just use a unique name for your links.

Finally, talk to your focus area leaders about updating the [AI Alliance website](https://thealliance.ai) with information about your project site.

### 7. When finished, delete this file

This file is no longer needed, so you can remove it from your repo:

```shell
git rm README-template.md
```

If you are building a microsite and have the `latest` branch:

```shell
git checkout latest
git merge main
```

Finally, push upstream:

```shell
git push --all
```
