
import copy
def Square(conditionCount):
  # first line
  firstLine = [0, 1]
  useBack = True
  choices = range(2, conditionCount)
  for i in range(2, conditionCount):
    if useBack:
      number = choices.pop()
    else:
      number = choices.pop(0)
    firstLine.append(number)
    useBack = not useBack
    
  # Latin square
  square = [firstLine]
  for i in range (1, conditionCount):
    line = [(element + i) % conditionCount for element in firstLine]
    square.append(line)
  
  # add reversed lines Latin square for odd-numbered condition
  if (conditionCount % 2 != 0):
   reversedSquare = []
   for line in square:
     reversedLine = copy.copy(line)
     reversedLine.reverse()
     reversedSquare.append(reversedLine)
   square.extend(reversedSquare)
   
  return square


if __name__=="__main__":
    s = Square(5)
    print s