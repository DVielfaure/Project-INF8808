from functools import reduce
from threading import Thread
import time
import pandas as pd

def thread_read_csv(result, index, file_name):
    result[index] = pd.read_csv(file_name)

def create_dataframe_from_csv():


    list_csv = ['Id', 'Departure Date', 
            'Departure Hardour', 'Departure Region', 
            'Departure Latitude', 'Departure Longitude', 
            'Arrival Date', 'Arrival Hardour', 
            'Arrival Region', 'Arrival Latitude', 
            'Arrival Longitude', 'Vessel Type', 
            'Lenght', 'Width', 
            'DeadWeight Tonnage', 'Maximum Draugth']


    threads = [None] * len(list_csv)
    results = [None] * len(list_csv)

    #Combine dataframes
    for i in range(len(list_csv)):
        file_name = "data/" + list_csv[i] + ".csv"
        threads[i] = Thread(target=thread_read_csv, args=(results, i, file_name))
        threads[i].start()

    for i in range(len(list_csv)):
        threads[i].join()

    dataframe = reduce(lambda left,right: left.join(right), results)
    
    #correction typo Hardour
    dataframe = dataframe.rename(columns={'Departure Hardour':'Departure Harbour', 'Arrival Hardour':'Arrival Harbour' })

    #raccourci "Merchant Chemical/Oil Products Tanker" en "Merchant Chemical/Oil" pour que la légende prenne moins de place 
    dataframe = dataframe.replace("Merchant Chemical/Oil Products Tanker","Merchant Chemical/Oil")
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

def filter_df(df, scale, place):
    '''
    Filter data on a specific scale: 
    example: filter on cleveland harbour:
    df = filter_df(df,"harbour","Cleveland")
    '''
    if scale == "Region":
        return df[df["Departure Region"] == place ]
    if scale == "Harbour":
        return df[df["Departure Harbour"] == place ]

    return df

def merge_topn_bar(df):
    
    #Create list of larger ship categories
    df_traffic_topn = df.groupby(['Vessel Type']).sum()
    df_traffic_topn = df_traffic_topn.nlargest(10,"Traffic").reset_index()
    topn = df_traffic_topn["Vessel Type"].unique()

    
    #Separating df in top and bottom categories
    df_traffic_top = df[df['Vessel Type'].isin(topn)]
    df_traffic_bottom = df[~df['Vessel Type'].isin(topn)]

    #Merging bottom
    df_traffic_bottom = df_traffic_bottom.groupby(['Date']).sum().reset_index()
    df_traffic_bottom["Vessel Type"] = "OTHERS"

    #Merging top and bottom
    df_traffic_total = pd.concat([df_traffic_top,df_traffic_bottom]).reset_index()

    return df_traffic_total.sort_values(by="Traffic", ascending=False)

def traffic_per_time_bar(df, scale="year"):
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

        df_traffic = df.groupby(["Date","Vessel Type"]).size().to_frame(name="Traffic").reset_index()

    if scale == "month":
        df['Date']= (df['Departure Date']).dt.month

        df_traffic = df.groupby(["Date","Vessel Type"]).size().to_frame(name="Traffic").reset_index()

    if scale == "day":
        df["Date"] = (df['Departure Date']).dt.date

        df_traffic = df.groupby(["Date","Vessel Type"]).size().to_frame(name="Traffic").reset_index()
        
    return df_traffic


def get_map_data_extended(data):
    '''
        Converts the data to a pandas dataframe.

        Args:
            data: The source csv data to convert
        Returns:
            my_df: The corresponding dataframe
    '''
    # Sélectionne quelques colonnes
    df = data[["Id","Departure Harbour","Departure Latitude","Departure Longitude", "Departure Region"]]
    #Groupby selon les ports de départs
    df = df.groupby(["Departure Harbour","Departure Latitude","Departure Longitude", "Departure Region"]).count()
    #return dataframe
    df = df.reset_index()
    df.columns = ['Trafic' if x=='Id' else x for x in df.columns]
   
    return df


def get_map_data(data):
    '''
        Converts the data to a pandas dataframe.

        Args:
            data: The source csv data to convert
        Returns:
            my_df: The corresponding dataframe
    '''
    # Sélectionne quelques colonnes
    df = data[["Id","Departure Harbour","Departure Latitude","Departure Longitude", "Departure Region"]]
    #Groupby selon les ports de départs
    df = df.groupby(["Departure Harbour", "Departure Region"]).agg(
        {"Departure Latitude":'mean',
        "Departure Longitude":'mean',
        "Id": 'count'}
    )
    #return dataframe
    df = df.reset_index()
    df.columns = ['Trafic' if x=='Id' else x for x in df.columns]
    return df


#les ports vituals : 
#map_data[map_data["Departure Harbour"].str.contains("Virtual")]


def get_barchart_data(data):
    '''
        Converts the data to a pandas dataframe.
        Args:
            data: The source csv data to convert
        Returns:
            my_df: The corresponding dataframe
    '''
    #même données que pour la map sans les géo positions
    # df = get_map_data(data)

    # df = df[["Departure Harbour", "Departure Region","Trafic"]]

    return data[["Departure Harbour", "Departure Region","Trafic"]]


def get_sankey_data(dataframe, type, value):
    '''
        Creates pandas dataframes ofr arrival and departure harbours.
        Args:
            dataframe: The source dataframe 
        Returns:
            df_provenance: Dataframe corresponding to departure
            df_destination: Dataframe corresponding to arrival
    '''
    
    #Drop unnecessary columns
    df_sankey = dataframe.drop(['Id', 'Departure Date', 'Lenght', 'Width',
                    'Departure Latitude', 'Departure Longitude',
                    'Arrival Longitude', 'Arrival Latitude',
                    'Vessel Type', 'DeadWeight Tonnage',
                    'Maximum Draugth', 'Arrival Date'], axis=1)

    if type == "All":
        df_departure = df_sankey.loc[dataframe['Departure Harbour'].str.contains("Virtual Harbour", case=False)]
        df_arrival = df_sankey.loc[dataframe['Arrival Harbour'].str.contains("Virtual Harbour", case=False)]
        
        #Count number of occurences
        Nb_departure_international = df_departure.shape[0]
        Nb_arrival_international = df_arrival.shape[0]
        Nb_departure_intra = dataframe.shape[0] - Nb_departure_international + Nb_arrival_international
        Nb_arrival_intra = dataframe.shape[0] - Nb_departure_international + Nb_arrival_international
        
        d_departure = {'International': Nb_departure_international, 'Intra-Canada': Nb_departure_intra}
        d_arrival = {'International': Nb_arrival_international, 'Intra-Canada': Nb_arrival_intra}
        df_departure = pd.Series(data=d_departure, index=['International', 'Intra-Canada'])
        df_arrival = pd.Series(data=d_arrival, index=['International', 'Intra-Canada'])
 
        #Converts dataframes to lists
        list_departure_harbours = df_departure.index.tolist()
        list_arrival_harbours = df_arrival.index.tolist()
        list_departure_counts = df_departure.tolist()
        list_arrival_counts = df_arrival.tolist()
        
        #Get index of central node
        central_node_index = len(list_arrival_harbours) 
        
        #Concatenate lists for sankey
        label = []
        label.extend(list_arrival_harbours)
        label.append("Ports du Canada")
        label.extend(list_departure_harbours)
        
        sankey_values=[]
        sankey_values.extend(list_arrival_counts)
        sankey_values.extend(list_departure_counts)
        
        #Returns the two lists
        return label, sankey_values, central_node_index
        
    elif type == "Region":
        #Filter with the right central Region
        df_departure = df_sankey.loc[dataframe['Arrival Region'] == value]
        df_arrival = df_sankey.loc[dataframe['Departure Region'] == value]
        
        #Count number of occurences
        df_departure = df_departure['Departure Region'].value_counts()
        df_arrival = df_arrival['Arrival Region'].value_counts()
        
        #Converts dataframes to lists
        list_departure_harbours = df_departure.index.tolist()
        list_arrival_harbours = df_arrival.index.tolist()
        list_departure_counts = df_departure.tolist()
        list_arrival_counts = df_arrival.tolist()
        
        #Count others
        departure_other_count = 0
        for n1 in list_departure_counts[5:]:
            departure_other_count += n1
            
        arrival_other_count = 0
        for n2 in list_arrival_counts[5:]:
            arrival_other_count += n2
            
        #Keep only top 5
        list_departure_harbours = df_departure.index.tolist()[0:5]
        list_arrival_harbours = df_arrival.index.tolist()[0:5]
        list_departure_counts = df_departure.tolist()[0:5]
        list_arrival_counts = df_arrival.tolist()[0:5]
        
        #Append others to list
        list_departure_harbours.append("Others")
        list_arrival_harbours.append("Others")
        list_departure_counts.append(departure_other_count)
        list_arrival_counts.append(arrival_other_count)
        
        #Get index of central node
        central_node_index = len(list_arrival_harbours) 
        
        #Concatenate lists for sankey
        label = []
        label.extend(list_arrival_harbours)
        label.append(value)
        label.extend(list_departure_harbours)
        
        sankey_values=[]
        sankey_values.extend(list_arrival_counts)
        sankey_values.extend(list_departure_counts)
        
        #Returns the two lists
        return label, sankey_values, central_node_index
        
    
    elif type == "Harbour":
        #Filter with the right central harbour
        df_departure = df_sankey.loc[dataframe['Arrival Harbour'] == value]
        df_arrival = df_sankey.loc[dataframe['Departure Harbour'] == value]

        #Count number of occurences
        df_departure = df_departure['Departure Harbour'].value_counts()
        df_arrival = df_arrival['Arrival Harbour'].value_counts()
        
        #Converts dataframes to lists
        list_departure_harbours = df_departure.index.tolist()
        list_arrival_harbours = df_arrival.index.tolist()
        list_departure_counts = df_departure.tolist()
        list_arrival_counts = df_arrival.tolist()
        
        #Count others
        departure_other_count = 0
        for n1 in list_departure_counts[5:]:
            departure_other_count += n1
            
        arrival_other_count = 0
        for n2 in list_arrival_counts[5:]:
            arrival_other_count += n2
            
        #Keep only top 5
        list_departure_harbours = df_departure.index.tolist()[0:5]
        list_arrival_harbours = df_arrival.index.tolist()[0:5]
        list_departure_counts = df_departure.tolist()[0:5]
        list_arrival_counts = df_arrival.tolist()[0:5]
        
        #Append others to list
        list_departure_harbours.append("Others")
        list_arrival_harbours.append("Others")
        list_departure_counts.append(departure_other_count)
        list_arrival_counts.append(arrival_other_count)
        
        #Get index of central node
        central_node_index = len(list_arrival_harbours) 
        
        #Concatenate lists for sankey
        label = []
        label.extend(list_arrival_harbours)
        label.append(value)
        label.extend(list_departure_harbours)
        
        sankey_values=[]
        sankey_values.extend(list_arrival_counts)
        sankey_values.extend(list_departure_counts)
        
        #Returns the two lists
        return label, sankey_values, central_node_index

def get_bar_traffic_data(df, time_scale):

    df = traffic_per_time_bar(df, time_scale)
    df = merge_topn_bar(df)
    df = df.drop(df.columns[0], axis=1)
    return df

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

def get_linechart_data(data):

    df = traffic_per_time_bar(data, scale="month")
    df = df.drop("Vessel Type",1)

    temp = pd.DataFrame([[x,0] for x in range(1,13)], columns = ["Date", "Traffic"])

    df = pd.concat([df, temp])
    df = df.groupby("Date").sum().reset_index()


    df = df.rename(columns={"Date":"Month"})

    df["Month"] = df["Month"].apply(lambda x: months[x-1])

    return df