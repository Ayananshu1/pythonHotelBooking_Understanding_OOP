import pandas
#import streamlit
df=pandas.read_csv("hotels.csv",dtype={"id":str})
df_data=pandas.read_csv("cards.csv",dtype=str).to_dict(orient="records")
df_data_security=pandas.read_csv("card_security.csv",dtype=str)

class Hotel:
    def __init__(self,hotel_id):
        self.hotel_id=hotel_id
        self.name=df.loc[df["id"]==self.hotel_id,"name"].squeeze()
    def book(self):
        """Book an available hotel by changing its availability to No"""
        df.loc[df["id"]==self.hotel_id,"available"]="no"
        df.to_csv("hotels.csv",index=False)


    def available(self):
        """Check if the hotel is available"""
        availability=df.loc[df["id"]==self.hotel_id,"available"].squeeze()
        if availability=="yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self,customer_name,hotel_obj):
        self.customer_name=customer_name
        self.hotel_obj=hotel_obj
    def generate(self):
        content=f"""
        Thank you for your Reservation
        Name:{self.customer_name}
        Hotel_name:{self.hotel_obj.name}
        """
        return content

class Creditcard:
    def __init__(self,cardnumber):
        self.cardnumber=cardnumber
    def validate(self,cvc,expiration,holder):
        card_data={"number":self.cardnumber,"cvc":cvc,"expiration":expiration,
                   "holder":holder}

        if card_data in df_data:
            return True
        else:
            return False

class SecureCreditCard(Creditcard):
    def authenticate(self,entered_password):
        password=df_data_security.loc[df_data_security["number"]==self.cardnumber,"password"].squeeze()
        if password==entered_password:
            return True
        else:
            return False

hotelid=input("Enter the Hotel id")
hotel=Hotel(hotelid)

if hotel.available():
    number1=input("Enter Credit card number")
    expiry=input("Enter expiration date")
    holder_name=input("Enter card holder name")
    cvc1=input("Enter cvc")

    credit_card=SecureCreditCard(number1)
    if credit_card.validate(cvc1,expiry,holder_name):
        entered_password=input("Enter password")
        if credit_card.authenticate(entered_password):
            hotel.book()
            name=input("Enter your name")
            reservation_ticket=ReservationTicket(name,hotel)
            print(reservation_ticket.generate())
        else:
            print("Authentication Failed")
    else:
        print("There was a problem with your payment")
else:
    print("Hotel is not free")

