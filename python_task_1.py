import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    
    #Read data set
    df = pd.read_csv('dataset-1.csv')
    
    #Create Pivot table with id_1 as index, id_2 as colums, and car as values 
    car_matrix = df.pivot_table(index='id_1', columns='id_2' , values='car' , fill_values=0)
    
    #set the diagonal values to 0 
    car_matrix.values[[range(len(car_matrix))*2] = 0 
    
                     
    return car_matrix
result = genrate_car_matrix('dataset-1.csv')
              
#Print
print(result)
             



def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic her
              
    # Read the CSV file into a DataFrame
    df = pd.read_csv('dataset-1.csv')

    # Add a new categorical column 'car_type' based on the values of the 'car' column
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])

    # Calculate the count of occurrences for each 'car_type' category
    type_count = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_count = dict(sorted(type_count.items()))

    return type_count

# Replace 'dataset-1.csv' with the actual path to your CSV file
result = get_type_count('dataset-1.csv')

# Print the result
print(result)



def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
 
    # Read the CSV file into a DataFrame
    df = pd.read_csv('dataset-1.csv')

    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

# Replace 'dataset-1.csv' with the actual path to your CSV file
result = get_bus_indexes('dataset-1.csv')

# Print the result
print(result)



def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
# Read the CSV file into a DataFrame
    df = pd.read_csv('dataset-1.csv')

    # Group by 'route' and calculate the average of the 'truck' column
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' column is greater than 7
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of filtered routes
    filtered_routes.sort()

    return filtered_routes

# Replace 'dataset-1.csv' with the actual path to your CSV file
result = filter_routes('dataset-1.csv')

# Print the result
print(result)



def multiply_matrix(input_matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here

    # Create a copy of the input matrix to avoid modifying the original DataFrame
    modified_matrix = input_matrix.copy()

    # Apply the specified logic to modify values in the DataFrame
    modified_matrix[modified_matrix > 20] *= 0.75
    modified_matrix[modified_matrix <= 20] *= 1.25

    # Round values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix

# Assuming 'result' is the DataFrame from Question 1
# You should replace it with the actual DataFrame you obtained from Question 1
result_from_question1 = generate_car_matrix('dataset-1.csv')

# Apply the multiply_matrix function
modified_result = multiply_matrix(result_from_question1)

# Print the modified result
print(modified_result)



def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here

    # Read the CSV file into a DataFrame
    df = pd.read_csv('dataset-2.csv')

    # Combine date and time columns to create a datetime column
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Check if timestamps cover a full 24-hour period and span all 7 days of the week
    time_completeness = (
        (df['start_datetime'].dt.time == pd.to_datetime('00:00:00').time()) &
        (df['end_datetime'].dt.time == pd.to_datetime('23:59:59').time()) &
        (df['start_datetime'].dt.dayofweek == 0) &  # Monday
        (df['end_datetime'].dt.dayofweek == 6)     # Sunday
    )

    # Create a multi-index boolean series with (id, id_2) as index
    time_completeness_series = time_completeness.groupby(['id', 'id_2']).all()

    return time_completeness_series

# Replace 'dataset-2.csv' with the actual path to your CSV file
result = check_time_completeness('dataset-2.csv')

# Print the result
print(result)


