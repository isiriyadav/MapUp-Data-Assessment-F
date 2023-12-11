import pandas as pd
from datetime import time, timedelta

def calculate_distance_matrix("dataset-3.csv")->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
df = pd.read_csv("dataset-3.csv", index_col='ID')

    # Initialize an empty distance matrix
    distance_matrix = pd.DataFrame(index=df.index, columns=df.index)

    # Iterate over each pair of toll locations
    for start_loc in df.index:
        for end_loc in df.index:
            if start_loc != end_loc:
                # Calculate the cumulative distance for bidirectional routes
                distance = df.at[start_loc, end_loc] + df.at[end_loc, start_loc]
                distance_matrix.at[start_loc, end_loc] = distance

    # Set diagonal values to 0
    distance_matrix.values[[range(distance_matrix.shape[0])]*2] = 0

    return distance_matrix

# Example usage
distance_matrix = calculate_distance_matrix("dataset-3.csv")
print(distance_matrix)


def unroll_distance_matrix(distance_matrix)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    # Stack the distance matrix and reset the index
    unrolled_df = distance_matrix.stack().reset_index()

    # Rename the columns to match the desired format
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

    # Exclude rows where id_start is equal to id_end
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]

    return unrolled_df

# Example usage
# Assuming distance_matrix is the DataFrame created in Question 1
unrolled_df = unroll_distance_matrix(distance_matrix)
print(unrolled_df)



def find_ids_within_ten_percentage_threshold(unrolled_df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    # Filter DataFrame for the given reference_id
    reference_data = unrolled_df[unrolled_df['id_start'] == reference_id]

    # Calculate the average distance for the reference_id
    reference_avg_distance = reference_data['distance'].mean()

    # Calculate the threshold as 10% of the average distance
    threshold = 0.1 * reference_avg_distance

    # Filter IDs within the threshold range
    selected_ids = unrolled_df[(unrolled_df['distance'] >= reference_avg_distance - threshold) &
                               (unrolled_df['distance'] <= reference_avg_distance + threshold)]['id_start'].unique()

    # Sort and return the selected IDs
    return sorted(selected_ids)

# Example usage
# Assuming unrolled_df is the DataFrame created in Question 2
reference_id = 1  # Replace with the desired reference ID
selected_ids = find_ids_within_ten_percentage_threshold(unrolled_df, reference_id)
print(selected_ids)



def calculate_toll_rate(df)->pd.DataFrame(unrolled_df):
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Calculate toll rates for each vehicle type and add columns to the DataFrame
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        unrolled_df[vehicle_type] = unrolled_df['distance'] * rate_coefficient

    return unrolled_df

# Example usage
# Assuming unrolled_df is the DataFrame created in Question 2
toll_rate_df = calculate_toll_rate(unrolled_df)
print(toll_rate_df)



def calculate_time_based_toll_rates(toll_rate_df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    # Define time intervals and discount factors
    time_intervals = {
        'Weekdays': [(time(0, 0), time(10, 0), 0.8),
                     (time(10, 0), time(18, 0), 1.2),
                     (time(18, 0), time(23, 59, 59), 0.8)],
        'Weekends': [(time(0, 0), time(23, 59, 59), 0.7)]
    }

    # Create new columns for start_day, start_time, end_day, and end_time
    toll_rate_df[['start_day', 'start_time', 'end_day', 'end_time']] = toll_rate_df.apply(
        lambda x: pd.Series([x.name[0], time(0, 0), x.name[1], time(23, 59, 59)]), axis=1)

    # Apply discount factors based on time intervals
    def apply_discount(row):
        for day_type, intervals in time_intervals.items():
            for start_time, end_time, discount_factor in intervals:
                if row['start_day'] in day_type and start_time <= row['start_time'] <= end_time:
                    return row[vehicle_type] * discount_factor
        return row[vehicle_type]

    # Apply discount factors to each vehicle type column
    vehicle_types = ['moto', 'car', 'rv', 'bus', 'truck']
    for vehicle_type in vehicle_types:
        toll_rate_df[vehicle_type] = toll_rate_df.apply(apply_discount, axis=1)

    return toll_rate_df

# Example usage
# Assuming toll_rate_df is the DataFrame created in Question 4
time_based_toll_rates_df = calculate_time_based_toll_rates(toll_rate_df)
print(time_based_toll_rates_df)


