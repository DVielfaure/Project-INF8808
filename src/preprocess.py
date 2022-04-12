import pandas as pd


def create_dataframe_from_csv():
    list_csv = ['Departure Date', 
            'Departure Hardour', 'Departure Region', 
            'Departure Latitude', 'Departure Longitude', 
            'Arrival Date', 'Arrival Hardour', 
            'Arrival Region', 'Arrival Latitude', 
            'Arrival Longitude', 'Vessel Type', 
            'Lenght', 'Width', 
            'DeadWeight Tonnage', 'Maximum Draugth']

    #Initial dataframe
    dataframe = pd.read_csv('./data/Id.csv')

    #Combine dataframes
    for file in list_csv:
        file_name = "data/" + file + ".csv"
        dataframe_temporary = pd.read_csv(file_name)
        dataframe = dataframe.join(dataframe_temporary)
        
    return dataframe


def convert_datetime(df):
    '''
        Converts the date to datetime format.

        Args:
            df: The source df 
        Returns:
            df: The corrected dataframe
    '''
    df['Departure Date']= pd.to_datetime(df['Departure Date'])
    df['Arrival Date']= pd.to_datetime(df['Arrival Date']) 
    return df
    

def correct_data(df):
    '''
    Correction of swapped dates
    '''
    convert_datetime(df) 
    df[["Departure Date","Arrival Date"]] = df[["Departure Date","Arrival Date"]].where(df['Departure Date'] < df['Arrival Date'], df[["Arrival Date","Departure Date"]].values )
    return df

def filter_df(df,scale,place):
    '''
    Filter data on a specific scale: 
    example: filter on cleveland harbour:
    df = filter_df(df,"harbour","Cleveland")
    '''
    if scale == "all":
        df = df
    if scale == "region":
        df = df[df["Departure Region"]== place ]
    if scale == "harbour":
        df = df[df["Departure Hardour"]== place ]
        
    return df


def merge_topn(df):
    
    #Create list of larger ship categories
    df_traffic_topn = df.groupby(['Vessel Type']).sum()
    df_traffic_topn =df_traffic_topn.nlargest(10,"Traffic").reset_index()
    topn = df_traffic_topn["Vessel Type"].unique()

    
    #Separating df in top and bottom categories
    df_traffic_top = df[df['Vessel Type'].isin(topn)]
    df_traffic_bottom = df[~df['Vessel Type'].isin(topn)]

    #Merging bottom
    df_traffic_bottom = df_traffic_bottom.groupby(['Date', "Departure Hardour"]).sum().reset_index()
    df_traffic_bottom["Vessel Type"] = "OTHERS"

    #Merging top and bottom
    df_traffic_total = pd.concat([df_traffic_top,df_traffic_bottom]).reset_index()

    return df_traffic_total

def traffic_per_time(df, scale="year"):
    '''
        Converts the date to datetime format.

        Args:
            df: The source df 
        Returns:
            df: The traffic dataframe group by year and harbour
    '''
    #convertion in datetime 
    convert_datetime(df) 
    
    if scale == "year":
        df['Date']= (df['Departure Date']).dt.year

        df_traffic = df.groupby(["Departure Hardour","Date","Vessel Type"]).size().to_frame(name="Traffic").reset_index()
    
    if scale == "day":
        df["Date"] = (df['Departure Date']).dt.date

        df_traffic = df.groupby(["Departure Hardour","Date","Vessel Type"]).size().to_frame(name="Traffic").reset_index()

    df_traffic = merge_topn(df_traffic)
        
    return df_traffic


def get_map_data_extended(data,type):
    '''
        Converts the data to a pandas dataframe.

        Args:
            data: The source csv data to convert
        Returns:
            my_df: The corresponding dataframe
    '''
    # Sélectionne quelques colonnes
    df = data[["Id",type+" Hardour",type+" Latitude",type+" Longitude", type+" Region"]]
    #Groupby selon les ports de départs
    df = df.groupby([type+" Hardour",type+" Latitude",type+" Longitude", type+" Region"]).count()
    #return dataframe
    df = df.reset_index()
    df.columns = ['Trafic' if x=='Id' else x for x in df.columns]
   
    return df


def get_map_data(data,type):
    '''
        Converts the data to a pandas dataframe.

        Args:
            data: The source csv data to convert
        Returns:
            my_df: The corresponding dataframe
    '''
    # Sélectionne quelques colonnes
    df = data[["Id",type+" Hardour",type+" Latitude",type+" Longitude", type+" Region"]]
    #Groupby selon les ports de départs
    df = df.groupby([type+" Hardour", type+" Region"]).agg(
        {type+" Latitude":'mean',
        type+" Longitude":'mean',
        "Id": 'count'}
    )
    #return dataframe
    df = df.reset_index()
    df.columns = ['Trafic' if x=='Id' else x for x in df.columns]
    return df


#les ports vituals : 
#map_data[map_data["Departure Hardour"].str.contains("Virtual")]


def get_barchart_data(data,type):
    '''
        Converts the data to a pandas dataframe.
        Args:
            data: The source csv data to convert
        Returns:
            my_df: The corresponding dataframe
    '''
    #même données que pour la map sans les géo positions
    df = get_map_data(data,type)

    df = df[[type+" Hardour", type+" Region","Trafic"]]

    return df


def get_sankey_data(dataframe, port_central):
    '''
        Creates pandas dataframes ofr arrival and departure harbours.
        Args:
            dataframe: The source dataframe 
        Returns:
            df_provenance: Dataframe corresponding to departure
            df_destination: Dataframe corresponding to arrival
    '''
    
    #Drop unnecessary columns
    df_sankey = dataframe.copy()
    df_sankey = df_sankey.drop(['Id', 'Departure Date', 'Lenght', 'Width',
                    'Departure Latitude', 'Departure Longitude',
                    'Arrival Longitude', 'Arrival Latitude',
                    'Vessel Type', 'DeadWeight Tonnage',
                    'Maximum Draugth', 'Arrival Date'], axis=1)
    
    #Filter with the right central harbour
    df_departure = df_sankey.loc[dataframe['Arrival Hardour'] == port_central]
    df_arrival = df_sankey.loc[dataframe['Departure Hardour'] == port_central]

    #Count number of occurences
    df_departure = df_departure['Departure Hardour'].value_counts()
    df_arrival = df_arrival['Arrival Hardour'].value_counts()
    
    #Returns the two dataframes
    return df_departure, df_arrival

def get_bar_traffic_data(df, time_scale, spatial_scale, place):
    df_cop = df.copy()
    df_cop = correct_data(df_cop)

    df_cop = filter_df(df_cop, spatial_scale, place)
    df_cop = traffic_per_time(df_cop, time_scale)
    df_cop = df_cop.drop(df_cop.columns[0], axis=1)
    return df_cop