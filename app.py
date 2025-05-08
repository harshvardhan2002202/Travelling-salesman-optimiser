# tsp_project/app.py (Streamlit App)
import streamlit as st
import pandas as pd
import json
from collections import namedtuple
from tsp_solver import compute_distance_matrix, greedy_tsp, two_opt, total_distance
from distance import haversine

def load_places_from_df(df):
    Place = namedtuple("Place", ["name", "lat", "lon"])
    return [Place(row["Name"], row["Lat"], row["Lon"]) for _, row in df.iterrows()]

def export_geojson(places, path):
    coords = [[places[i].lon, places[i].lat] for i in path]
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": coords
                },
                "properties": {}
            }
        ]
    }
    return geojson

def main():
    st.title("🗺️ Travelling Salesman City-Tour Optimizer")

    uploaded_file = st.file_uploader("Upload places.csv", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if not {"Name", "Lat", "Lon"}.issubset(df.columns):
            st.error("CSV must contain Name, Lat, Lon columns.")
            return

        places = load_places_from_df(df)
        names = [p.name for p in places]
        start_name = st.selectbox("Select starting location", names)
        return_trip = st.checkbox("Return to start")

        if st.button("Optimize Route"):
            start_index = names.index(start_name)
            dist = compute_distance_matrix(places)
            path = greedy_tsp(dist, start=start_index)
            path = two_opt(path, dist)
            if return_trip:
                path.append(start_index)

            st.subheader("📌 Optimized Route")
            for idx in path:
                st.write(f"- {places[idx].name}")

            total_km = total_distance(path, dist)
            st.success(f"Total Distance: {total_km:.2f} km")

            geojson = export_geojson(places, path)
            st.download_button("Download GeoJSON", json.dumps(geojson, indent=2), "route.geojson", "application/geo+json")

if __name__ == "__main__":
    main()
