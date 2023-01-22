import flights

BA_BASES = ['LHR', 'LGW', 'LCY']

# Short haul destinations in a higher tier point earning category
SHORT_HAUL_PLUS = [
    'ATH', 'CHQ', 'CFU', 'HER', 'KLX', 'EFL', 'KGS', 'JMK', 'RHO', 'JTR', 
    'JSI', 'SKG', 'ZTH', 'LCA', 'PFO', 'LPA', 'ACE', 'TFS', 'MLA', 'KEF', 
    'AYT', 'DLM', 'IST', 'FNC', 'PDL', 'TER', 'TIA', 'SOF', 'OTP', 'CTA', 
    'ALG', 'RAC', 'HEL']

# Avios bonus for BA Exec Club status
STATUS_BONUS = {'blue': 0, 'bronze': 0.25, 'silver': 0.5, 'gold': 1}

# Floor value in pence based in Nectar conversion rate
AVIOS_FLOOR_VALUE = 0.67


class Trip():
    def __init__(self, itinerary, ticket_price):
        """
        Initialize a Trip object with an itinerary and ticket price

        :param itinerary: an Itinerary object
        :param ticket_price: a float representing the ticket price
        """
        self.itinerary = itinerary
        self.ticket_price = ticket_price


class BA_Trip(Trip):
    def __init__(self, itinerary, ticket_price, tier_status='blue'):
        """
        Initialize a BA_Trip object with an itinerary, ticket price, and Executive Club tier status
        :param itinerary: an Itinerary object
    :param ticket_price: a float representing the ticket price
    :param tier_status: a string representing the Executive Club tier status (default: 'blue')
    """
        super().__init__(itinerary, ticket_price)
        self.tier_status = tier_status

    def earns_avios_per_segment(self):
        """
        Returns a list of the number of avios earned in all segments of a itinerary
        """
        avios_earned = []
        for segment in self.itinerary.segments:
            
            # Intiialise avios for current segment to 0
            avios = 0

            # Calculate avios for each segment by summing the avios of each leg
            for leg in segment.legs:

                # Apply the fare class multiplier to the distance in miles of the leg
                avios_for_leg = round(self.itinerary.all_distances[tuple(leg)] 
                                        * segment.fare_class.avios_multiplier)

                # Ensure the minimum number of avios are collected
                if avios_for_leg < segment.fare_class.minimum_avios:
                    avios_for_leg = segment.fare_class.minimum_avios
                
                # Increment avios earned for the segment
                avios += avios_for_leg

            # Apply status bonus and append avios to the list
            avios_earned.append(round(avios * (1 + STATUS_BONUS[self.tier_status])))
        return avios_earned

    def earns_tier_points_per_segment(self):
        """
        Returns a list of the number of tier points earned in all segments of an itinerary
        """
        tier_points_earned = []
        for segment in self.itinerary.segments:

            # Intiialise tier points for the current segment to 0
            segment_tier_points = 0
            
            # Calculate tier points for each segment by summing the tier points of each leg
            for leg in segment.legs:

                # Check for short haul plus or SYD routs
                leg_tier_points = self.is_shp_or_syd(leg, segment.fare_class)
                if not leg_tier_points:

                    # Look up tier points by distance
                    distance = self.itinerary.all_distances[tuple(leg)]
                    leg_tier_points = self.tier_points_by_distance(distance, segment.fare_class)

                # Increment tier points for segment with tier points for leg
                segment_tier_points += leg_tier_points
            tier_points_earned.append(segment_tier_points)
        return tier_points_earned

    def tier_points_by_distance(self, distance, fare_class):
        """
        Return tier points for a leg based on distance
        """
        if distance < 2000:
            return fare_class.tier_points[2000]
        elif distance < 6000:
            return fare_class.tier_points[6000]
        elif distance < 10000:
            return fare_class.tier_points[10000]
        else:
            return fare_class.tier_points['SYD']

    def is_shp_or_syd(self, leg, fare_class):
            """
            Check whether a leg is a short haul plus or SYD route
            """
            
            # Departure and arrival airports
            depart = leg[0]
            arrive = leg[1]

            # Return the correct tier points if the leg is short haul plus
            if (depart in BA_BASES or arrive in BA_BASES) and (
                    depart in SHORT_HAUL_PLUS  or arrive in SHORT_HAUL_PLUS):
                    return fare_class.tier_points['SH+']

            # Return the correct tier points if the leg is SYD
            if (depart in BA_BASES or arrive in BA_BASES) and (
                    depart == 'SYD' or arrive == 'SYD'):
                    return fare_class.tier_points['SYD']
            return None

    def cost_per_tier_point(self):
        """
        Calculate the cost in ££ per tier point for the trip
        """
        # Divide the ticket price by the total number of tier points earned
        return round(self.ticket_price / sum(self.earns_tier_points_per_segment()), 2)


class BA_Flight_Redemption():
    def __init__(self, avios_required, cash_required):
        """
        Initialize a BA_Flight_Redemption object with values for avios and cash

        :param itinerary: an int representing the avios reuired for the redemption
        :param ticket_price: a float representing the cash required for the redemtion
        """
        self.avios_required = avios_required
        self.cash_required = cash_required

    def value_per_avios(self, ticket_price):
        """
        Calculates the value achieved in pence per avios for a redemption
        """
        # Divide the cash difference by the tier point required
        cash_saving = ticket_price - self.cash_required
        return round((cash_saving * 100) / self.avios_required, 2)

    def saving(self, ticket_price):
        """
        Calculates total saving based on the cash ticket price and avios floor value
        """
        # Calculate the equivalant cash value of redemption price
        avios_in_cash = (self.cash_required * 100) + (self.avios_required * AVIOS_FLOOR_VALUE)

        # Subtract the cash value of the redemption from the ticket price
        return round(ticket_price - (avios_in_cash / 100), 2)
