import pytest


@pytest.fixture
def unused_import_code():
    return "import os\n"


@pytest.fixture
def clean_code():
    return "x = 1\n"


@pytest.fixture
def unformatted_code():
    return "x=1\n"


@pytest.fixture
def multi_violation_code():
    return "import os\nimport sys\nx=1\n"


@pytest.fixture
def fixable_code():
    """Code with unused import (fixable) and used import."""
    return "import os\nimport sys\nprint(sys.path)\n"
