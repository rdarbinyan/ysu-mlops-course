import json

import pytest
from tests.test_api import SECONDARY_VARIABLES_TO_RENAME
from gb_regressor.processing.data_management import load_dataset

from .compare import compare_differences


@pytest.mark.differential
def test_model_prediction_differentials(client):
    test_inputs_df = load_dataset(file_name="test.csv")
    old_model_inputs_df = test_inputs_df.rename(
        columns=SECONDARY_VARIABLES_TO_RENAME
    )

    new_model_response = client.post(
        "v1/predictions/gb", json=test_inputs_df.to_dict(orient="records")
    )
    new_model_predictions = json.loads(new_model_response.data)["predictions"]

    old_model_response = client.post(
        "v1/predictions/lasso",
        json=old_model_inputs_df.to_dict(orient="records"),
    )
    old_model_predictions = json.loads(old_model_response.data)["predictions"]

    # We just pass in the first 10 rows as a sample
    compare_differences(
        expected_predictions=new_model_predictions[:10],
        actual_predictions=old_model_predictions[:10],
        # you would adjust the rel_tol level parameter on your model.
        # right now this is extremely permissive of variation.
        rel_tol=0.2,
    )
