#helper functions to allow a user to have friends

from model import Relations, User
from model import db

def friend_or_pending(user_a_id, user_b_id):
    """
    Checks the friend status between user_a and user_b. 

    Checks if user_a and user_b are friends. 
    Checks if there is a pending friend request from user_a to user_b. 
    """

    is_friends = db.session.query(Relations).filter(Relations.user_a_id == user_a_id,
                                                    Relations.user_b_id == user_b_id,
                                                    Relations.status == "Accepted").first()

    is_pending = db.session.query(Relations).filter(Relations.user_a_id == user_a_id,
                                                    Relations.user_b_id == user_b_id,
                                                    Relations.status == "Requested").first()

    return is_friends, is_pending

def get_friend_requests(user_id):
    """
    Get user's friend requests.

    Returns users that user received friend requests from.
    Returns users that user sent friend requests to.

    """

    received_friend_requests = db.session.query(User).filter(Relations.user_b_id == user_id,
                                                            Relations.status == "Requested").join(Relations,
                                                                                                Relations.user_a_id == User.user_id).all()
    sent_friend_requests = db.session.query(User).filter(Relations.user_a_id == user_id,
                                                        Relations.status = "Requested").join(Relations,
                                                                                            Relations.user_b_id == User.user_id).all()
    return received_friend_requests, sent_friend_requests

def get_friends(user_id):
    """
    Return a query for user's friends

    Note: this does not reture User object, just the query
    """

    friends = db.session.query(User).filter(Relations.user_a_id == user_id,
                                            Relations.status == "Accepted").join(Relations,
                                                                                Relations.user_b_id == User.user_id)


    