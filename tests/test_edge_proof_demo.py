import unittest

from examples.edge_proof_demo import (
    CANDIDATES,
    purged_splits,
    run_demo,
    select_on_train,
    synthetic_panel,
)


class EdgeProofDemoTests(unittest.TestCase):
    def test_generation_is_deterministic(self) -> None:
        self.assertEqual(synthetic_panel(seed=23), synthetic_panel(seed=23))
        self.assertNotEqual(synthetic_panel(seed=23), synthetic_panel(seed=24))

    def test_splits_leave_a_horizon_aware_gap(self) -> None:
        max_horizon = max(candidate.horizon for candidate in CANDIDATES)
        splits = purged_splits(
            720,
            train_end=360,
            validation_end=540,
            max_horizon=max_horizon,
            embargo=5,
        )
        self.assertLess(max(splits["train"]) + max_horizon, min(splits["validation"]))
        self.assertLess(max(splits["validation"]) + max_horizon, min(splits["test"]))

    def test_selection_does_not_depend_on_future_rows(self) -> None:
        panel = synthetic_panel(seed=31)
        train = list(range(200))
        original = select_on_train(panel, train)

        altered_future = panel[:200] + synthetic_panel(n=len(panel) - 200, seed=999)
        self.assertEqual(original, select_on_train(altered_future, train))

    def test_demo_reports_oos_and_stress_results(self) -> None:
        result = run_demo()
        self.assertEqual(result["selected_on"], "TRAIN")
        self.assertIn("validation", result)
        self.assertIn("test", result)
        self.assertIn("test_stress", result)
        self.assertTrue(result["checks"]["synthetic_data_only"])
        self.assertFalse(result["checks"]["selection_uses_test"])


if __name__ == "__main__":
    unittest.main()

