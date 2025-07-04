import pandas as pd
from pathlib import Path
from django.conf import settings


def load_data(name: str) -> pd.DataFrame:
    """
    Loads a CSV file from the project's data folder and
    returns its content as a pandas DataFrame.
    """
    data_path = Path(settings.PROJECT_DIR) / "data" / name
    try:
        return pd.read_csv(data_path)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file {name} could not be found at {data_path}.")


def get_params(forms: list, mapping: dict) -> dict:
    """
    Extracts parameters from a list of forms.
    If a feature was selected, a parameter mapping the
    function name to True is added.
    """
    result = {}
    for form in forms:
        if form.is_valid():
            if form.cleaned_data["selected"]:
                # Get params from form
                params = {
                    key: val
                    for key, val in form.cleaned_data.items()
                    if key != "selected"
                }
                # Add function name as param for (un)selecting
                params.update({mapping[type(form)]: True})
                result.update(params)
            else:
                result.update({mapping[type(form)]: False})
    return result


def get_match_for_seq(data: pd.DataFrame, seq: str) -> dict:
    """
    Matches the given sequence to a row of computed sequences.
    Returns the number of matches and the found features as dict.
    """
    matched = data[data["Sequence"] == seq]
    num_matches = len(matched)
    matched = matched.drop(
        columns=[
            "Sample",
            "Protein ID",
            "Intensity",
            "PEP",
        ],
        errors="ignore",
    )
    if not matched.empty:
        return (num_matches, matched.iloc[0].to_dict())
    else:
        return (0, {})
