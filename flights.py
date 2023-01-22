from geopy.distance import geodesic
from fare_classes import FareClass
import airportsdata

AIRPORTS_DATA = airportsdata.load('IATA')

class Itinerary:
    def __init__(self, *segments):
        """
        Initialize an itinerary with a variable number of segments. 
        Each segment is a tuple containing a list of airports and a fare class.
        
        :param segments: variable number of tuples containing a list of airports and a fare class
        """
        self.segments = segments

    @property
    def segments(self):
        """List of Segment objects in the itinerary"""
        return self._segments

    @segments.setter
    def segments(self, segments):
        self._airports = None
        self._all_distances = None
        self._segments = [Segment(segment[0], segment[1]) for segment in segments]

    @property
    def airports(self):
        """
        A dictionary that maps airport codes to their coordinates.
        """
        if not self._airports:
            # Set dictionary keys from the airport codes in the itinerary
            self._airports = {code: None for segment in self.segments for code in segment.flight_segment}

            # Find coordinates and set as values for each airport code in the dictionary
            self._airports = {code: (AIRPORTS_DATA[code]['lat'], 
                                AIRPORTS_DATA[code]['lon']) for code in self._airports}
        return self._airports

    @property
    def all_distances(self):
        """
        A dictionary that maps legs (pairs of airports) to their distances in miles.
        """
        if not self._all_distances:
            # Create a dictionary of legs and their distances in miles
            distances = {tuple(leg): round(geodesic(self.airports[leg[0]], self.airports[leg[1]]).miles)
                                    for segment in self.segments for leg in segment.legs}
        return distances

    def distance_per_segment(self):
        """
        Returns a list of the distances of the segments
        
        :return: list of distances of all the segments
        """

        # Sum distances of each leg in each segment
        return [sum(self.all_distances[tuple(leg)] for leg in segment.legs) for segment in self.segments]


class Segment:
    def __init__(self, flight_segment, fare_class):
        """
        Initialize a segment with a flight segment and fare class
        
        :param flight_segment: list of airport codes
        :param fare_class: fare class for the flight segment
        """
        self.flight_segment = flight_segment
        self.fare_class = fare_class

    @property
    def flight_segment(self):
        """List of airport codes for the flight segment"""
        return self._flight_segment

    @flight_segment.setter
    def flight_segment(self, flight_segment):
        self._legs = None
        self._flight_segment = [code.upper() for code in flight_segment]

    @property
    def legs(self):
        """
        A list of legs (pairs of airports) in the segment
        """
        if not self._legs:

            # Create a list containing all legs in the segment
            self._legs = [[self.flight_segment[i], self.flight_segment[i + 1]] 
                    for i, code in enumerate(self.flight_segment[:-1])]
        return self._legs

    @property
    def fare_class(self):
        """
        Fare class for the flight segment
        """
        return self._fare_class

    @fare_class.setter
    def fare_class(self, fare_class):
        self._fare_class = FareClass(fare_class)
