""" Algo functions for sorting and recommending lodgings """


def sort_and_filter_lodgings(lodgings_list):
    """ sort the lodgings by total price and ratings
    return the cheapest and best rated (with most reviews)"""
    # add top result
    lodgings_list[0].tags.append("top result")
    final_recommendation_set = {lodgings_list[0]}
    # filter list with ratings
    filtered_list = filter_ratings_only(lodgings_list)

    cheapest = sort_and_find_cheapest(filtered_list)
    best_rated = sort_and_find_best_ratings(filtered_list)
    most_booked = sort_and_find_most_ratings(filtered_list)

    final_recommendation_set.add(cheapest)
    final_recommendation_set.add(best_rated)
    final_recommendation_set.add(most_booked)

    return final_recommendation_set


def filter_ratings_only(lodgings_list):
    """ filter out the listings with no ratings """
    def filter_ratings(lodging):
        if lodging.rating and lodging.num_ratings > 5:
            return True
        return False
    return [*filter(filter_ratings, lodgings_list)]


def sort_and_find_cheapest(lodgings_list):
    """ sort the list and find the cheapest lodging
    and return the cheapeast"""
    sorted_by_price = sorted(lodgings_list,
                             key=lambda l: int(l.total_price[1:].replace(",", "")))
    cheapest = sorted_by_price[0]
    cheapest.tags.append("cheapest")
    return cheapest


def sort_and_find_best_ratings(lodgings_list):
    """ sort the list and find the best rated lodging,
    return it 
    TODO: custom sort function that incorporates less/no ratings
    """
    sorted_by_rating = sorted(lodgings_list,
                              key=lambda l: l.rating,
                              reverse=True)
    best_rated = sorted_by_rating[0]
    best_rated.tags.append("best rated")
    return best_rated


def sort_and_find_most_ratings(lodgings_list):
    """ sort the list and find the most rated lodging,
    return it
    """
    sorted_by_rating = sorted(lodgings_list,
                              key=lambda l: l.num_ratings,
                              reverse=True)
    most_booked = sorted_by_rating[0]
    most_booked.tags.append("most popular")
    return most_booked
