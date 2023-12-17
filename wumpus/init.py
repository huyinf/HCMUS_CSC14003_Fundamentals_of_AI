# # notion
# '''
# W - Wumpus
# S - Stench
# P - Pit
# B - Breeze
# A - Agent
# - - Empty/Save
# '''
# # input/output
# '''
# input.txt

# N       --> map N x N
# N lines --> map info

# output.txt

# path + points 
# '''
# # initialization
# '''
# read input.txt --> build map M[] (2d)

# count gold --> nG
# count wumpus --> nW

# score = 0
# path = [] (1d)

# knowledge --> K[] (2d)
# Inference --> I[] (2d)

# add direction and roration for each step

# model of First Order Logic (FOL)
# '''
# # algorithm
# '''


# while True:

#     # win game
#     if nG == 0 and nW == 0:
#         print('win')
#         return score,path
        
#     # caught by wumpus or fall in pit
#     if M[x,y] == 'W' or M[x,y] == 'P':
#         print('die')
#         return score,path
        
#     # if M[x,y] == 'B':
#         update I[x,y] = 'B'
#         get gold if possible
    
# '''


'''

# (prev,curr) --> sol
cases = {
        
        ('PW','P'):'P',
        ('PW','W'):'W',
        ('P','PW'):'P',
        ('W','PW'):'W',
        
        ('S','E'):'E',
        ('B','E'):'E',
        ('W','E'):'E',
        ('P','E'):'E',
        
        ('P','W'):'E',
        ('W','P'):'E',
        
        ('B','S'):'BS',
        ('S','B'):'BS',
        ('B','BS'):'BS',
        ('S','BS'):'BS',
        
        ('P','S'):'S',
        ('W','B'):'B',
        
        
         
        }

'''

l = [(1,2),(2,2)]
l.append((1,1))
print(type(l))