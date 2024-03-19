from datetime import date, datetime

import allure
import os
import sys

import pandas as pd
import pytest
import wandb
from dotenv import load_dotenv

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent.replace('regression-test', ''))

from common_src.utils.Screenshot import add_attachment

load_dotenv()


def convert_data_of_date(file, column):
    df = pd.read_csv(file)
    column_to_convert = column
    df[column_to_convert] = pd.to_datetime(df[column_to_convert], format="%Y-%m-%d %H:%M").dt.strftime("%Y-%m-%d %H:%M")
    df.to_csv(file, index=False)


def convert_data_of_numeric(file, column):
    df = pd.read_csv(file)
    column_to_convert = column
    # Convert to integers (assuming no decimals)
    df[column_to_convert] = pd.to_numeric(df[column_to_convert], errors='coerce')  # Handle non-numeric values
    df.to_csv(file, index=False)


# @pytest.mark.skip(reason="Feature is being updated")
@allure.title("NANL Upload Speed Summary")
def test_print_out_performance_nanl_metric():
    file_name = os.getenv("SPEED_PERFORMANCE_FILE")
    add_attachment(file_name, "average speed summary")
    cur_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    wandb.init(project='NANL Report',
               name=f"{cur_date} - NANL Upload Speed Report")
    convert_data_of_date(file_name, "Time")
    convert_data_of_numeric(file_name, "Average Upload Speed")
    df_fix = pd.read_csv(file_name)
    my_table = wandb.Table(dataframe=df_fix)
    wandb.log({"Average Upload Speed Of NANL": my_table})
    wandb.finish()
