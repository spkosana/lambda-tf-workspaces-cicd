"""
This Module is for testing handler code

"""

# pylint: disable=import-error,no-name-in-module

from handler.handler import lambda_handler, get_cleaned_data


def test_get_cleaned_data():
    """
    Tests the get_cleaned_data function

    Verifies that the length of the list returned by get_cleaned_data is
    equal to the number argument passed to the function.

    """
    number = 1
    data = get_cleaned_data(number)
    assert number == len(data)


# # Commenting for testing failure case of coverage
def test_lambda_function_data(s3_client):
    """_summary_

    Args:
        create_bucket1 (s3 fixture): Fixture that is creating mock bucket
    Assets:
        number given in the event with user_count from the lambda response
    """

    bucket_name = "sample-test"
    number = 10
    s3_client.create_bucket(Bucket=bucket_name)
    event = {"bucket_name": bucket_name, "number": number}
    context = {}
    response = lambda_handler(event, context)
    users_count = response.get("users_count")

    assert number == users_count


# pylint: disable=logging-fstring-interpolation


def test_lambda_exception_status_code(s3_client):
    """_summary_

    Args:
        s3 (_type_): _description_
    """
    number = 10
    s3_client.create_bucket(Bucket="sample-test-1")
    bucket_name = "sample-test-2"
    event = {"bucket_name": bucket_name, "number": number}
    response = lambda_handler(event, context={})
    status_code = response.get("status_code")
    assert status_code == 404


def test_lambda_exception_file_location(s3_client):
    """_summary_

    Args:
        s3 (_type_): _description_
    """
    number = 10
    s3_client.create_bucket(Bucket="sample-test-1")
    bucket_name = "sample-test-2"
    event = {"bucket_name": bucket_name, "number": number}
    response = lambda_handler(event, context={})
    file_location = response.get("file_location")
    assert file_location is None
