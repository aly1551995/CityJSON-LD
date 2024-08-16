import json
from SPARQLWrapper import SPARQLWrapper, JSON

# Set up the SPARQL endpoint
sparql = SPARQLWrapper("http://localhost:3031/Helsinki/sparql")

# Define the SPARQL query to fetch the attributes along with the city object
query = """
PREFIX cj: <https://www.cityjson.org/ont/cityjson.ttl#>

SELECT ?cityObject ?attributes
WHERE {
    ?cityObject cj:hasAttribute ?attributes .
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

# Initialize variables for calculating the average height
total_height = 0
count = 0
details = []

# First pass: Calculate the total height and count valid measurements
if results and "results" in results and "bindings" in results["results"]:
    for result in results["results"]["bindings"]:
        city_object = result["cityObject"]["value"]
        attributes_values = json.loads(result["attributes"]["value"])
        
        # Check if "measuredHeight" is in the attributes and is a number
        measuredHeight = attributes_values.get("measuredHeight", None)
        if measuredHeight is not None:
            try:
                measuredHeight = float(measuredHeight)
                total_height += measuredHeight
                count += 1
            except ValueError:
                measuredHeight = "N/A"
        
        # Store the details for the second pass
        details.append((city_object, measuredHeight))

    # Calculate the average height if any valid heights were found
    if count > 0:
        average_height = total_height / count
    else:
        average_height = 0.0
    
    # Print the summary at the beginning
    print(f"Query returned {count} results with valid heights. Average Height: {average_height:.7f}.")
    
    # Second pass: Print each city's details
    for city_object, measuredHeight in details:
        print(f"City Object: {city_object}, measuredHeight: {measuredHeight}")
else:
    print("No results found or an error occurred.")


