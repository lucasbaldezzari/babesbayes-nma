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

def gettingDiffAnglesRate(diff_angles, trials_window = 20):
    """
    We get the diff_angles array and average the values in a window of trials_window

    Args:
    - diff_angles: array with the diff_angles
    - trials_window: int with the number of trials to average
    """

    ##getting the length of the array
    length = len(diff_angles)
    ##getting the number of windows
    windows = length//trials_window
    ##getting the diff_angles rate
    diff_angles_rate = np.zeros(windows)
    for i in range(windows):
        diff_angles_rate[i] = np.mean(diff_angles[i*trials_window:(i+1)*trials_window])
    return diff_angles_rate

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