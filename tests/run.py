import unittest
from io import StringIO
from caos.style.console import red_text, green_text


def main() -> None:
    _ERROR_FORMAT = "[Exception Type: '{ex_type}'] -> {ex_message}"
    _SUCCESS_FORMAT = "[No errors found] -> {message}"

    try:
        from tests import suite
        out_stream: StringIO = StringIO()
        test_runner: unittest.TextTestRunner = unittest.TextTestRunner(stream=out_stream, verbosity=3)
        tests_result: unittest.runner.TextTestResult = test_runner.run(suite)

        if tests_result.failures or tests_result.errors:
            print(red_text(out_stream.getvalue()))

        if tests_result.failures:
            print(red_text("[The execution finished with failures]"))

        if tests_result.errors:
            print(red_text("[The execution finished with errors]"))

        if tests_result.failures or tests_result.errors:
            exit(1)

        print(green_text(out_stream.getvalue()))
        print(green_text(_SUCCESS_FORMAT.format(message="Tests execution completed successfully")))

    except Exception as e:
        print(red_text(_ERROR_FORMAT.format(
            ex_type=type(e).__name__,
            ex_message=str(e)
        )))
        exit(1)
    exit(0)
