"""
This module contains code which generated users and write to s3 
"""

import logging
from datetime import date, datetime
from typing import List, Dict
from pprint import pprint
from faker import Faker
import boto3
import awswrangler as wr
import pandas as pd


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


FAKE = Faker()


# pylint: disable=line-too-long
# pylint: disable=logging-fstring-interpolation
def get_cleaned_data(number: int) -> List[Dict]:
    """
    Aim: To generate fake data for users based on the number given as input and gets cleaned data as output

    Args:
        number (int): Take a number to generate data


    Returns:
        List(dict): Return list of dictionaries
    """
    LOGGER.info(f"Given Number as input is {number = }")
    data = [FAKE.simple_profile() for _ in range(number)]
    cleaned_data = []
    for d in data:
        new = {}
        for k, v in d.items():
            if isinstance(v, date):
                new[k] = v.strftime("%Y-%m-%d")
            else:
                new[k] = v
        cleaned_data.append(new)
    return cleaned_data


# pylint: disable=logging-fstring-interpolation
# pylint: disable=broad-exception-caught
def lambda_handler(event, context) -> Dict:
    """
    Aim: Event recieves number and bucket name and generated data
         write to s3 bucket and returns the file location in output response

    Args:
        event (dict): Event has the values that are passed in the event
        context (dict): context has pre defined paramaters

    Returns:
        dict: Returns dictionary
    """
    LOGGER.info(f"Event Object: {event}")
    LOGGER.info(f"Context Object: {context}")
    session = boto3.session.Session()
    number = event.get("number")
    bucket_name = event.get("bucket_name")
    status_code = 0
    cleaned = get_cleaned_data(number)
    df = pd.DataFrame(data=cleaned)

    try:
        now_str = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"users_{now_str}.csv"
        file_location = f"s3://{bucket_name}/cicd/{file_name}"
        s3_write_response = wr.s3.to_csv(
            df, path=file_location, boto3_session=session, index=False
        )
        LOGGER.info(f"wrangler write response {s3_write_response = }")
        pprint(s3_write_response)
        status_code = 200
    except Exception as e:
        LOGGER.error(e)
        file_location = None
        status_code = 404
    finally:
        response = {
            "status_code": status_code,
            "file_location": file_location,
            "users_count": len(cleaned),
        }
    return response
