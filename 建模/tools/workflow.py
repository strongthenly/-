"""Portable, standard-library helpers. Never overwrite an existing skill/project."""
import argparse
import importlib.metadata
import json
import platform
from pathlib import Path
import shutil
import sys

PACKAGE = Path(__file__).resolve().parents[1]
SKILL = PACKAGE / '.agents/skills/gpt6-math-modeling'

def install(destination):
    target = Path(destination).expanduser().resolve() / SKILL.name
    if target.exists():
        raise FileExistsError(f'Skill already exists: {target}; compare and back up before updating.')
    if not (SKILL / 'SKILL.md').is_file():
        raise FileNotFoundError('Copy the entire modeling package, not only this script.')
    shutil.copytree(SKILL, target)
    return target

def initialize(destination):
    target = Path(destination).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=False)
    for name in ['data/raw','data/processed','code','results','figs','latex','deliverables','docs']:
        (target/name).mkdir(parents=True)
    (target/'HANDOFF.md').write_text(
        '# 建模交接\n\n状态：尚未运行。\n\n'
        '- 用户目标与范围：待填\n- 原题与数据来源：待填\n- 当前产物：无\n'
        '- 冻结结果与哈希：无\n- 完成的验证：无\n- 未完成与原因：待填\n'
        '- 下一步：读取原题并核对附件\n- 复现命令/环境：待填\n'
        '- 会覆盖结果的脚本及外部数据依赖：待填\n', encoding='utf-8')
    shutil.copy2(SKILL/'assets/evidence.example.json',target/'results/evidence.json')
    shutil.copy2(SKILL/'assets/smoke.tex',target/'latex/smoke.tex')
    return target

def doctor():
    packages = {}
    for name in ['numpy','pandas','scipy','scikit-learn','statsmodels','xgboost','ortools','matplotlib','openpyxl','PyMuPDF']:
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    return {'python':platform.python_version(),'executable':sys.executable,
            'platform':platform.system(),'packages':packages,
            'commands':{name:shutil.which(name) for name in ['git','xelatex','pdftoppm']},
            'note':'Read-only inventory. Missing optional packages are not an instruction to install everything.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor')
    for name in ['init','install']:
        sub.add_parser(name).add_argument('destination')
    a=p.parse_args()
    if a.command=='doctor':print(json.dumps(doctor(),ensure_ascii=False,indent=2))
    elif a.command=='init':print(initialize(a.destination))
    else:print(install(a.destination))

if __name__=='__main__':
    main()
