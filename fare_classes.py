FARE_CODES = ['Q', 'O', 'G', 'K', 'L', 'M', 'N', 'S', 'V', 'Y', 'B', 'H',
                'E', 'T', 'W', 'R', 'I', 'J', 'C', 'D', 'A', 'F']
AVIOS_FARE_CATERGORIES = [
    {'codes': ['Q', 'O', 'G'], 'multiplier': 0.25, 'minimum': 125},
    {'codes': ['K', 'L', 'M', 'N', 'S', 'V'], 'multiplier': 0.25, 'minimum': 125},
    {'codes': ['Y', 'B', 'H', 'E', 'T'], 'multiplier': 1, 'minimum': 500},
    {'codes': ['W', 'R', 'I'], 'multiplier': 1.5, 'minimum': 750},
    {'codes': ['J', 'C', 'D', 'A'], 'multiplier': 2.5, 'minimum': 1250},
    {'codes': ['F'], 'multiplier': 3, 'minimum': 1500}
    ]
TIER_POINT_AWARDS ={
    ('Q', 'O', 'G'): {2000: 5, 6000: 20, 10000: 20, 'SH+': 10, 'SYD': 30},
    ('K', 'L', 'M', 'N', 'S', 'V'): {2000: 10, 6000: 35, 10000: 40, 'SH+': 20, 'SYD': 60},
    ('Y', 'B', 'H'): {2000: 20, 6000: 70, 10000: 80, 'SH+': 40, 'SYD': 120},
    ('R', 'I', 'J', 'C', 'D'): {2000: 40, 6000: 140, 10000: 160, 'SH+': 80, 'SYD': 240},
    ('E', 'T', 'W'): {6000: 90, 10000: 100, 'SYD': 150},
    ('A', 'F'): {6000: 210, 10000: 240, 'SYD': 360}
}

class FareClass:
    def __init__(self, code):
        """
        Initialize a FareClass object with a fare class code
        
        :param code: fare class code
        """
        self.code = code

    @property
    def code(self):
        """Fare class code"""
        return self._code

    @code.setter
    def code(self, code):
        # Validate code
        if code.upper() not in FARE_CODES:
            raise ValueError("Invalid fare class code")
        self._code = code.upper()
        
        # Iterate over fare categories
        for category in AVIOS_FARE_CATERGORIES:

            # Assign the correct values
            if self.code in category['codes']:
                self._avios_multiplier = category['multiplier']
                self._minimum_avios = category['minimum']

        # Iteraate over tier point awards
        for codes in TIER_POINT_AWARDS:

            # Assign the correct tier point dictionary
            if self.code in codes:
                self._tier_points = TIER_POINT_AWARDS[codes]

    @property
    def avios_multiplier(self):
        """
        Multiplier used to calculate the number of avios earned for a flight
        """
        return self._avios_multiplier

    @property
    def minimum_avios(self):
        """
        Minimum number of avios that can be earned for a flight
        """
        return self._minimum_avios

    @property
    def tier_points(self):
        """
        Dictionary that maps different thresholds of flight distance to the number of tier points earned
        """
        return self._tier_points
