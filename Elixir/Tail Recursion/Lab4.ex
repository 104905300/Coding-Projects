defmodule Lab4 do
  def sumEven([]) do 
    0
  end

  def sumEven(li) do 
    sumEven(li, 0)
  end
 
  def sumEven([h | t], sum) do
    cond do
      (is_number(h) && (rem(h, 2) === 0)) ->
        sumEven(t, h + sum)
      true -> # catch all condition (not even)
        sumEven(t, sum)   
    end
  end
  
  def sumEven([], sum) do
    sum
  end
    

  def sumNum([]) do 
    0
  end
  
  def sumNum(li) do 
    sumNum(li, 0)
  end
  
  def sumNum([h | t], sum) do 
    cond do
      is_number(h) ->
        sumNum(t, h + sum)
      true -> # catch all condition (not a number)
        sumNum(t, sum)   
    end
  end

  def sumNum([], sum) do
    sum
  end


  def tailFib(num), do: tailFib(num, 0, 1) #get fib number but do it from num to 0
  def tailFib(0, firAdder, _), do: firAdder
  def tailFib(num, firAdder, secAdder), do: tailFib(num-1, secAdder, firAdder+secAdder)


  # checks for empty list
  def reduce([], _), do: 0
  # checks for empty list for 3 arguments. This is also the base case
  def reduce([], acc, _) when(is_number(acc)), do: acc

  # the two below are for entry cases
  def reduce(list, f), do: reduce((tl list), (hd list), f)
  def reduce([h | t], acc, f) when(is_number(acc)), do: reduce(t, f.(h, acc), f)

end
