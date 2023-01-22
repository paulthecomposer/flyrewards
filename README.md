# **flyrewards**

A python package to calculate the rewards earned from air travel, specifically for British Airways.

## **Description**

The flyrewards package is a collection of modules designed to calculate the rewards earned from air travel.

It has three main components:

Itinerary: This module takes a list of segments, each containing a list of airports and a fare class. It calculates the distance between each pair of airports in the itinerary, and also provides a method to return the distance for each segment.

FareClass: This module takes a fare class code as input and returns the Avios multiplier, minimum Avios, and Tier points earned for that fare class.

BA_Trip: This module inherits from the Trip class and calculates the Avios and Tier points earned for a British Airways trip based on the itinerary, ticket price, and Executive Club status. It also provides a method to calculate the Avios value of the trip based on the Avios earned and the ticket price.

To use the package, create an instance of the BA_Trip class by passing in an instance of the Itinerary class, the ticket price, and the Executive Club status. Then use the provided methods to calculate the rewards earned.

Please note that the package is designed for British Airways, for other airlines you have to create a new class like BA_Trip and configure it accordingly.

## **Usage**

`from flyrewards.itinerary import Itinerary`
`from flyrewards.fare_classes import FareClass`
`from flyrewards.ba_trip import BA_Trip`

`# Create an itinerary with segments, each containing a list of airports and a fare class`
`segments = [`
    `([ "LHR", "JFK", "SFO"], 'R'),`
   ` ([ "SFO", "LHR"], 'F'),`
`]`
`itinerary = Itinerary(*segments)`

`# Create a BA_Trip instance by passing in the itinerary, ticket price, and Executive Club status`
`trip = BA_Trip(itinerary, 500, 'silver')`

`# Use the provided methods to calculate the rewards earned`
`avios_earned = trip.earns_avios_per_segment()`
`tier_points_earned = trip.earns_tier_points_per_segment()`

`print(f"Avios Earned: {avios_earned}")`
`print(f"Tier Points Earned: {tier_points_earned}")`

## **Features**

Calculates the distance between each pair of airports in the itinerary
Returns the distance for each segment
Returns the Avios multiplier, minimum Avios, and Tier points earned for a fare class
Calculates the Avios and Tier points earned for a British Airways trip based on the itinerary, ticket price, and Executive Club status
Calculates the cost per tier point for a trip based on the tier points earned and the ticket price
Calculates the value in pence per avios for a flight redemption
Calculates the total saving for a flight redemtion based on the cash price of an equivalent ticket and the avios floor value

## **License**

This project is licensed under the MIT License.
