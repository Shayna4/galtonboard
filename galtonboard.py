import Draw
import random
#"I hereby certify that this program is solely the result of my own work and is 
#in compliance with the Academic Integrity policy of the course syllabus and the 
#academic integrity policy of the CS department.”

PIN_GAP = 30 #spacing between row and col

#this function accepts the specific row # and col # for each pin as input
#it returns the x coordinates for each pin
#odd pin rows begin with a gap while even rows begin with a pin
def xCoord(row,col):
    if row % 2 == 0: 
        newX = (col*PIN_GAP) +PIN_GAP+PIN_GAP//2+3
        
    else:
        newX = (PIN_GAP//2) + (col*PIN_GAP)+PIN_GAP//2+3  
        
    return newX

#this function takes the row # as input 
#it returns the y coordinate for that specific pin by adding the PIN_GAP to the 
#previous recorded coordinate
def yCoord(row):
    return row*PIN_GAP +PIN_GAP 

#this function accepts the current x cordinate of the ball and the number of 
#rows of pins as input
#it randomly chooses if the ball should drop to the left or to the right if 
#it's not the first position for the ball
#it returns the correct new x coordinate for that specific ball
def xCirc(xBall,pinRows):
    change = random.randint(0,10) 
    
    if xBall < 1: 
        #the first x - coord should be the middle
        xBall = (pinRows*7)-5 +PIN_GAP
    
    #when it's not the first position for the ball randomly increase or 
    #decrease the x coordinate by PIN_GAP/2 
    else: 
        if change <= 4:
            xBall += PIN_GAP/2 
            
        elif change >= 5:
            xBall = xBall - PIN_GAP/2
    return xBall

#this function takes the y coordinate of the ball as input
#it returns the new y coordinate by adding PIN_GAP the initial position is 
#slightly less to keep the ball above the pin
def yCirc(yBall):
    #if it's the first position for the ball, the y should be positioned 
    #slightly higher than the pin
    if yBall == 1:
        yBall += PIN_GAP -5
    #all other jumps should have the same vertical displacement of PIN_GAP
    else:
        yBall += PIN_GAP         
    return yBall

#this function accepts the x and y coordinates for each pin and draws a pin in 
#that location
def createPin(x,y):
    Draw.picture("images copy.gif",x,y)  
    
#this function draws the board 
#this function sets the canvas color, draws the pins and the shoots through the 
#xCoord and  yCoord functions, stores the coordinates in lists, and invokes the 
#fall function to drop the ballls into the shoots
def drawBoard(b,pinRows,pinCols,balls,colorList,d,top):
    
    #set up and draw the pins using the a nested loop and the functions xCoord, 
    #yCoord, and createPin
    Draw.setColor(colorList[1]) 
    for row in range(pinRows):
        for col in range(pinCols): 
            x = xCoord(row,col) 
            y = yCoord(row) 
            createPin(x,y)
            
    #set up and draw the shoots 
    for row in range(pinRows+1):
        shoot = row*PIN_GAP+ PIN_GAP//2
        Draw.setColor(colorList[2])
        Draw.filledRect(shoot,top,5,b-top)
    
    #draw the last shoot outside of the loop to fence post
    Draw.setColor(colorList[2])
    Draw.filledRect((pinRows+1)*PIN_GAP+PIN_GAP//2,top,5,b-top)
    
    #set up and draw the bars in the shoots using the fall function
    Draw.setColor(colorList[7])
    fall(balls,pinRows,d,colorList,b) #need to fix this
    Draw.setColor(colorList[12])

#this function accepts the list of the ball's coordinates the number of rows of 
#pins, the dictionary recording how many balls are in each shoot, the list of 
#colors and the height of the board
#this function drops the balls from the bottom of the triangle into the shoots 
#through an if statement and a for loop 
def fall(balls,pinRows,shoot,colorList,height):
    
    #if the list exceeds the number of jumps the ball has on the board the 
    #dictionary is incremented acording to the shoot the ball falls into
    if len(balls)> pinRows*2: 
        if balls[-2] in shoot: shoot[balls[-2]] += 1
        else: shoot[balls[-2]]= 1 
        
    #draw a bar in the shoot whos height is incremented based on the number in 
    #that shoots index in the dictionary
    Draw.setColor(colorList[-3])
    for p in shoot:
        Draw.filledRect(p,height-shoot[p]/7,15,height)


#this function takes the number of balls and the parameters used in drawBoard to
#drop the balls 
#utilyzing the xCirc and yCirc functions, this function drops each ball down the 
#galton board changing the color of each ball to make it easier for one to 
#understand the simulation 
def ballDrops(height,pinRows,pinCols, balls,colorList,d,ballNum,top):

    #run the loop of creating the list for each induvidual ball's path 1 more 
    #times than the ballNum because the final one's landing doesn't get incremented 
    #in the shoot dictionnary
    for j in range(ballNum+1):
        
        #set a unique color for each ball  
        h = random.choice(colorList)
        Draw.setColor( h)
        
        #go through each jump/set of coordinates of the ball
        for i in range(0, len(balls)-1,2): 
            Draw.setColor(h)  
            xBall = i 
            yBall = i+1             
            
            #if it's not the first position of the ball check back at the 
            #previous position which are the previous 2 elements in the list
            #the first position doesn't reference this statement because it has 
            #a separate commant in the functions xCirc and yCirc
            if i != 0:
                xBall = balls[i-2] 
                yBall = balls[i-1]
            
            #through the functions xCirc and yCirc increment the ball's coordinates 
            xBall = xCirc(xBall,PIN_GAP) 
            yBall = yCirc(yBall)
            
            #save the balls coordinates in the list
            balls[i] = xBall
            balls[i+1] = yBall
            
            #when the balls reaches/bounces to the bottom of the pins redraw the
            #board with the ball in the correct spot the and count number incremented   
            if len(balls) >= (pinRows+1)*2:
                
                Draw.clear()
                drawBoard(height,pinRows,pinCols,balls,colorList,d,top)
                
                #draw the ball in the correct place with the correct color
                Draw.setColor( h)
                Draw.filledOval(xBall,yBall,10,10)
                Draw.show(1)
        
        #if the ball should still bounce add two 0s to the balls coordinate list 
        #so that it can hold coordinates
        if len(balls) <= pinRows*2:     
            balls.append(0)
            balls.append(0)
            
    
    Draw.clear() 


def main():   
    a = 500 #dimension
    b = 700#dimension
    Draw.setCanvasSize(a,b)
    
    #number of rows of pins
    pinRows = 14
    #number of cols in pins
    pinCols =14
    #number of balls
    ballNum = 300
    #coordinate list of balls that will drop
    #this list represents an induvidual balls entire track    
    balls = [0]*pinRows*2
    #top is the height of the shoots
    top = PIN_GAP*(pinRows+1)
    #this is the list of possible colors for balls
    colorList = [Draw.color(136,189,231),Draw.color(233,157,69),\
                 Draw.color(81,27,124),Draw.color(96,126,224),\
                 Draw.color(146,152,243),Draw.color(218,217,248),\
                 Draw.color(234,161,73), Draw.color(67,24,118),\
                 Draw.color(172,192,27),Draw.color(106,92,194),\
                 Draw.color(232,219,233),Draw.color(209,37,104),\
                 Draw.color(215,70,244),Draw.color(56,128,206),\
                 Draw.color(235,114,49),Draw.color(40,92,178),\
                 Draw.color(247,236,242),Draw.color(138,216,192),\
                 Draw.color(9,1,51),Draw.color(165,90,245),\
                 Draw.color(176,58,126),Draw.color(237,108,92),\
                 Draw.color(39,147,147),Draw.color(9,1,51),\
                 Draw.color(165,90,245),Draw.color(176,58,126),\
                 Draw.color(237,108,92),Draw.color(242,198,109), \
                 Draw.color(70,151,193),Draw.color(92,167,139),\
                 Draw.color(180,39,138),Draw.color(48,18,143)] 
    #this empty dictionary will house the heights of each of the bars in the shoots
    d = {}
    
    Draw.show()
    drawBoard(b,pinRows,pinCols,balls,colorList,d,top)
    Draw.show()
    ballDrops(b,pinRows,pinCols, balls,colorList,d,ballNum,top)
       
main()