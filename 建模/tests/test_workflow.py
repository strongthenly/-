import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('workflow',ROOT/'tools/workflow.py')
w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)

class WorkflowTest(unittest.TestCase):
    def test_install_preserves_existing_user_skill(self):
        with tempfile.TemporaryDirectory() as t:
            target=w.install(Path(t)/'.agents/skills')
            self.assertTrue((target/'references/prediction.md').is_file())
            (target/'SKILL.md').write_text('user changes',encoding='utf-8')
            with self.assertRaises(FileExistsError):w.install(Path(t)/'.agents/skills')
            self.assertEqual((target/'SKILL.md').read_text(encoding='utf-8'),'user changes')

    def test_project_is_unrun_and_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as t:
            p=w.initialize(Path(t)/'含空格 project')
            evidence=json.loads((p/'results/evidence.json').read_text(encoding='utf-8'))
            self.assertTrue(evidence['example_only'])
            self.assertIsNone(evidence['claims'][0]['method']['value'])
            self.assertTrue((p/'latex/smoke.tex').is_file())
            with self.assertRaises(FileExistsError):w.initialize(p)

    def test_references_survive_installation(self):
        with tempfile.TemporaryDirectory() as t:
            p=w.install(t)
            for file in p.rglob('*.md'):
                for link in re.findall(r'\]\(([^)]+)\)',file.read_text(encoding='utf-8')):
                    if '://' not in link:self.assertTrue((file.parent/link).exists(),link)

    def test_doctor_is_available_without_optional_packages(self):
        report=w.doctor()
        self.assertIn('python',report)
        self.assertIn('xelatex',report['commands'])

if __name__=='__main__':unittest.main()
