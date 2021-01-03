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
    def __init__(self, total_price):
        self.flights = []
        self.total_price = total_price
 
    def add_flight(self, flight):
        self.flights.append(flight)


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
        self.airlines = []
        self.airport_origin = airport_origin
        self.airport_destination = airport_destination
        self.price = None
        self.takeoff_time = takeoff_time
        self.landing_time = landing_time
        self.connections = int(connections)
        self.duration = duration
    
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
    """ list of flights """
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







