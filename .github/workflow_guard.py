"Standalone source-branch guards; distributed from ease-ws/scripts/workflow_guard.py."
import argparse, hashlib, json, os, shlex, subprocess, sys
from pathlib import Path


POLICY_SHA256 = '6c3b94bf9ab1b792f7ce26d31987bdfaefcd67421678a84bfe9b5e2bc1d3503c'
SOURCE_BRANCHES = ('development', 'main')
DEPLOYMENT_BRANCHES = ('deployed/dev', 'deployed/prod')


def git(repo, *args): return subprocess.run(['git','-C',str(repo),*args],check=True,capture_output=True,text=True).stdout.strip()


def validate_commit(branch):
    if not branch or branch in SOURCE_BRANCHES:
        raise ValueError('Commit on a feature branch; main and development are protected integration branches')


def validate_push(records):
    for record in records.splitlines():
        _, _, destination, previous = record.split()
        if destination in {f'refs/heads/{name}' for name in (*SOURCE_BRANCHES,*DEPLOYMENT_BRANCHES)}:
            raise ValueError(f'{destination}: use reviewed pull requests; deployment refs belong to rsc')
        if destination.startswith('refs/tags/') and previous != '0'*40:
            raise ValueError('Published tags must not be overwritten or deleted')


def check_policy(repo):
    if hashlib.sha256((Path(repo)/'WORKFLOW.md').read_bytes()).hexdigest() != POLICY_SHA256:
        raise ValueError('Workflow policy differs from the central policy; synchronise it from ease-ws')
    event = os.environ.get('GITHUB_EVENT_PATH')
    if not event: return
    request = json.loads(Path(event).read_text()).get('pull_request')
    if request and request['base']['ref']=='main':
        head = request['head']['ref']
        if head!='development' and not head.startswith('pr/hotfix/'):
            raise ValueError('Promote development to main; emergency fixes use pr/hotfix/* and return to development')


def install(repo):
    repo = Path(git(repo,'rev-parse','--show-toplevel'))
    if not (repo/'.github/workflow_guard.py').is_file(): raise ValueError('Synchronise the workflow policy before installing hooks')
    common = Path(git(repo,'rev-parse','--path-format=absolute','--git-common-dir'))
    directory = common/'ease-workflow'
    hooks, state = directory/'hooks', directory/'previous.json'
    previous = Path(git(repo,'rev-parse','--path-format=absolute','--git-path','hooks'))
    if previous != hooks:
        if state.exists():
            saved = json.loads(state.read_text())
            if saved['hooks'] != str(previous): raise ValueError('Hook configuration changed; review the saved hook chain before reinstalling')
        else:
            directory.mkdir(parents=True,exist_ok=True)
            state.write_text(json.dumps(dict(hooks=str(previous)),indent=2)+'\n')
    hooks.mkdir(parents=True,exist_ok=True)
    (directory/'guard.py').write_text((repo/'.github/workflow_guard.py').read_text())
    native = Path(json.loads(state.read_text())['hooks'])
    names = {'pre-commit','pre-push','pre-merge-commit'}
    if native.is_dir(): names.update(path.name for path in native.iterdir() if path.is_file() and '.' not in path.name and os.access(path,os.X_OK))
    for name in sorted(names):
        target = hooks/name
        script = '#!/bin/sh\n# ease-workflow source guards\n'
        script += 'repo=$(git rev-parse --show-toplevel) || exit\n'
        script += f'exec {shlex.quote(sys.executable)} {shlex.quote(str(directory/"guard.py"))} hook {name} "$@"\n'
        if target.exists() and 'ease-workflow source guards' not in target.read_text():
            raise ValueError(f'Refusing to replace an unknown hook: {target}')
        target.write_text(script)
        target.chmod(0o755)
    git(repo,'config','core.hooksPath',str(hooks))


def run_hook(repo, name, args):
    records = sys.stdin.read() if name=='pre-push' else None
    if name in ('pre-commit','pre-merge-commit'): validate_commit(git(repo,'branch','--show-current'))
    elif name=='pre-push': validate_push(records)
    common = Path(git(repo,'rev-parse','--path-format=absolute','--git-common-dir'))
    previous = Path(json.loads((common/'ease-workflow/previous.json').read_text())['hooks'])/name
    if previous.is_file() and os.access(previous,os.X_OK): subprocess.run([str(previous),*args],cwd=repo,input=records,text=True,check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=['install','check','hook'])
    parser.add_argument('arguments',nargs='*')
    args = parser.parse_args()
    repo = Path(git(Path.cwd(),'rev-parse','--show-toplevel'))
    try:
        if args.operation=='install': install(repo)
        elif args.operation=='check': check_policy(repo)
        else: run_hook(repo,args.arguments[0],args.arguments[1:])
    except (ValueError,OSError,subprocess.CalledProcessError) as error: parser.exit(1,str(error)+'\n')


if __name__=='__main__': main()
