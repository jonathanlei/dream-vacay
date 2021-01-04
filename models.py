from datetime import datetime


class Lodging():
    """ single lodging """
    def __init__(self, img_url, rating, room_type, description, total_price):
        self.img_url = img_url
        self.rating = rating
        self.room_type = room_type
        self.description = description
        self.total_price = total_price

    @classmethod
    def fromdict(cls, d):
        allowed = ("img_url", "rating", "room_type", "description", "total_price")
        df = {k: v for k, v in d.items() if k in allowed}
        return cls(**df)


class Lodgings_List():
    """ list of lodgings """
    def __init__(self, location, checkin, checkout, adults):
        self.location = location
        self.checkin = checkin
        self.checkout = checkout
        self.adults = adults
        self.searchTime = datetime.utcnow()
        self.lodgings = []

    def add_lodging(self, lodging):
        self.lodgings.append(lodging)

    @classmethod
    def fromdict(cls, d):
        allowed = ("location", "checkin", "checkout", "adults")
        df = {k: v for k, v in d.items() if k in allowed}
        return cls(**df)


# Flight data classes

class RoundTripFlights():
    """ Round trip flights"""
    def __init__(self, total_price, origin_flight, return_flight, statuses):
        self.total_price = total_price
        self.origin_flight = origin_flight
        self.return_flight = return_flight
        self.statuses = statuses

    def __repr__(self):
        return f""" <ROUND TRIP FLIGHT: 
                    Total Price : {self.total_price}
                    Origin Flight : {self.origin_flight.__repr__()}
                    Return Flight : {self.return_flight.__repr__()}
                    Statuses : {self.statuses}>\n"""


class Flight():
    """ single flight """
    def __init__(
                 self,
                 airlines,
                 airport_origin,
                 airport_destination,
                 takeoff_time,
                 landing_time,
                 connections,
                 duration,
                 ):
        self.airlines = airlines
        self.airport_origin = airport_origin
        self.airport_destination = airport_destination
        self.price = None
        self.takeoff_time = takeoff_time
        self.landing_time = landing_time
        # list of connections
        self.connections = connections
        self.num_stops = len(connections)
        self.duration = duration

    def __repr__(self):
        return f"""<Flight : Airline: {self.airlines["name"]}
                            Origin: {self.airport_origin}
                            Destination: {self.airport_destination}
                            Price : {self.price}
                            Takeoff time : {self.takeoff_time}
                            Landing time : {self.landing_time}
                            Connections: {self.connections}
                            Duration : {self.duration}>"""
    @classmethod
    def fromdict(cls, d):
        allowed = (
            "airlines",
            "airport_origin",
            "airport_destination",
            "price",
            "takeoff_time",
            "landing_time",
            "connections",
            "duration",
            )
        df = {k: v for k, v in d.items() if k in allowed}
        return cls(**df)

  
class Flights_List():
    """ list of flights 
    TODO: Consider changing to city_origin and city_destination becuase each flight
    already contains info about airports but the Flights_List will be based on a single
    query from one city to another
    """
    def __init__(
                 self,
                 airport_origin,
                 airport_destination,
                 outbound_date,
                 inbound_date,
                 adults,
                 ):
        self.airport_origin = airport_origin
        self.airport_destination = airport_destination
        self.outbound_date = outbound_date
        self.inbound_date = inbound_date
        self.adults = adults
        self.searchTime = datetime.utcnow()
        self.flights = []
    
    def __repr__(self):
        """ Readable representation String for list of RoundTripFlights """

        return f""" <Flights List
            Airport Origin: {self.airport_origin}
            Airport Destination: {self.airport_destination}
            Outbound Date: {self.outbound_date}
            Inbound Date: {self.inbound_date}
            Adults: {self.adults}
            Search Time: {self.searchTime}
            Flights: {self.flights}>"""

    def add_flight(self, flight):
        self.flights.append(flight)

    @classmethod
    def fromdict(cls, d):
        allowed = (
                   "airport_origin",
                   "airport_destination",
                   "outbound_date",
                   "inbound_date",
                   "adults",
                   )
        df = {k: v for k, v in d.items() if k in allowed}
        return cls(**df)







# trips class 
# dates
# destination 
# num of guests 
# budget

# trips list 
    # dates
    # destination
    # origin 
    # guests 

    # flights list 
    # lodgings list 

# trip subclass 
    # dates
    # destination
    # origin 
    # guests 

    # flight 
    # lodging
    # total price


# flight class - back end class
    # dates
    # location (origin - destination)
    # price
    # number of guests
    # airline
    # time 
    # duration 
    # layovers


# lodging class
    # dates
    # location 
    # price 
    # number of guests/beds 
    # images url






# Tables

# flights
  #ID
  #

# lodgings




# flight class 
# location (from and to)
# price 


# lodging class 
# price 
# picture url







