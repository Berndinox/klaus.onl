# klaus-landing

Static site served at [klaus.onl](https://klaus.onl).

`site/` holds the files. `kustomization.yaml` turns them into the ConfigMap
`klaus-landing-site`, which Flux applies to the homelab cluster. A push to `main`
is live within a few minutes.
