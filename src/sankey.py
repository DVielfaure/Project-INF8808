import plotly.graph_objects as go

def trace_sankey(df_departure, df_arrival, port_central):

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
  
  #Concatenate lists for sankey
  label = []
  label.extend(list_arrival_harbours)
  label.append(port_central)
  label.extend(list_departure_harbours)
  
  value=[]
  value.extend(list_arrival_counts)
  value.extend(list_departure_counts)

  
  #Trace sankey
  fig = go.Figure(data=[go.Sankey(
      node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "grey", width = 0.0),
        label = label,
        color = ["blue", "blue", "blue", "blue", "blue", "blue", "gray", "blue", "blue", "blue", "blue", "blue", "blue"]
      ),
      link = dict(
        source = [0, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6],
        target = [6, 6, 6, 6, 6, 6, 7, 8, 9, 10, 11, 12],
        value = value,
        hovertemplate='Provenance: %{source.label}<br />'+
          'Destination: %{target.label}<br />Nombre de voyages: %{value}<extra></extra>'
      ),
      textfont=dict(size=10)
      )])

  #Add title
  fig.update_layout(
    title_text="Flux entrants et flux sortants du port de " + port_central,
    title_x=0.5,
    margin=dict(l=0, r=0, t=26, b=0, pad=0),
  )

  #Show figure for development
  return fig