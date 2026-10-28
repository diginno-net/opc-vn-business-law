#!/usr/bin/env python3
"""Build public ZIP/.skill from explicit source paths; leave checkout untouched."""
import argparse
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'opc-vn-business-law'
PUBLIC_DOCS = ['SKILL.md', 'README.md', 'DISCLAIMER.md', 'LICENSE', 'CHANGELOG.md',
               'MAINTAINING.md', 'PROMO.md']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    parser.add_argument('--kind', choices=['all', 'zip', 'skill'], default='all')
    args = parser.parse_args()
    content = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    version = re.search(r'^  version: (\d+\.\d+\.\d+)\s*$', content, re.MULTILINE)
    if not version:
        parser.error('SKILL.md needs a three-part metadata.version')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    runtime = [ROOT / name for name in PUBLIC_DOCS]
    runtime += sorted((ROOT / 'references').glob('*.md'))
    runtime += sorted((ROOT / 'assets').glob('*.md'))
    runtime += [ROOT / 'scripts/so_sanh_thue.py']
    full = sorted(set(runtime + list((ROOT / 'scripts').glob('*.py'))
                      + list((ROOT / 'scripts').glob('*.sh'))
                      + list((ROOT / 'tests').glob('test_*.py'))
                      + list((ROOT / 'evals').glob('*.json'))
                      + list((ROOT / 'evals').glob('*.md'))))
    for kind, files in [('skill', runtime), ('zip', full)]:
        if args.kind not in ('all', kind):
            continue
        target = output / (f'{NAME}.skill' if kind == 'skill' else f'{NAME}-v{version[1]}.zip')
        # Only the named archive is replaced; no directory removal or .git relocation.
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
            for source in files:
                if source.is_symlink() or not source.is_file():
                    raise ValueError(f'Expected regular public source: {source.name}')
                relative = source.relative_to(ROOT)
                archive.write(source, str(Path(NAME) / relative if kind == 'skill' else relative))
        print(f'Created {target.name}: {len(files)} public files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
