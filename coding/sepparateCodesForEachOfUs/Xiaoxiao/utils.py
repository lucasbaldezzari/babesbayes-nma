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


def getAngles(x,y):
  """
  - x: array with the x values in cartesian coordinates
  - y: array with the y values in cartesian coordinates

  return: array with the angles in degrees
  """
  return np.arctan2(y, x) * 180 / np.pi