import pyarrow.feather as feather
import pyarrow as pa
import pyarrow.parquet as pf
import pyarrow.csv as csv
import pandas as pd
import numpy as np
import os
from compute_features import produce_files, compute_features, compute_and_save

def motion_forecasting_get_data():
    '''
    Processes the motion forcasting files in the Argoverse 2 dataset. 
    The files are in a tabular format. This function converts features
    to numpy arrays and stacks those featires into a single array. 
    The function combines data from multiple parquet files and returns the
    matrix.

    The returned matrix has the following features and 
    in this order: timestep, position_x, position_y,
    velocity_x, velocity_y.

    NOTE: Currently the file locations are hardcoded. This can be updated in 
    later revisions.
    NOTE: The function extracts only motion forcasting sequences that are 
    the full 11 seconds long.
    '''

    #files = ['../argoverse_2_data/motion_forecasting/00010486-9a07-48ae-b493-cf4545855937/scenario_00010486-9a07-48ae-b493-cf4545855937.parquet',
    #         '../argoverse_2_data/motion_forecasting/00062a32-8d6d-4449-9948-6fedac67bfcd/scenario_00062a32-8d6d-4449-9948-6fedac67bfcd.parquet',
    #         '../argoverse_2_data/motion_forecasting/0006ca28-fcbb-4ae2-9d9e-951fa3b41c1c/scenario_0006ca28-fcbb-4ae2-9d9e-951fa3b41c1c.parquet',
    #         '../argoverse_2_data/motion_forecasting/0007df76-c9a2-47aa-83bf-3b2b414109c9/scenario_0007df76-c9a2-47aa-83bf-3b2b414109c9.parquet'
    #         ]


    # Incorporating the social features computation and combination with parquet file dta here.
    compute_and_save()

    dir = '../features/val'
    files = []
    for root, dirs, file in os.walk(dir, topdown = False):
        for name in file:
            print(name)
            files.append(os.path.join(root, name))


    print(files)

    # Empty array to combine processed data into one array.
    full_dataset = np.empty(shape = [0,9])

    for file in files:
      ## Each file contains catagorical and continious data. The complete list of features is:'observed',
      ## 'track_id', 'object_type', 'object_category', 'timestep', 'position_x', 'position_y', 'heading',
      ## 'velocity_x', 'Velocity_y', 'scenario_id', 'start_timestamp', 'end_timestamp', 'num_timestamps',
      ## 'focal_track_id', 'city'

      #motion_forecasting_data = pf.ParquetFile(file)
      motion_forecasting_data = pd.read_csv(file) 
      data_features = ['track_id', 'object_category', 'timestep', 'position_x', 'position_y', 'heading', 'velocity_x', 'velocity_y', 'MIN_DISTANCE_FRONT', 'MIN_DISTANCE_BACK', 'NUM_NEIGHBORS']
      #data_subset = motion_forecasting_data.read(columns = data_features)
      data_subset = motion_forecasting_data[data_features]
      track_id = data_subset['track_id'].to_numpy().reshape(len(data_subset), 1)
      object_category = data_subset['object_category'].to_numpy().reshape(len(data_subset), 1)
      timestep = data_subset['timestep'].to_numpy().astype(np.int32).reshape(len(data_subset), 1)
      position_x = data_subset['position_x'].to_numpy().reshape(len(data_subset), 1)
      position_y = data_subset['position_y'].to_numpy().reshape(len(data_subset), 1)
      heading = data_subset['heading'].to_numpy().reshape(len(data_subset), 1)
      velocity_x = data_subset['velocity_x'].to_numpy().reshape(len(data_subset), 1)
      velocity_y = data_subset['velocity_y'].to_numpy().reshape(len(data_subset), 1)
      min_distance_front = data_subset['MIN_DISTANCE_FRONT'].to_numpy().reshape(len(data_subset), 1)
      min_distance_back = data_subset['MIN_DISTANCE_BACK'].to_numpy().reshape(len(data_subset), 1)
      num_neighbors = data_subset['NUM_NEIGHBORS'].to_numpy().reshape(len(data_subset), 1)

      index = []
      for i in range(len(timestep)):
        if timestep[i] == 109:
          if timestep[i - 109] == 0:
            for l in range(i-109, i+1):
              #print(timestep[l])
              index.append(l)

      data_values = np.hstack((timestep, position_x, position_y, heading, velocity_x, velocity_y, min_distance_front, min_distance_back, num_neighbors))
      full_dataset = np.vstack((full_dataset, data_values[index]))
      print(full_dataset.shape)

    return full_dataset
