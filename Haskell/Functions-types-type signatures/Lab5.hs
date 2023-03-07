module Lab5 where 
  thirdLast list = 
    if (length list == 3) then head list
    else thirdLast (tail list)

  everyOther [] = []
  everyOther [e] = e:[]
  everyOther (e0:e1:li) = e0: everyOther li

  sumPosList [] = 0
  sumPosList (e:li) = 
    if (e > 0) then e + sumPosList li
    else sumPosList li

    
  