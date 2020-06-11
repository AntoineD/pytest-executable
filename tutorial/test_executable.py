# Copyright 2020, CS Systemes d'Information, http://www.c-s.fr
#
# This file is part of pytest-executable
#     https://www.github.com/CS-SI/pytest-executable
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test modules for pytest-executable."""


import pytest


def test_runner(runner):
    """Check the runner execution.

    An OK process execution shall return the code 0.

    Args:
        runner: Fixture to run the runner script.
    """
    assert runner.run() == 0


def test_logs(output_path):
    """Check the executable log files.

    The error log shall be empty and the output log shall not be empty.

    Args:
        output_path: Path to the current test output directory.
    """
    assert (
        output_path / "executable.stderr"
    ).stat().st_size == 0, "stderr file shall be empty"


def test_regression(output_path, tolerances, regression_file_path):
    """Check the result files against the reference files.

    The reference files shall be defined in the test-settings.yaml, pytest will
    execute this function for each of the reference files found in the
    reference directory of the current test case.

    Args:
        output_path: Path to the current test output directory.
        tolerances: Dictionnary of tolerances.
        regression_file_path: Relative and absolute paths to a reference file.
    """
    pytest.importorskip("pandas", reason="skip test requiring pandas")

    import pandas as pd

    ref_data = pd.read_csv(regression_file_path.absolute)
    new_file = output_path / regression_file_path.relative
    new_data = pd.read_csv(new_file)

    for data_name in ref_data.keys():
        tolerance = tolerances[data_name]
        assert new_data[data_name].to_numpy() == pytest.approx(
            ref_data[data_name].to_numpy(), rel=tolerance.rel, abs=tolerance.abs
        )
