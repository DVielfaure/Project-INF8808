'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd


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