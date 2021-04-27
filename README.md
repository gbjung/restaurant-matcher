### Restaurant Matcher
API concept of a basic search function that allows for searching of local restaurants for the best match.

## How to Setup
1. Install pipenv via "pip install pipenv" or https://pypi.org/project/pipenv/ for additional methods.
   pipenv acts as both a virtual environment and package manager

2. In /restaurant-matcher, "pipenv install" to install the contents from the Pipfile.
   Pipfile are like gemfiles in ruby or package.json in node

3. In /restaurant-matcher, "pipenv shell" to start the virtual env

4. "python -m flask run" to start the application

5. "python -m pytest" to run unit tests

## How to Use
1. After "python -m flask run", the local server will run on localhost:5000.
   The proof of concept API lives under the route "localhost:5000/match_service/"
   This base view shows you all available restaurants in the sort of lowest distance -> highest rating -> cheapest price

2. Query for additional filters using the url parameters as arguments.

   available parameters:
      name: Name of restaurant to search for. Matches substrings. Example: "Chowify"
      rating: From 1 to 5, restaurant rating
      distance: From 1 to 10, unit of distance away
      cuisine: Type of cuisine to filter. Example: "Chinese"

   These parameters can be mixed/matched and are all optional.

   Example queries:
   localhost:5000/match_service/?name=chow&rating=1&distance=10&cuisine=Chinese
   localhost:5000/match_service/?rating=5&distance=3

## Assumptions
1. The API was designed in a way to not be dependent on any external search/filtering tools
   outside of Python. The logic in DataStorage is inspired by noSQL DBs and DataManager
   emulates a lot SQL like queries, in which it is operated via various ANDed subqueries.

2. The data accessors in DataStorage such as self.ratings and self.distance are meant to
   emulate behaviors like indexed join tables.

   self.cuisines and self.cuisine ids are separated to account for potential data mutability (hypothetical, Greek reclassified as Mediterranean).
   Same split logic applies to the self.names acting as a foreign key to self.restaurant_details.

3. The filtering/sorting in DataManager takes a modular approach to filtering and sorting.
   With the goal of maintainability, readability, and modularity, it can hypothetically be easily broken apart
   for multiple contributors to alter the various methods in parallel.

   Certain "samey" methods like those for filtering rating, distance, and price have been split apart
   for logical delineation in case data formats for any of these properties change to add/remove complexity later.
