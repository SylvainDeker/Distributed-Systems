import pytest
import smtplib

# pytest -s -q --tb=no

# function, class, module, package(experimental) or session.
@pytest.fixture(scope="function")
def smtp_connection():
    smtp_connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
    yield smtp_connection  # provide the fixture value
    print("teardown smtp")
    smtp_connection.close()

# By using a yield statement instead of return, all the code
#  after the yield statement serves as the teardown code

# equivalent to:
# @pytest.fixture(scope="module")
# def smtp_connection():
#     with smtplib.SMTP("smtp.gmail.com", 587, timeout=5) as smtp_connection:
#         yield smtp_connection  # provide the fixture value


# import contextlib
#
# import pytest
#
#
# @contextlib.contextmanager
# def connect(port):
#     ...  # create connection
#     yield
#     ...  # close connection
#
#
# @pytest.fixture
# def equipments():
#     with contextlib.ExitStack() as stack:
#         yield [stack.enter_context(connect(port)) for port in ("C1", "C3", "C28")]
