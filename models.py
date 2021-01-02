from datetime import datetime
import itertools


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







