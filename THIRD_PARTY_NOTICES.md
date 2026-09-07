# Local frontend dependencies

Browser scripts and styles are served from this repository. No JavaScript is loaded from a third-party CDN.

| Package | Version | License |
| --- | --- | --- |
| Chart.js | 4.4.7 | MIT |
| Tailwind CSS | 3.4.17 | MIT |
| Lucide | 0.468.0 | ISC |

License notices are retained in `assets/vendor`. Build dependency versions and registry integrity hashes are recorded in `package-lock.json`.

To regenerate assets after editing HTML classes or the themes in `scripts/style-builds.json`:

```sh
npm ci --ignore-scripts
npm run build:assets
python3 scripts/security_gate.py
```

Commit the regenerated assets with the source change. No Node server or build step is needed to visit the published static pages. An advisory check of the locked build dependencies returned no known vulnerabilities on 7 September 2026; rerun `npm audit` when updating dependencies.
