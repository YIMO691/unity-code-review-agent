from __future__ import annotations

from pathlib import Path
import unittest

from src.scanner import load_rules, scan_file


class ScannerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        _, cls.rules = load_rules(cls.root / "rules" / "unity_rules.json")
        cls.fixtures = cls.root / "tests" / "fixtures"

    def scan_fixture(self, name: str):
        return scan_file(self.fixtures / name, self.rules)

    def test_example_hits_all_v0_rules(self):
        findings = scan_file(self.root / "examples" / "InventoryView.cs", self.rules)
        rule_ids = {finding.rule_id for finding in findings}

        self.assertTrue({"U001", "U002", "U003", "U004", "U005"}.issubset(rule_ids))

    def test_empty_file_has_no_findings(self):
        self.assertEqual(self.scan_fixture("empty.cs"), [])

    def test_class_only_has_no_findings(self):
        self.assertEqual(self.scan_fixture("class_only.cs"), [])

    def test_get_component_in_awake_is_not_update_finding(self):
        self.assertEqual(self.scan_fixture("get_component_awake.cs"), [])

    def test_get_component_in_update_hits_u001(self):
        findings = self.scan_fixture("get_component_update.cs")
        self.assertEqual([finding.rule_id for finding in findings], ["U001"])

    def test_linq_in_start_has_no_findings(self):
        findings = self.scan_fixture("linq_start.cs")
        self.assertEqual(findings, [])

    def test_linq_in_update_hits_u002(self):
        findings = self.scan_fixture("linq_update.cs")
        self.assertEqual([finding.rule_id for finding in findings], ["U002"])

    def test_linq_in_lateupdate_hits_u002(self):
        findings = self.scan_fixture("linq_lateupdate.cs")
        self.assertEqual([finding.rule_id for finding in findings], ["U002"])

    def test_r3_reactive_where_is_not_linq_finding(self):
        findings = self.scan_fixture("r3_reactive_chain.cs")
        self.assertNotIn("U002", {finding.rule_id for finding in findings})

    def test_r3_file_exclusion_only_affects_u002(self):
        findings = self.scan_fixture("r3_file_still_hits_u001.cs")
        self.assertEqual([finding.rule_id for finding in findings], ["U001"])

    def test_add_listener_still_hits_when_remove_exists(self):
        findings = self.scan_fixture("add_listener_removed.cs")
        self.assertEqual([finding.rule_id for finding in findings], ["U003"])

    def test_addressables_load_with_release_has_no_u005(self):
        findings = self.scan_fixture("addressables_released.cs")
        self.assertNotIn("U005", {finding.rule_id for finding in findings})

    def test_addressables_load_without_release_hits_u005(self):
        findings = self.scan_fixture("addressables_unreleased.cs")
        self.assertEqual([finding.rule_id for finding in findings], ["U005"])

    def test_commented_get_component_has_no_findings(self):
        self.assertEqual(self.scan_fixture("commented_get_component.cs"), [])

    def test_event_subscription_hits_but_accumulation_does_not(self):
        findings = self.scan_fixture("event_subscription_vs_accumulation.cs")
        rule_ids = {finding.rule_id for finding in findings}

        self.assertEqual(rule_ids, {"U003"})
        self.assertTrue(all("hitCount +=" not in finding.code for finding in findings))

    def test_non_cs_file_is_rejected(self):
        from src.scanner import collect_cs_files

        with self.assertRaises(ValueError):
            collect_cs_files(self.root / "README.md")


if __name__ == "__main__":
    unittest.main()
