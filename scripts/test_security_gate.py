import tempfile
import unittest
from pathlib import Path
import security_gate as gate


class PublicReleaseSecurityTests(unittest.TestCase):
    def test_private_paths_are_rejected_and_public_case_study_is_allowed(self):
        for path in ['.env', 'keys/account.pem', 'Latest_CV_2026/cv.html',
                     '98_Maintenance/generate_mytvs_exit_pack.py', 'node_modules/pkg/index.js']:
            with self.subTest(path=path):
                self.assertTrue(gate.path_findings(path))
        self.assertFalse(gate.path_findings('docs/Synthetic_Case_Study.pdf'))
        self.assertFalse(gate.path_findings('.env.example'))

    def test_sensitive_values_are_detected_without_being_returned(self):
        token = 'ghp_' + 'A' * 36
        value = 'personal' + '@' + 'real-mail.invalid'
        result = gate.text_findings('first line\n' + token + '\n' + value)
        self.assertIn(('GitHub token', 2), result)
        self.assertIn(('non-example email', 3), result)
        self.assertNotIn(token, str(result))
        self.assertNotIn(value, str(result))

    def test_synthetic_addresses_and_package_versions_are_not_private_emails(self):
        self.assertEqual([], gate.text_findings('staff@example.com staff@apd.example staff@apexprecision.test chart.js@4.4.7'))

    def test_remote_and_outside_scripts_are_blocked_but_existing_local_script_works(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'app.js').write_text('console.log(1)')
            source = root / 'index.html'
            self.assertEqual([], gate.script_findings('<script src="app.js"></script>', source, root))
            for target in ['https://cdn.example.test/app.js', '//cdn.example.test/app.js',
                           'data:text/javascript,1', '../app.js', '%2e%2e/app.js', 'missing.js']:
                with self.subTest(target=target):
                    self.assertTrue(gate.script_findings('<script src="' + target + '"></script>', source, root))


if __name__ == '__main__':
    unittest.main()
