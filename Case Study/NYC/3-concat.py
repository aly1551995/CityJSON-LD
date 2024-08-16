from SPARQLWrapper import SPARQLWrapper, JSON
import geopandas as gpd
from shapely import wkt
import folium

# Set up the SPARQL endpoint
sparql = SPARQLWrapper("http://localhost:3031/NYC/sparql")
# Define the SPARQL query to fetch the geometry collection with non-empty WKTs
query = """
PREFIX cj: <https://www.cityjson.org/ont/cityjson.ttl#>
PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>
PREFIX geof: <http://www.opengis.net/def/function/geosparql/>

SELECT (CONCAT("GEOMETRYCOLLECTION(", GROUP_CONCAT(?geometryWKT; separator=","), ")") AS ?geometryCollectionWKT)
WHERE {
  {
    SELECT ?geometry
    WHERE {
      # Retrieve the geometries of buildings
      ?building cj:hasGeometry ?geometry .
      ?geometry cj:lod "2" .
    }
  }
  ?geometry geosparql:asWKT ?geometryWKT .
}

"""
# Set the query
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
# Execute the query and get the results
try:
    results = sparql.query().convert()
except Exception as e:
    print(f"Error querying the SPARQL endpoint: {e}")
    results = None
# Check if results were returned
if results and "results" in results and "bindings" in results["results"]:
    for result in results["results"]["bindings"]:
        geometry_collection_wkt = result["geometryCollectionWKT"]["value"]
        
        # Save the result to a file
        with open("geometry_collection.wkt", "w") as file:
            file.write(geometry_collection_wkt)
            print("Geometry collection WKT saved to geometry_collection.wkt")
        
        # Convert WKT to a Shapely geometry
        geometry = wkt.loads(geometry_collection_wkt)

        # Create a GeoDataFrame with EPSG:2263
        gdf = gpd.GeoDataFrame(index=[0], crs="EPSG:2263", geometry=[geometry])

        # Reproject to EPSG:4326 for visualization on a real-world map
        gdf = gdf.to_crs(epsg=4326)

        # Get the centroid of the geometry to center the map
        centroid = gdf.geometry.centroid.iloc[0]

        # Create a folium map centered around the geometry
        m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12)

        # Add the geometry to the map
        folium.GeoJson(gdf).add_to(m)

        # Save or display the map
        m.save("map.html")
        print("Map saved to map.html")

else:
    print("No results found or an error occurred.")
