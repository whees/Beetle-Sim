# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 19:04:29 2022

@author: lcuev
"""
import pygame
import numpy as np
import matplotlib.pyplot as plt



empty = 0
stem = 1
flower = 2
beetle = 3



plant_scale = 15
scale= 10

dimx = 100
dimy = 100

tmax = 5
ftmax = 200


col_background = (10, 10, 50)
col_stem = (10,120,10)
col_flower = (248,200,200)
col_beetle = (255,95,31)

empty_to_flower = (133,100,100)
pollen_to_flower = (133,100,133)
beetle_to_empty = (100,95,31)
pollenate = (255,142,47)
stem_to_empty = (10,80,10)
stem_to_flower = (100,255,100)



def update(surface, cur, xy,timers,pollens,ftimers,kill_plant):
    if not kill_plant:
        for i in range(400):
            x,y = xy
            r = np.random.random()
            if r < 0.01:
                x, y =  0.00 * x + 0.00 * y,  0.00 * x + 0.16 * y + 0.00
            elif r < 0.85:
                x, y =  0.91 * x + 0.00 * y, -0.0 * x + 0.86 * y + 1.60
            elif r < 0.925:
                x, y =  0.20 * x - 0.26 * y,  0.1 * x + 0.1 * y + 1.60
            else:
                x, y = -0.20* x + 0.26 * y,  0.1* x + 0.1 * y + 1
        
            
            
            xy = [x,y]
            
            X = int((plant_scale*x + dimx / 2))
            Y = dimy - int((plant_scale*y)) 
            
         
            
            if X in range(dimx) and Y in range(dimy):
                if cur[X][Y] != flower:
                    cur[X][Y] = stem
            
            
    
    for X in range(dimx):
        for Y in range(dimy):
            n_stem = 0
            n_flower = 0
            n_beetle = 0
            
            col = (0,0,0)
            
     
            for r_ in range(X-1,X+2):
                for c_ in range(Y-1,Y+2):
                    if r_ > -1 and r_ < dimx and c_ > -1 and c_ < dimy:
                        if cur[r_][c_] == stem:
                            n_stem += 1
                        elif cur[r_][c_] == flower:
                            n_flower += 1
                        elif cur[r_][c_] == beetle:
                            n_beetle += 1
                            
                            
            if cur[X][Y] == empty:        
                di = np.random.random()
                if di < 0.001 and not pollens[X][Y] and n_stem ==3:
                    cur[X][Y] = flower
                    col = empty_to_flower
                elif di < 0.01 and pollens[X][Y] and n_stem > 0:
                    cur[X][Y] = flower
                    col = empty_to_flower
                    pollens[X][Y] = False
                elif (n_beetle > 0 and not kill_plant and n_stem > 2) or (n_beetle > 0 and kill_plant and n_stem > 0 ) :
                    cur[X][Y] = beetle
                    col = beetle_to_empty 
            elif cur[X][Y] == beetle:
                timers[X][Y] += 1
                
                if n_beetle > 3 or timers[X][Y] == tmax:
                    cur[X][Y] = empty
                    timers[X][Y] = 0
                    col = beetle_to_empty
                if n_stem > 0 or n_flower > 0:
                    timers[X][Y] = 0
                if n_flower > 0:
                    pollens[X][Y] = True
                    col = pollenate
                    
                
            elif cur[X][Y] == stem:
                if n_beetle > 0:
                    if not pollens[X][Y]:
                        cur[X][Y] = empty
                        col = stem_to_empty
                    else:
                        di = np.random.random()
                        if di < 0.01 and n_flower > 0:
                            cur[X][Y] = flower
                            col = stem_to_flower
                            pollens[X][Y] = False
                        else:
                            cur[X][Y] = empty
                            col = stem_to_empty
              
                        
            
            elif cur[X][Y] == flower:
                ftimers[X][Y] += 1
                if ftimers[X][Y] == ftmax:
                    cur[X][Y] = empty
                    ftimers[X][Y] = 0
                    col = empty_to_flower
            
            
            
            if col == (0,0,0):
                if cur[X][Y] == 0:
                    col = col_background
                elif cur[X][Y] == 1:
                    col = col_stem
                elif cur[X][Y] == 2:
                    col = col_flower
                elif cur[X][Y] == 3:
                    col = col_beetle
                    
            
                
                
                
            
                
                    

            pygame.draw.rect(surface, col, ( scale * X,  scale * Y, scale, scale))

        
  

    
    return cur,xy,timers,pollens,ftimers

def init(dimx, dimy):
    cells = [[0 for i in range(dimx)] for j in range(dimy)]
    return cells


def main(cellsize):
    pygame.init()
    surface = pygame.display.set_mode((scale * dimx, scale * dimy))
    pygame.display.set_caption("John Conway's Game of Life")

    cells = init(dimx,dimy)
    timers = [[0 for i in range(dimx)] for j in range(dimy)]
    ftimers = [[0 for i in range(dimx)] for j in range(dimy)]
    pollens = [[False for i in range(dimx)] for j in range(dimy)]
    running = True
    eat = False
    penup = True
    xy = [0,0]
    penup = True
    kill_beetle = False
    kill_plant = False
    

    
    beetle_totals = []
    stem_totals = []
    flower_totals = []
    times = []
    time = -1

    while running:
        
        time += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                plt.plot(times,flower_totals,'pink')
                plt.plot(times,stem_totals,'green')
                plt.plot(times,beetle_totals,'orange')
                plt.show()
                return
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    eat = not eat
                if event.key == pygame.K_b:
                    kill_beetle = True
                if event.key == pygame.K_p:
                     kill_plant = not kill_plant
            elif event.type == pygame.MOUSEBUTTONDOWN:
               penup = False
            elif event.type == pygame.MOUSEBUTTONUP:
                penup = True
                
        if not penup:
            x,y = pygame.mouse.get_pos() 
            X,Y = int(x/scale), int(y/scale)
            if X in range(dimx) and Y in range(dimy):
                cells[X][Y] = beetle
                    
            

        surface.fill(col_background)
        cells,xy,timers,pollens,ftimers = update(surface, cells, xy,timers,pollens,ftimers,kill_plant)
        pygame.display.update()
        
        n_flower = 0
        n_stem = 0
        n_beetle = 0
        
        for X in range(dimx):
            for Y in range(dimy):
                if cells[X][Y] == 1:
                    n_stem += 1
                elif cells[X][Y] == 2:
                    n_flower += 1
                elif cells[X][Y] == 3:
                    n_beetle += 1
        
        beetle_totals += [n_beetle]
        flower_totals += [n_flower]
        stem_totals += [n_stem]
        times += [time]
        
        if kill_beetle:
            for X in range(dimx):
                for Y in range(dimy):
                    if cells[X][Y] == beetle:
                        timers[X][Y] = tmax - 1
            kill_beetle = False
        

    

                
       
    return

if __name__ == "__main__":
    main(8)
    





