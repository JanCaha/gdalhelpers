import os

print(os.path.dirname(__file__))

print(os.path.join(os.path.realpath(".."), "test_data", "points.gpkg"))

POINTS_PATH = os.path.join(os.path.dirname(__file__), "..", "tests", "points.gpkg")

print(POINTS_PATH)