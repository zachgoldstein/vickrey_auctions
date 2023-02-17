from typing import List
from typing import Protocol
from statistics import fmean

class BidProtocol(Protocol):
    price: int
    id: int

# Example generic use of this could be via a dataclass instead of django model:
"""
from dataclasses import dataclass

@dataclass
class TestDummyBid():
    price: int
    id: int
"""

# def calculate_average_bid(bids: Union[QuerySet, List[Bid]]) -> float:
def calculate_average_bid(bids: List[BidProtocol]) -> float:
    return fmean([bid.price for bid in bids])

def calculate_top_n_average_bid(top_n:int, bids: List[BidProtocol]) -> float:
    desc_price = sorted(bids, key=lambda bid: bid.price) 
    return fmean([bid.price for bid in bids[:top_n]])

# # get top auction.num_items + 1 bid
def get_winning_bids(top_n:int, bids: List[BidProtocol]) -> List[BidProtocol]:
    desc_price = sorted(bids, key=lambda bid: bid.price, reverse=True) 
    return desc_price[:top_n]

def get_winning_price(top_n:int, bids: List[BidProtocol]) -> float:
    desc_price = sorted(bids, key=lambda bid: bid.price) 
    return desc_price[top_n+1].price

def get_recommendations(bids: List[BidProtocol]) -> List[str]:
    return [
        f"The top X bids were X% higher than the average price, consider commisions?", 
        f"The average price of all bids was $XYZ",
        f"The average price of the top n bids was $XYZ",
        f"There was X times as many bids as the number of items for sale, consider a run of X items at the average price of $XYZ",
    ]
    pass
