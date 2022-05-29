from numpy import partition
from datasets import data
from datasets.data import Normalizer
from dask.distributed import Client
import dask.dataframe as dd
import pandas as pd

import os

root_dir = 'data/epacems'
dest_dir = 'data/epacems_preprocess'

client = Client()

row_filter = [[('year', '=', 2019)]]
col_filter = [
    "state",
    "operating_datetime_utc",
    "unit_id_epa",
    "operating_time_hours",
    "gross_load_mw",
    "heat_content_mmbtu"
]
epacems_dd = dd.read_parquet(
    root_dir,
    filters=row_filter,
    columns=col_filter
)
all_df = epacems_dd.compute()

# I chose to convert the heat_content_mmbtu column to a heat_content_mwh column 
# for ease of interpretation by non-energy-experts
all_df['heat_content_mwh'] = all_df.heat_content_mmbtu / 3.409510
all_df.drop(columns = ['heat_content_mmbtu'], inplace = True)

# I chose to fill the NaNs in operating_time_hours with zeros, becuase they 
# occur in these giant long chunks, at least in several places, and to my best 
# understanding the EPA wouldn't allow missing values in this dataset, since
# it's a financial dataset used for cap and trade
all_df.operating_time_hours  = all_df.operating_time_hours.fillna(0)

# Now, getting the TGU-month sample IDs for use by the transformer model
all_df['year'] = all_df.operating_datetime_utc.dt.year
all_df['month'] = all_df.operating_datetime_utc.dt.month

index_cols = ['unit_id_epa', 'year', 'month']
all_df = all_df.set_index(index_cols)
id_df = all_df.groupby(index_cols).agg(n_obs = pd.NamedAgg('state', 'count'))
# Eliminate all samples with less than 100 observations (necessary for convolutions)
id_df = id_df.drop(index=id_df.loc[id_df.n_obs < 100].index)
id_df = id_df.reset_index().reset_index().rename(columns={'index':'sample_id'})
id_df = id_df.drop(columns='n_obs')
id_df = id_df.set_index(index_cols)
all_df = all_df.merge(id_df, how = 'inner', left_index = True, right_index = True)

# Perform normalization
normer = Normalizer(norm_type='standardization')
norm_df = normer.normalize(all_df.loc[:, ['operating_time_hours', 'gross_load_mw', 'heat_content_mwh']])
all_df['operating_time_hours'] = norm_df['operating_time_hours']
all_df['gross_load_mw'] = norm_df['gross_load_mw']
all_df['heat_content_mwh'] = norm_df['heat_content_mwh']

# Write out to new parquet files
state_list = all_df.state.unique()
state_df_dict = {cur_state:all_df.loc[all_df.state == cur_state, :] for cur_state in state_list}

[state_df_dict[state].to_csv(f'data/preprocessed/2019/{state}.csv') for state in state_list]