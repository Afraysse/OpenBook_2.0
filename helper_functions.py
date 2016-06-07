from model import * 

######## Helper Functions #########

def draft_submissions(user_id, published):
    """ Tallies the number of drafts published. """

    p_drafts = Published.query.filter_by(user_id=session['user_id']).all()

    publish_dicts = [publish.to_dict() for publish in published]

    count_pub = len(publish_dicts)

    return count_pub

# need to iterate through the dictionary to OR need to query for publish_id


def check_publish_id():
    