def sum_exists(n, i, p_list):
    # Returns True if n can be formed from p_list repeated
    # some arbitrary number of times.
    print(n, p_list[i])
    
    if (n - p_list[i] == 0):
        # we found a sum form the list!
        return True
    elif (n - p_list[i] < 0):
        # this sum doesn't work, move on to the next index
        return False
    for x in range(i, len(p_list)):
        if (sum_exists (n - p_list[x], x, p_list) == True):
            return True
    
    # this sum doesn't work, move on to the next index
    return False