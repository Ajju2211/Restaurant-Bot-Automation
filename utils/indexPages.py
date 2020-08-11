def indexPages(numOfThings, limitThingsPerPage):
  totalPages = int(numOfThings / limitThingsPerPage)
  rem = numOfThings % limitThingsPerPage
  lastPagecount = rem
  if rem == 0:
    lastPagecount = limitThingsPerPage
  else:
    totalPages = totalPages +1
  defaultPageCount = limitThingsPerPage
  firstPageCount = defaultPageCount
  if totalPages == 0:
    firstPageCount = lastPagecount
  indexPages = {}
  start , end = 1 , 0
  # If only one page their set as firstPage
  # otherwise firstpage ovewritten in loop
  indexPages["1"] = {"startIndex": 1,"endIndex": firstPageCount}
  for i in range(1,totalPages+1):
    if i == totalPages:
      end = numOfThings      
      start = end - lastPagecount + 1
    else :
      end = i * defaultPageCount
      start = end - defaultPageCount + 1
    pageObj = { "startIndex": start , "endIndex": end}
    indexPages[str(i)] = pageObj

  #   set current page index to keep track of pages after calling this function
  #   indexPages["currentPage"] = 1 ;
  #   save result of this function & update indexPages["currentPage"] = currentPageVaue
  return { "indexPages": indexPages, "firstPageCount": firstPageCount }

# print(indexPages(13, 3))



