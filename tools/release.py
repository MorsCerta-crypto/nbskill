"Publish GitHub artifacts with Fastship before an immutable release is sealed."
import argparse, asyncio, subprocess
from pathlib import Path
from fastship.release import Release, get_config


def git(root, *args): return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


async def publish(root, artifacts, tag=None, latest=False, publish=False):
    root = root.resolve()
    artifacts = [str(p.resolve(strict=True)) for p in artifacts]
    cfg = get_config(root)
    tag = tag or cfg.version
    head = git(root, 'rev-parse', 'HEAD')
    if git(root, 'status', '--porcelain'): raise ValueError('Release checkout must be clean')
    if git(root, 'rev-parse', f'{tag}^{{commit}}') != head: raise ValueError('Local tag must match HEAD')
    remote = git(root, 'ls-remote', 'origin', f'refs/tags/{tag}', f'refs/tags/{tag}^{{}}')
    if head not in [row.split()[0] for row in remote.splitlines()]: raise ValueError('Remote tag must already point to HEAD')
    token = subprocess.check_output(['gh', 'auth', 'token'], text=True).strip()
    release = Release(cfg=cfg, token=token)
    draft = await release.gh.create_release(tag_name=tag, branch=head, name=f'{cfg.data['project']['name']} {cfg.version}',
        body=release.latest_notes(), draft=True, files=artifacts)
    if publish:
        draft = await release.gh.repos.update_release(release_id=draft.id, draft=False,
            make_latest='true' if latest else 'false')
    print(draft.html_url)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('artifacts', nargs='+', type=Path)
    parser.add_argument('--tag')
    parser.add_argument('--latest', action='store_true')
    parser.add_argument('--publish', action='store_true', help='Publish after all artifacts have uploaded')
    args = vars(parser.parse_args())
    asyncio.run(publish(**args))


if __name__ == '__main__': main()
