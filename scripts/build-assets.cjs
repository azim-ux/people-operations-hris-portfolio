// Build reviewed local assets; dependency versions and integrity are locked.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const {createHash} = require('node:crypto');
const {execFileSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const builds = require('./style-builds.json');
const vendor = path.join(root, 'assets', 'vendor');
fs.mkdirSync(vendor, {recursive: true});
const copies = [
  ['chart.js/dist/chart.umd.js', 'chart.umd.min.js'],
  ['chart.js/LICENSE.md', 'Chart.js.LICENSE.md'],
  ['tailwindcss/LICENSE', 'Tailwind.LICENSE.txt'],
];
if (require('../package.json').devDependencies.lucide) copies.push(
  ['lucide/dist/umd/lucide.min.js', 'lucide.min.js'],
  ['lucide/LICENSE', 'Lucide.LICENSE.txt'],
);
for (const [source, destination] of copies) {
  fs.copyFileSync(path.join(root, 'node_modules', source), path.join(vendor, destination));
}
// Keep the existing onboarding CSP synchronized with its inline application script.
for (const build of builds) {
  const file = path.join(root, build.html);
  let html = fs.readFileSync(file, 'utf8');
  if (!html.includes('http-equiv="Content-Security-Policy"')) continue;
  const hashes = [...html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/gi)]
    .filter(match => !/\bsrc\s*=|application\/json/i.test(match[1]))
    .map(match => "'sha256-" + createHash('sha256').update(match[2]).digest('base64') + "'");
  html = html.replace(/script-src [^;]+;/, "script-src 'self' " + [...new Set(hashes)].join(' ') + ';');
  fs.writeFileSync(file, html);
}
const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'portfolio-styles-'));
try {
  for (const css of new Set(builds.map(build => build.css))) {
    const group = builds.filter(build => build.css === css);
    const config = {...group[0].config, content: group.map(build => path.join(root, build.html))};
    const configPath = path.join(temp, 'tailwind.config.json');
    fs.writeFileSync(configPath, JSON.stringify(config));
    const output = path.join(root, css);
    fs.mkdirSync(path.dirname(output), {recursive: true});
    execFileSync(process.execPath, [path.join(root, 'node_modules/tailwindcss/lib/cli.js'),
      '--config', configPath, '--input', path.join(__dirname, 'tailwind-input.css'),
      '--output', output, '--minify'], {cwd: root, stdio: 'inherit'});
  }
} finally {
  fs.rmSync(temp, {recursive: true, force: true});
}
console.log('Built local styles and vendor scripts.');
