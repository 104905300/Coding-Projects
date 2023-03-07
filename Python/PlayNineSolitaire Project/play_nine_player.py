# An example player agent for the Play Nine Solitaire project. This version doesn't
# make any decisions on its own, but asks the human to provide the decisions via
# console input.

# Version December 6, 2021, Ilkka Kokkarinen

# The three functions to implement begin here:
# --------------------------------------------

# Returns a tuple of two strings, the name and the student ID of the author.

def get_author_info():
    return "Hai Ning Liu", "501155767"


# Choose the drawing action for the current draw. The return value of this function
# must be either string "k" or "d" for taking the known card from the kitty and for
# drawing a random card from the deck, respectively.

def choose_drawing_action(top_concealed, bottom_concealed, draws_left, kitty_card):
    action = ai_kitty_action(top_concealed, bottom_concealed, draws_left, kitty_card)
    return action

    # action = "X"
    # while len(action) != 1 or action not in "kdKD":
        # action = input("Will you take the (k)itty card or (d)raw from deck? ")
    # return action



# Choose the replacement action for the current card. The return value of this function
# must be a triple of the form (action, row, column) where
# - action is one of the characters "rRtT", "r" for replace and "t" for turn over
# - row is the row number of the card subject to chosen action
# - column is the column number of the card subject to chosen action

def choose_replacement_action(top_concealed, bottom_concealed, draws_left, current_card):
    result_tuple = ai_replace_or_turn_action(top_concealed, bottom_concealed, draws_left, current_card)
    return result_tuple[0], result_tuple[1], result_tuple[2]

    #action = "X"
    #while len(action) != 1 or action not in "rRtT":
        #action = input(f"Will you (r)eplace or (t)urn over a board card? ")
    #action_verb = "replace" if action in "rR" else "turn over"
    #row = int(input(f"Enter row number of card to {action_verb}: "))
    #column = int(input(f"Enter column number of card to {action_verb}: "))
    #return action, row, column




# take kitty card if (list by priority)
  # take if < 5
  # check for matching and profit
  # take if exist matching (even if matching is not the optimal play, this card is probably small and can benifit in
  # other spots)
  # if less than 4 draws left, take the biggest profit
  # take if (5 or 6) and there is profit and draw is less than 4 
  # don't take if > 6 
  # don't take if there is no profit

def ai_kitty_action(top_row, bottom_row, draws_left, kitty):

  if(kitty < 1):
    return 'k'
  
  # found matching
  for ind in range(len(top_row)):
    if ((top_row[ind] == kitty or bottom_row[ind] == kitty) and bottom_row[ind] != top_row[ind]):
      return 'k'
    
  return 'd'


  
# if draws_left >= 3:
  # replace if matching exist
  # if no matching exist, replace if current_card is <= 5, by the biggest x > 5 that's not matching
  # if current_card is <=5 but no x > 5 that's not matching exist, replace it with any unknown card (this case it's the last index bc of my design)
  # if current_card > 5 , turn over the last unknwon card
# if draws_left < 3:
  # replace by biggest profit
def ai_replace_or_turn_action(top_row, bottom_row, draws_left, current_card):
  
  # you can't get profit that's lower than -100, so you can only go up from here
  biggest_profit = -100
  biggest_profit_ind = (0, 0)
  
  matching_profit = -1000
  matching_index = (-1, -1)
  
  num_of_matches = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  # highest card on the borad that's not matched to a pair, we need it to decide if we should replace or flip over
  h_unmatched_card = -100
  h_unmatched_ind = (-1, -1)
  num_of_stars = 0
  star_column = (-1, -1)
  last_star_ind = (-1, -1)

  # first iteration of the board, find all the matched pairs, the matching_index if any, and find the highest unmatched card and find the index of the last '*'
  for ind in range(len(top_row)):
    if (top_row[ind] == '*' and bottom_row[ind] == '*'):
        star_column = (0, ind)
    if (top_row[ind] == '*'):
      last_star_ind = (0, ind)
      num_of_stars = num_of_stars + 1
    if (bottom_row[ind] == '*'):
      last_star_ind = (1, ind)
      num_of_stars = num_of_stars + 1
    
    if (top_row[ind] != '*' and top_row[ind] != bottom_row[ind]):
        if (top_row[ind] > h_unmatched_card):
          h_unmatched_card = top_row[ind]
          h_unmatched_ind = (0, ind)
    if (bottom_row[ind] != '*'and top_row[ind] != bottom_row[ind]):
        if (bottom_row[ind] > h_unmatched_card):
          h_unmatched_card = bottom_row[ind]
          h_unmatched_ind = (1, ind)
    if (top_row[ind] != '*' and top_row[ind] == bottom_row[ind]):
      # find all matched pair and record all their occurance for calculating profit
      if (top_row[ind] == -5):
        num_of_matches[13] = num_of_matches[13] + 1
      else:
        num_of_matches[top_row[ind]] = num_of_matches[top_row[ind]] + 1
    else:
      # don't overwrite matching index if they are already matched
      # find matching index if any
      if (top_row[ind] == current_card):
        matching_index = (1, ind)
      if (bottom_row[ind] == current_card):
        matching_index = (0, ind)

  # second iteration of the board, find the biggest profit for inserting in each spot for the top and bottom row
  for ind in range(len(top_row)):
    # profit for changing a matched column is possible (tho very unlikely), BUT you shouldn't do it bc replacing the "*" instead should be more benifical (assuming expected value of star is around 6)
    if (top_row[ind] != '*' and top_row[ind] == bottom_row[ind]): continue
      
    cur_profit = profit(num_of_matches, [top_row[ind], bottom_row[ind]], 0, current_card)
    
    # record the highest matching profit if match is found
    if (current_card == bottom_row[ind]):
      matching_profit = max(matching_profit, cur_profit)
      
    if (cur_profit > biggest_profit):
      biggest_profit = cur_profit
      biggest_profit_ind = (0, ind)

  for ind in range(len(bottom_row)):
    if (bottom_row[ind] != '*' and top_row[ind] == bottom_row[ind]): continue
      
    cur_profit = profit(num_of_matches, [top_row[ind], bottom_row[ind]], 1, current_card)
    if (current_card == top_row[ind]):
      matching_profit = max(matching_profit, cur_profit)
          
    if (cur_profit > biggest_profit):
      biggest_profit = cur_profit
      biggest_profit_ind = (1, ind)


  # don't flip over the last card if score will be 10+, unless draw == 1
  # go for the most profitable that's does not involve the last star (replace or flip) 
  # if you are going for the highest unmatch and the profit is big net negative (<=-5), end the game by flipping or replacing
    # flip over if cur_card > 5
    # else replace the last star
  if (num_of_stars == 1):
    if (last_star_ind[0] == 0):
      top_row[last_star_ind[1]] = current_card
    else:
      bottom_row[last_star_ind[1]] = current_card

    # if the score is reasonable and the highest unmatch card is less than 6, we are safe to go to end game
    # else, we know there is at least one unmatch card bigger than 5, or the score is too high (bunch of small numbers scattered everywhere)
    # ## originnl: ((score_if_flip_last >= 5 or h_unmatched_card >= 5) and draws_left > 1):
    # ######## (POST SUBMISSION CHANGE) big improvment?? original (v2): (score_if_flip_last >= 2 or h_unmatched_card >= 3) and draws_left > 0
    if (draws_left > 0):
      # there is a matching and it's the best choice, then go for it even if it's the last star
      if (biggest_profit_ind == matching_index or biggest_profit_ind != last_star_ind):
        return ('r', biggest_profit_ind[0], biggest_profit_ind[1])
      # If the best choice is to reaplace/flip the last card, don't do that yet, replace the highest unmatched card instead, at least until draws are low
      # but don't replace the highest unmatched card if current_card - h_unmatched_card < 6
      # ######## (POST SUBMISSION CHANGE) big improvment?? original if (biggest_profit_ind == last_star_ind and current_card - h_unmatched_card < 6): 
      if (biggest_profit_ind == last_star_ind):      
        return ('r', h_unmatched_ind[0], h_unmatched_ind[1])
      # for draws = 1, cases are covered below
        

  # now we have everything we need to make a decision to replace or flip over
  # if draws_left >= 3, matching takes priority, else, biggest profit takes priority
  if (draws_left >= 3):
    # matching exist
    # match if matching profit is greater than 2 OR biggest non matching profit is 7 or less compare to matching profit
    # and (matching_profit > 2 or (biggest_profit - matching_profit < 6))
    if (matching_index[0] != -1 and (matching_profit > 2 or (biggest_profit - matching_profit < 6))):
      # unless the matching profit is really small, we replace the matching
        return ('r', matching_index[0], matching_index[1])
    # ## current_card <= 3 or 4 is the sweet spot big imporvement compare to 5 or 6!!!
    # ## num_of_matches[current_card] != 0 also make a big imporvment!!! (add cur number in board if that pair already exist)
    elif (current_card <= 0 or num_of_matches[current_card] != 0):
        '''''
        # cancel the below code resulted in big imporvment!!! 
      if (h_unmatched_card > 6):
        return ('r', biggest_profit_ind[0], biggest_profit_ind[1])
      else:
        '''''
        if (star_column[0] != -1):
            return ('r', star_column[0], star_column[1])
        else:
            return ('r', last_star_ind[0], last_star_ind[1])
    else:
      # currrent card is bigger than 3 and we don't want it, so flip over a card instead
        if (star_column[0] != -1):
            return ('t', star_column[0], star_column[1])
        else:
            return ('t', last_star_ind[0], last_star_ind[1])
  else:
    # draws_left < 3, take the biggest profit
    # sometimes matching profit is the same as biggest_profit, in that case, choose the matching profit instead
    if ((current_card <= 4 or biggest_profit > 0) and matching_profit < biggest_profit):
        return ('r', biggest_profit_ind[0], biggest_profit_ind[1])
    elif (matching_index[0] != -1):
        return ('r', matching_index[0], matching_index[1])
    else:
        if (star_column[0] != -1):
            return ('t', star_column[0], star_column[1])
        else:
            return ('t', last_star_ind[0], last_star_ind[1])

  
# need the cur_column bc for matching purposes 
def profit(num_of_matches, cur_column, row_num, current_card):
  # treat unknown number as the expected value which is roughly 5.59
  # NOTE: 6 MAKES IT MORE LIKELY TO REPLACE THE STAR, CHANGE TO 5 IT WILL BE LESS LIKELY
  
  if (cur_column[1] == '*'):
    cur_column[1] = 5.59
  if (cur_column[0] == '*'):
    cur_column[0] = 5.59
  
  result = 0
  # index for num_of_matches, -5 is at index 13
  ind = current_card
  if (current_card == -5):
    ind = 13

  # we want to compare num in the 1st row if replacement is the 0th rwo, and vise versa. 1 - row_num swtich from 0 to 1 and 1 to 0 which is what we want
  if (current_card == cur_column[1 - row_num]):
    # found a replacement to form a pair! Now calculate the bonus for matching
    if (num_of_matches[ind] == 0):
      result = cur_column[0] + cur_column[1]
    elif (num_of_matches[ind] == 1):
      result = cur_column[0] + cur_column[1] + (5 * 2)
    else:
      result = cur_column[0] + cur_column[1] + 5
    
    if (current_card == -5):
      # bonus for the -5 matching
      result = result + 10
  else: 
    result = cur_column[row_num] - current_card
    
  return result
