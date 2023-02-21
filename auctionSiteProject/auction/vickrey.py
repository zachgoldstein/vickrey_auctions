from typing import List
from typing import Protocol
from statistics import fmean

class BidProtocol(Protocol):
    price: int
    id: int

COMMISSION_RECCO_DIFF_PERC = 150
LARGER_RUN_RECCO_DIFF_PERC = 200

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

def get_recommendations(top_n:int, bids: List[BidProtocol]) -> List[str]:
    average_bid = calculate_average_bid(bids)
    # top_n_average_bid = calculate_top_n_average_bid(top_n, bids)
    top_bids_average_bids_diff = get_top_bid_average_bid_diff(top_n, bids)
    
    recommendations: List[str] = []
    if top_bids_average_bids_diff > COMMISSION_RECCO_DIFF_PERC:
        recommendations.append(f"The top {top_n} bids were {top_bids_average_bids_diff:.2f}% higher than the average price, consider commisions?")

    bid_quantity_diff = get_bid_quantity_diff(top_n, bids)
    if  bid_quantity_diff > LARGER_RUN_RECCO_DIFF_PERC:
        recommendations.append(f"There was {bid_quantity_diff:.2f}% as many bids as the number of items for sale, consider a run of {len(bids)} items at the average price of {average_bid}",)

    return recommendations

def get_top_bid_average_bid_diff(top_n:int, bids: List[BidProtocol]):
    average_bid = calculate_average_bid(bids)
    top_n_average_bid = calculate_top_n_average_bid(top_n, bids)
    return top_n_average_bid / average_bid * 100

def get_bid_quantity_diff(top_n:int, bids:List[BidProtocol]):
    return len(bids) / top_n * 100