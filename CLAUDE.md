# klaus.onl — Claude context

Static personal site served at https://klaus.onl.

## Rule 1: this repo is public

Everything here is public: files, commit messages, branch names and the full
history, including this file. Never commit:

- secrets of any kind (passwords, tokens, API keys, private keys, cookies)
- real internal details of the infrastructure behind the site: IP addresses,
  hostnames, network layout, cluster or namespace names, software versions,
  paths, configs
- personal data beyond what the site already shows

Fake values in the terminal easter egg are fine, but they must not reproduce
the real setup. If unsure whether something is sensitive, ask first.

If something sensitive was pushed, stop and tell the owner. Rewriting history
does not undo it (forks, caches, clones); a leaked secret must be rotated.

## How changes go live

- A push to `main` is live within one to two minutes. There is no build step
  and no staging, so check changes locally first (open `site/index.html`).
- `kustomization.yaml` turns the files in `site/` into one ConfigMap. Only
  that ConfigMap is deployed from here; any other manifest makes the deploy
  fail.
- A new file must be listed in `kustomization.yaml`. The ConfigMap is flat,
  so files in subdirectories need a key and a matching server rule (see
  `security.txt`).
- The ConfigMap must stay under 1 MiB in total (about 240 KB today). Keep
  images small.
- Web server config (paths, caching, headers, 404 handling) is not in this
  repo. Changes to it are made by the owner elsewhere.
