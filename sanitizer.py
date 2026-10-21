def clean_and_normalize_sensor_readings(readings):
    if readings is None:
        return []

    if not isinstance(readings, list):
        return []

    if len(readings) == 0:
        return []

    cleaned = []

    for item in readings:
       
        if item is None:
            continue

       
        try:
            value = float(item)
        except (ValueError, TypeError):
           
            continue

       
        if value < 0:
            continue

       
        if value > 500.0:
            value = 500.0

        cleaned.append(value)

    return cleaned



if __name__ == "__main__":
    print("=" * 55)
    print("  Section 1: Clean and Normalize Sensor Readings")
    print("=" * 55)

    print("\nTest 1 - Mixed valid and invalid inputs:")
    test1_input = ["12.5", None, -5, "bad_data", 550.0, 42, "0"]
    test1_result = clean_and_normalize_sensor_readings(test1_input)
    test1_expected = [12.5, 500.0, 42.0, 0.0]
    print(f"  Input:    {test1_input}")
    print(f"  Expected: {test1_expected}")
    print(f"  Got:      {test1_result}")
    if test1_result == test1_expected:
        print("  Result:   PASS")
    else:
        print("  Result:   FAIL")

    print("\nTest 2 - Empty list:")
    test2_input = []
    test2_result = clean_and_normalize_sensor_readings(test2_input)
    test2_expected = []
    print(f"  Input:    {test2_input}")
    print(f"  Expected: {test2_expected}")
    print(f"  Got:      {test2_result}")
    if test2_result == test2_expected:
        print("  Result:   PASS")
    else:
        print("  Result:   FAIL")

    print("\nTest 3 - All invalid entries:")
    test3_input = [None, "error", -1, -999.0, "N/A", "null"]
    test3_result = clean_and_normalize_sensor_readings(test3_input)
    test3_expected = []
    print(f"  Input:    {test3_input}")
    print(f"  Expected: {test3_expected}")
    print(f"  Got:      {test3_result}")
    if test3_result == test3_expected:
        print("  Result:   PASS")
    else:
        print("  Result:   FAIL")

    print("\n" + "=" * 55)

    all_pass = (
        test1_result == test1_expected and
        test2_result == test2_expected and
        test3_result == test3_expected
    )
    if all_pass:
        print("  All 3 tests passed!")
    else:
        print("  Some tests failed, check above.")
    print("=" * 55)
