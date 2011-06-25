import ants, time, pygame, random


def setup():                            #Setup all our lists and establish two ant colonies (RED vs BLU)
        global colonies, trails, foods, text, debug, showtrail
        colonies = []
        trails = []
        foods = []
        text = []
        colonies.append(ants.Colony([0,0,150],10, 150, 150, WIDTH, HEIGHT, 300))
        colonies.append(ants.Colony([150,0,0],10, 650, 650, WIDTH, HEIGHT, 300))
        debug=0
        showtrail=0

def doinput():                          #Check for input ESC for exit d for debug mode.
        global debug, showtrail
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                        keys[event.key] = True
                elif event.type == pygame.KEYUP:
                        keys[event.key] = False
                if keys[pygame.K_ESCAPE]:
                        exit(0)
                if keys[pygame.K_d]:
                        debug+=1
                if (debug>1): debug=0
                if keys[pygame.K_t]:
                        showtrail+=1
                if (showtrail>1): showtrail=0
                        
def update():                           #Update all our ants, trails, and foods.
        global colonies, trails, foods, text, debug, showtrail
        
        MainSurf.fill([157,107,64])     #blank our background with a pleasant brown.

        if len(trails) > 0:
                for pheromone in trails:                #If there are any trails we need to degrade them over time
                        pheromone.update()
                        if (showtrail==1):
                                pheromone.draw(MainSurf)
                        if pheromone.strength < 0.05:   #Trails that grow weak should be removed.
                                trails.remove(pheromone)

        
        for f in foods:                 #Update and draw our food blobs.
                f.draw(MainSurf)
                if (f.size <2): foods.remove(f)
                
        if (len(foods) < 1):    #Place new ones if the current ones are mined out.
                for i in range(2):
                        x = 100 + random.random()*(WIDTH-100)
                        y = 100 + random.random()*(HEIGHT-100)
                        s = (random.random()*20)+20
                        foods.append(ants.Food(x,y,s)) 
        
        text=[]                         #text method only used for debug mode at this point.

        for colony in colonies:         #for each colony we need to go through and update and draw the ants.
                colony.draw(MainSurf)
                text.append(ants.Text([150,150,150], 10, (colony.x-5, colony.y+30), str(len(colony))))
                for ant in colony:
                        ant.update(trails,foods,colonies)
                        ant.draw(MainSurf)
                
                        if debug==1:    #if debug mode is on draw our ants heading and position.
                                text.append(ants.Text([150,150,150], 10, (ant.x, ant.y), str((int(ant.step),int(ant.r)))))
                
        
        for t in text:                  #draw any text we have.
                t.draw(MainSurf)
            
        pygame.display.update()         #draw our new frame.


if __name__ == "__main__":

        
        pygame.init()                   #initialize pygame
        clock = pygame.time.Clock()     #start our FPS clock

        #global constants here
        WIDTH=800
        HEIGHT=800
        MainSurf = pygame.display.set_mode([WIDTH, HEIGHT])

        keys = {pygame.K_ESCAPE : False, pygame.K_d : False, pygame.K_t : False} #Declare keys we will use
        
        setup()                                 #run our init function
        
        while 1:                                #main loop
                clock.tick(500)                  #Limit FPS to 30
                doinput()                       #Do input functions
                update()                        #Do main update routene

        exit(0)
