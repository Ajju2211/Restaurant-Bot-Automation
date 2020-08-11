from utils import indexPages as inP
# suppose user queries for dosa and found these
# currently I'm limiting 3 dishes per page
# each page is indexed from 1-N and Each page contains 1-M dishes

queriedSimdishes = ["dosa","neer dosa","panir dosa","butter dosa","plain dosa","aloo dosa","masala dosa"]
numOfDishes = len(queriedSimdishes)
limiDishesPerPage = 3
print(inP.indexPages(numOfDishes, limiDishesPerPage))
# # output: 
# {
# 'indexPages':
#  {
#  '1': {'startIndex': 1, 'endIndex': 3},
#  '2': {'startIndex': 4, 'endIndex': 6}, 
#  '3': {'startIndex': 7, 'endIndex': 7}
#  }, 
#  'firstPageCount': 3
#  }
#  assign it to dishIndexPages variable
#  dishIndexPages["currentPage"] = currentPage
 
# save in dishIndexPages.json




