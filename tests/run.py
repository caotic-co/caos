import unittest
from io import StringIO
from caos._internal.console import red_text, green_text


def main() -> None:
    _ERROR_FORMAT = "[ERROR] Exception Type: '{ex_type}' -> {ex_message}"

    try:
        from tests import suite
        out_stream: StringIO = StringIO()
        test_runner: unittest.TextTestRunner = unittest.TextTestRunner(stream=out_stream, verbosity=3)
        tests_result: unittest.result.TestResult = test_runner.run(suite)

        if tests_result.failures or tests_result.errors:
            print(red_text(out_stream.getvalue()))

        if tests_result.failures:
            print(red_text("[ERROR] The execution finished with failures"))

        if tests_result.errors:
            print(red_text("[ERROR] The execution finished with errors"))

        if tests_result.failures or tests_result.errors:
            exit(1)

        print(green_text(out_stream.getvalue()))
        print(green_text("[SUCCESS] Tests execution completed successfully"))

    except Exception as e:
        print(red_text(_ERROR_FORMAT.format(
            ex_type=type(e).__name__,
            ex_message=str(e)
        )))
        exit(1)
    exit(0)
