import unittest
from sanitizer import clean_and_normalize_sensor_readings


class TestCleanAndNormalize(unittest.TestCase):

    def test_mixed_valid_invalid(self):
        data = ["12.5", None, -5, "bad_data", 550.0, 42, "0"]
        result = clean_and_normalize_sensor_readings(data)
        self.assertEqual(result, [12.5, 500.0, 42.0, 0.0])

    def test_empty_list(self):
        result = clean_and_normalize_sensor_readings([])
        self.assertEqual(result, [])

    def test_none_as_input(self):
        result = clean_and_normalize_sensor_readings(None)
        self.assertEqual(result, [])

    def test_all_invalid(self):
        data = [None, "error", -1, -999.0, "N/A"]
        result = clean_and_normalize_sensor_readings(data)
        self.assertEqual(result, [])

    def test_clipping_above_500(self):
        data = [499.9, 500.0, 500.1, 1000.0]
        result = clean_and_normalize_sensor_readings(data)
        self.assertEqual(result, [499.9, 500.0, 500.0, 500.0])

    def test_zero_is_kept(self):
        data = [0, 0.0, "0"]
        result = clean_and_normalize_sensor_readings(data)
        self.assertEqual(result, [0.0, 0.0, 0.0])

    def test_string_numbers(self):
        data = ["10", "20.5", "30"]
        result = clean_and_normalize_sensor_readings(data)
        self.assertEqual(result, [10.0, 20.5, 30.0])

    def test_only_negatives(self):
        data = [-1, -50, -0.1]
        result = clean_and_normalize_sensor_readings(data)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
