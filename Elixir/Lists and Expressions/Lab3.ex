defmodule Lab3 do
  def firstTwo(li) do
    [first_ele | [second_ele | _]] = li
    first_ele === second_ele
  end
  
  def evenSize(li) do
    rem(length(li), 2) === 0
  end

  def frontBack(li) do
    [first_ele | tail] = li
    tail ++ [first_ele]
  end

  def nextNineNine(li) do
      [first_ele | tail] = li
      [first_ele | [99 | tail]]
  end 

  def isCoord(li) do
      (length(li) >= 2) && is_number(hd li) && is_number(hd (tl li))
  end 

  def helloIfSo(li) do
    new_list = li -- ["Hello"]
    new_list ++ ["Hello"]
  end 
end

