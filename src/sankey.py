import plotly.graph_objects as go

#Inputs
ports_provenance = ["Quebec", "Autres", "Ingonish", "New York (USA)", "Trois-Rivières"]
port_central = ["Montreal"]
ports_destination = ["Autres", "New York (USA)", "Le Havre (France)", "Quebec", "St. Andrews"]

couleur_provenance = ["blue", "blue", "blue", "orange", "blue"]
couleur_central = ["gray"]
couleur_destination = ["blue", "orange", "orange", "blue", "blue"]

nb_voyages = [12, 1, 2, 7, 4, 2, 4, 6, 7, 7]


fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "grey", width = 0.0),
      label = ["Quebec", "Autres", "Ingonish", "New York (USA)", "Trois-Rivières", "Montreal", "Autres", "New York (USA)", "Le Havre (France)", "Quebec", "St. Andrews"],
      color = ["blue", "blue", "blue", "orange", "blue", "gray", "blue", "orange", "orange", "blue", "blue"]
    ),
    link = dict(
      source = [0, 1, 2, 3, 4, 5, 5, 5, 5, 5],
      target = [5, 5, 5, 5, 5, 6, 7, 8, 9, 10],
      value = [12, 1, 2, 7, 4, 2, 4, 6, 7, 7],
      hovertemplate='Provenance: %{source.label}<br />'+
        'Destination: %{target.label}<br />Nombre de voyages: %{value}<extra></extra>'
  ))])

#Add title
fig.update_layout(title_text="Flux entrants et flux sortants du port de " + port_central[0], font_size=15)

#Show figure for development
fig.show()