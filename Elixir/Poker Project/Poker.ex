defmodule Poker do
  def deal(li) do
    [fpCardOne|[spCardOne|[fpCardTwo|[spCardTwo|pool]]]] = li
    firstPlayerPool = [fpCardOne|[fpCardTwo|pool]]
    secondPlayerPool = [spCardOne|[spCardTwo|pool]]

    # tuple card list is great for checking for appropriate rank of hand
    fTupleCardList = numListTotupleCardList(firstPlayerPool)
    sTupleCardList = numListTotupleCardList(secondPlayerPool)

    fBestHand = checkForFlush(fTupleCardList)
    fBestHand = case fBestHand do [] -> checkForStraight(fTupleCardList); _ -> fBestHand end
    fBestHand = case fBestHand do [] -> checkForDups(fTupleCardList); _ -> fBestHand end

    sBestHand = checkForFlush(sTupleCardList)
    sBestHand = case sBestHand do [] -> checkForStraight(sTupleCardList); _ -> sBestHand end
    sBestHand = case sBestHand do [] -> checkForDups(sTupleCardList); _ -> sBestHand end

    bestHand = cond do (fBestHand >= sBestHand) -> fBestHand; true -> sBestHand end
    tupleListToStringCardList(tl bestHand) # last line of method is return value
  end
#******************************************************************************

  def numListTotupleCardList([]) do 
    []
  end

  # recursively go through each card in the list
  def numListTotupleCardList([curCard | rest]) do 
    suit = cond do
      (1 <= curCard and curCard <= 13) -> "C"
      (14 <= curCard and curCard <= 26) -> "D"
      (27 <= curCard and curCard <= 39) -> "H"
      (40 <= curCard and curCard <= 52) -> "S"
    end

    num = rem(curCard - 1, 13) + 1
    # popolate tuple card list
    cond do
      num == 1 -> 
        [{14, suit} | numListTotupleCardList(rest)]
      true ->
        [{num, suit} | numListTotupleCardList(rest)]
    end
  end
#******************************************************************************

  def tupleListToStringCardList([]) do 
    []
  end

  # recursively go through each card in the list
  def tupleListToStringCardList([curCard | rest]) do 
    stringCard = case curCard do
      {14, _} -> "1" <> elem(curCard,1) # change Ace from 14 to 1
      _ -> to_string(elem(curCard,0)) <> elem(curCard,1)
    end
    [stringCard | tupleListToStringCardList(rest)]
  end
#******************************************************************************

  def checkForFlush(li) do
    clubs = for {a, "C"} <- li, do: {a, "C"}
    diamonds = for {a, "D"} <- li, do: {a, "D"}
    hearts = for {a, "H"} <- li, do: {a, "H"}
    spades = for {a, "S"} <- li, do: {a, "S"}
    
    suits = [clubs, diamonds, hearts, spades]
    # check if there is flush (5 cards or more of the same suit)
    flush = for list <- suits, Enum.count(list) >= 5, do: list #extra bracket if flush found!

    flush = case flush do
      [] -> []
      _ -> Enum.at(flush, 0) # remove extra brakcet if list is not empty
    end

    # Anonymous Functions to take care of flush
    flushHanlder = fn
      [] -> []
      #if flush exist, sort by descending order, then take the 5 biggest card from flush
      _ -> [6 | Enum.take(Enum.sort(flush, &(&1 >= &2)), 5)]
    end

    straightFlush = checkForStraight(flush)
    case straightFlush do
      [] -> flushHanlder.(flush)
      _ -> [9 | (tl straightFlush)]
    end
  end
#******************************************************************************

  def checkForStraight(li) do
    case li do
      [] -> [] # return input list if empty
      _ -> 
        # make sure list is in descending order 
        li = Enum.sort(li, &(&1 >= &2))
        index = checkForStraight((tl li), (hd li), 1, 1)
        case index do
            -1 -> # only wheel straight or no straight exist
              cond do
                elem(Enum.at(li, 0),0) == 14 and elem(Enum.at(li, -4),0) == 5 and elem(Enum.at(li,                   -3),0) == 4 and elem(Enum.at(li, -2),0) == 3 and elem(Enum.at(li, -1),0) == 2 ->
                  # check if wheel straight (A2345) exist, 
                  # only check if no other straight exist since this is the smallest straight
                  suitAtAce = elem(Enum.at(li, 0),1)
                  [5 | Enum.take(li, -4) ++ [{1, suitAtAce}]] # return wheel straight
                true -> [] # else no straight exist, return empty list
              end
            # ind is end index of straight, 
            # it's overcounted by 1, so use index - 5 instead of index - 4
            _ -> [5 | Enum.slice(li, index-5, 5)] # get the 5 cards of the straights!
        end
    end
  end

  # base case 1: list finished traversal
  def checkForStraight([], _, straightCount, ind) do
    case straightCount do
       # Stragith exist! return the end index of straight for straight creation later
      5 -> ind
      # straight doesn't exist, use -1 index to represent that
      _ -> -1
    end
  end

  # base case 2: stragiht found
  def checkForStraight(_, _, 5, ind) do
    ind
  end

  # recursive case
  def checkForStraight([secComp|rest], firstComp, straightCount, ind) do
    cond do
      # if cur num is one more than the next, straight count + 1
      (elem(firstComp,0) - elem(secComp,0) == 1) -> 
          checkForStraight(rest, secComp, straightCount+1, ind+1)
      # if not, reset straight count to 0
      true -> checkForStraight(rest, secComp, 1, ind+1)
    end
  end
#******************************************************************************

  def checkForDups(li) do
    # create a map that counts frequency of each card num
    dupMap = Enum.frequencies_by(li, &elem(&1, 0))
    # sort by frequency, then by card num
    dupsGroup = Enum.sort_by(li,  &{dupMap[elem(&1,0)], elem(&1,0)}, :desc)
    
    dupMapList = Map.to_list(dupMap)
    cond do
      # if any quads exist
      Enum.any?(dupMapList, fn {_, feq} -> feq == 4 end) ->
        quad = Enum.take(dupsGroup, 4)
        kicker = Enum.max(Enum.drop(dupsGroup, 4))
        [8 | (quad ++ [kicker])] # quads
      Enum.any?(dupMapList, fn {_, feq} -> feq == 3 end) ->
        cond do
          elem(Enum.at(dupsGroup,3),0) == elem(Enum.at(dupsGroup,4),0) ->
              [7 |Enum.take(dupsGroup, 5)] # fullhouse
          true ->
              [4 |Enum.take(dupsGroup, 5)] # three of a kind
        end 
      Enum.any?(dupMapList, fn {_, feq} -> feq == 2 end) ->
        cond do
          elem(Enum.at(dupsGroup,2),0) == elem(Enum.at(dupsGroup,3),0) ->
            twoPair = Enum.take(dupsGroup, 4)
            kicker = Enum.max(Enum.drop(dupsGroup, 4))
            [3 | (twoPair ++ [kicker])] # two pair
          true ->
            [2 |Enum.take(dupsGroup, 5)] # one pair
        end
      true ->
        [1 |Enum.take(dupsGroup, 5)] # high card
    end
  
  end
end