import plotly.graph_objects as go


def get_sankey_colors(label):
  color_list=[]
  for name in label:
    if "Virtual Harbour" in name or "International" in name or "Canadian Water" in name:
      color_list.append("rgb(255,127,80)")
    else:
      color_list.append("rgb(13,8,135)")
      
  return color_list

def get_sankey_source(central_node_index, label):
  source_list = []
  for i in range(len(label)):
    if i < central_node_index:
      source_list.append(i)
    else:
      source_list.append(central_node_index)
    
  return source_list

def get_sankey_target(central_node_index, label):
  target_list = []
  for i in range(len(label)):
    if i < central_node_index:
      target_list.append(central_node_index)
    else:
      target_list.append(i+1)
    
  return target_list
  
def trace_sankey(label, sankey_values, central_node_index):
  #Get colors
  color_list = get_sankey_colors(label)
  
  #Get source and target lists
  source_list = get_sankey_source(central_node_index, label)
  target_list = get_sankey_target(central_node_index, label)
    
  #Trace sankey
  fig = go.Figure(data=[go.Sankey(
      node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "grey", width = 0.0),
        label = label,
        color = color_list,
        hovertemplate = None,
        hoverinfo='skip'
      ),
      link = dict(
        source = source_list,
        target = target_list,
        value = sankey_values,
        hovertemplate='Provenance: %{source.label}<br>'+
          'Destination: %{target.label}<br/>Traffic: %{value}<extra></extra>'
      ),
      textfont=dict(size=10)
      )])
  
  #Add title
  fig.update_layout(
    title_text="Inflows and outflows",
    title_x=0.5,
    margin=dict(l=14, r=14, t=32, b=14, pad=0),
  )
  return fig