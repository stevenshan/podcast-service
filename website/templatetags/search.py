from django import template

register = template.Library()

# # calculate the change in subscribers based on
# # subscribers_last_week and subscribers
# # used as a measure of what's trending
# def calculateWeeklyIncrease(subscribersLastWeek, subscribers):
#     try:
#         change = float(subscribersLastWeek) / subscribers

#         # format floating point to string
#         change = int(round(change * 100,1))
#         change = "+" + str(change) + "%"
#     except:
#         change = "-"
#     return change

# register.filter("calculateWeeklyIncrease", calculateWeeklyIncrease)