import pandas as pd
import numpy as np

def getSubjecBasicStats(data, subjectID, interest_columns):
  """
  - data: DataFrame with the data
  - subjectID: int with the subjectID
  - interest_columns: list of strings with the columns names to get the stats
  """

  ##grouping data by subject
  grouped = data.groupby("subject_id")
  return grouped.get_group(subjectID)[interest_columns].describe()

  ##you can make the same doing
  # filter = data.loc[:,"subject_id"] == subjectID
  # data_filtered = data.loc[filter]

  # return data_filtered[interest_columns].describe()


def getAngles(x,y, limits = 360):
  """
  - x: array with the x values in cartesian coordinates
  - y: array with the y values in cartesian coordinates
  - limits: int with the limits to convert the angles

  return: array with the angles in degrees
  """
  return (np.arctan2(y, x) * 180 / np.pi) % limits

def limitingAngles(angles, bottom=-180, top=180):
    """
    Angles: Array with the angles between 0 and 359 degrees
    
    The idea is to transfrom the angles between bottom and top degrees
    """
    return (angles + 180) % 360 - 180

def gettingMADiffAngles(dataframe, trials_window = 10, divided_by = None,
                        replace_nan = "mean"):
    """
    Getting the moving average of the diff_angles

    Args:
    - dataframe: dataframe with the data
    - trials_window: int with the number of trials to average
    """
    ##getting the MA for each subjetc_id and rund_id over the trials (trial_index column) using the diff_angles column
    ##save the data in a dictionary with keys as (subject_id, run_id)

    ##divided_by should be None, or "motion_coherence" or "prior_std", if not, raise and value error
    if divided_by not in [None, "motion_coherence", "prior_std"]:
        raise ValueError("divided_by should be None, 'motion_coherence' or 'prior_std'")
    
    ##replace_nan should be "mean" or "zero", if not, raise and value error
    if replace_nan not in ["mean", "zero"]:
        raise ValueError("replace_nan should be 'mean' or 'zero'")

    if divided_by is None:
        ma_diff_angles = {}
        for subjetc_id in dataframe["subject_id"].unique():
            for run_id in dataframe["run_id"].unique():
                filter = (dataframe["subject_id"] == subjetc_id) & (dataframe["run_id"] == run_id)
                ma_diff_angles[(subjetc_id, run_id)] = dataframe.loc[filter, "diff_angles"].rolling(trials_window).mean()
                ##replace nan
                if replace_nan == "mean":
                    ma_diff_angles[(subjetc_id, run_id)] = ma_diff_angles[(subjetc_id, run_id)].fillna(ma_diff_angles[(subjetc_id, run_id)].mean())
                if replace_nan == "zero":
                    ma_diff_angles[(subjetc_id, run_id)] = ma_diff_angles[(subjetc_id, run_id)].fillna(0)
                #reset the index
                ma_diff_angles[(subjetc_id, run_id)] = ma_diff_angles[(subjetc_id, run_id)].reset_index(drop=True)

        return ma_diff_angles
    
    elif divided_by == "motion_coherence":
        ##getting the MA for each subjetc_id and rund_id over the trials (trial_index column)
        ## using the diff_angles column
        ##save the data in a dictionary with keys as (subject_id, run_id, motion_coherence)
        ma_diff_angles = {}
        for subjetc_id in dataframe["subject_id"].unique():
            for run_id in dataframe["run_id"].unique():
                for motion_coherence in dataframe["motion_coherence"].unique():
                    filter = (dataframe["subject_id"] == subjetc_id) & (dataframe["run_id"] == run_id) & (dataframe["motion_coherence"] == motion_coherence)
                    ma_diff_angles[(subjetc_id, run_id, motion_coherence)] = dataframe.loc[filter, "diff_angles"].rolling(trials_window).mean()
                    ##replace nan
                    if replace_nan == "mean":
                        ma_diff_angles[(subjetc_id, run_id, motion_coherence)] = ma_diff_angles[(subjetc_id, run_id, motion_coherence)].fillna(ma_diff_angles[(subjetc_id, run_id, motion_coherence)].mean())
                    if replace_nan == "zero":
                        ma_diff_angles[(subjetc_id, run_id, motion_coherence)] = ma_diff_angles[(subjetc_id, run_id, motion_coherence)].fillna(0)
                    #reset the index
                    ma_diff_angles[(subjetc_id, run_id, motion_coherence)] = ma_diff_angles[(subjetc_id, run_id, motion_coherence)].reset_index(drop=True)

        return ma_diff_angles
    
    elif divided_by == "prior_std":
        ##getting the MA for each subjetc_id and rund_id over the trials (trial_index column)
        ## using the diff_angles column
        ##save the data in a dictionary with keys as (subject_id, run_id, prior_std)
        ma_diff_angles = {}
        for subjetc_id in dataframe["subject_id"].unique():
            for run_id in dataframe["run_id"].unique():
                for prior_std in dataframe["prior_std"].unique():
                    filter = (dataframe["subject_id"] == subjetc_id) & (dataframe["run_id"] == run_id) & (dataframe["prior_std"] == prior_std)
                    ma_diff_angles[(subjetc_id, run_id, prior_std)] = dataframe.loc[filter, "diff_angles"].rolling(trials_window).mean()
                    ##replace nan with
                    if replace_nan == "mean":
                        ma_diff_angles[(subjetc_id, run_id, prior_std)] = ma_diff_angles[(subjetc_id, run_id, prior_std)].fillna(ma_diff_angles[(subjetc_id, run_id, prior_std)].mean())
                    if replace_nan == "zero":
                        ma_diff_angles[(subjetc_id, run_id, prior_std)] = ma_diff_angles[(subjetc_id, run_id, prior_std)].fillna(0)
                    ##reset the index
                    ma_diff_angles[(subjetc_id, run_id, prior_std)] = ma_diff_angles[(subjetc_id, run_id, prior_std)].reset_index(drop=True)

        return ma_diff_angles

##Liquitaine function
def get_cartesian_to_deg(
    x: np.ndarray, y: np.ndarray, signed: bool
) -> np.ndarray:
    """convert cartesian coordinates to
    angles in degree
    Args:
        x (np.ndarray): x coordinate
        y (np.ndarray): y coordinate
        signed (boolean): True (signed) or False (unsigned)
    Usage:
        .. code-block:: python
            import numpy as np
            from bsfit.nodes.cirpy.utils import get_cartesian_to_deg
            x = np.array([1, 0, -1, 0])
            y = np.array([0, 1, 0, -1])
            degree = get_cartesian_to_deg(x,y,False)
            # Out: array([  0.,  90., 180., 270.])
    Returns:
        np.ndarray: angles in degree
    """
    # convert to radian (ignoring divide by 0 warning)
    with np.errstate(divide="ignore"):
        degree = np.arctan(y / x)

    # convert to degree and adjust based
    # on quadrant
    for ix in range(len(x)):
        if (x[ix] >= 0) and (y[ix] >= 0):
            degree[ix] = degree[ix] * 180 / np.pi
        elif (x[ix] == 0) and (y[ix] == 0):
            degree[ix] = 0
        elif x[ix] < 0:
            degree[ix] = degree[ix] * 180 / np.pi + 180
        elif (x[ix] >= 0) and (y[ix] < 0):
            degree[ix] = degree[ix] * 180 / np.pi + 360

    # if needed, convert signed to unsigned
    if not signed:
        degree[degree < 0] = degree[degree < 0] + 360
    return degree