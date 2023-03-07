import math

def getName():
    #This method must return your name EXACTLY as D2L presents it.
    #If this does not work, you will fail this lab.
	return "Hai Ning Liu"

def sum_exists(n, i, p_list):
    # Returns True if n can be formed from p_list repeated
    # some arbitrary number of times.

    # I am subtracting n from some combo of p_list until I reach 0
    # if can't reach 0 from all possible combo, return false

    if (n == 0):
        # we found a sum form the list!
        return True
    elif (n < p_list[i]):
        # this sum doesn't work, move on to the next index
        return False
    
    for x in range(i, len(p_list)):
        if (n < p_list[x]):
            # to big for n to subtract the remaining num in p_list, go back one level up 
            return False

        if (sum_exists (n - p_list[x], x, p_list) == True):
            return True 
    
    # this sum doesn't work, move on to the next index
    return False


def find_sum(n, i, p_list, sum_list):
    # Returns a list of primes from p_list repeated some
    # arbitrary number of times so that it sums to n

    if (n == 0):
        # we found a sum form the list!
        return sum_list
    elif (n < p_list[i]):
        # this sum doesn't work, move on to the next index
        return []
    
    for x in range(i, len(p_list)):
        if (n < p_list[x]):
            # too big for n to subtract the remaining num in p_list, go back one level up
            # for exmaple find sum to 5 from list [7,9,34], list is ordered from smallest 
            # to largest. If 5 can't subtract from 7 then it can't subtract from 9 and 34 
            return []

        # try to sum from a current number on the list
        sum_list.append(p_list[x])
        result_list = find_sum (n - p_list[x], x, p_list, sum_list)
        
        if (result_list != []):
            # we found a combo match!
            return result_list
        
        # if it reach here that means a base case is reached and current sum doesn't work,
        # return an empty list(temporary, a sum_list can be the new return if a sum is found) 
        # and pop the last number, then either add the next number from the list or if the 
        # loop is finished go back one level up and pop/add number again. If no more 
        # numbers can be added it means no sum works and return the empty list to the user
        sum_list.pop()


    # this sum doesn't work, move on to the next index
    return []


