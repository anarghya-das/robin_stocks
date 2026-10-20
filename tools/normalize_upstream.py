"""Adapt newly merged upstream Python modules to the fork's namespace."""

from pathlib import Path
import re
import subprocess


def main():
    root = Path(__file__).resolve().parents[1]
    old_package = root / 'robin_stocks'
    package = root / 'calcap_robin_stocks'
    if old_package.exists():
        for source in old_package.rglob('*'):
            if not source.is_file():
                continue
            destination = package / source.relative_to(old_package)
            if destination.exists():
                raise RuntimeError(f'Resolve namespace collision: {source}')
            destination.parent.mkdir(parents=True, exist_ok=True)
            source.rename(destination)

    # Include tracked upstream examples and tests, as well as moved additions.
    tracked = subprocess.check_output(
        ['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
    paths = {root / name for name in tracked if name.endswith('.py')}
    paths.update(package.rglob('*.py'))
    for path in paths:
        if not path.is_file() or path.resolve() == Path(__file__).resolve():
            continue
        text = path.read_text()
        updated = re.sub(r'\brobin_stocks\b', 'calcap_robin_stocks', text)
        # Repository URLs continue to identify the existing GitHub repositories.
        updated = re.sub(r'(https?://github.com/[^/]+/)calcap_robin_stocks',
                         r'\1robin_stocks', updated)
        if updated != text:
            path.write_text(updated)


if __name__ == '__main__':
    main()
