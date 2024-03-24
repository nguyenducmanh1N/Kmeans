
import pygame
from random import randint 
import math 



pygame.init()

screem = pygame.display.set_mode((1200,700))

pygame.display.set_caption("kmeans visualization")

running = True 

clock = pygame.time.Clock()

BACKGROUND = (214,214,214)
BLACK = (0,0,0)
BACKGROUND_PANEL =(249,255,230)
WHILE = (255,255,255)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (147,153,35)
purple = (255,0,255)
sky = (0,255,255)
orange = (100,25,125)
grape =(100,25,125)
grass = (55,155,65)


colors = [red,green,blue,yellow,purple,sky,orange,grass,grape] 

font = pygame.font.SysFont('sans',40)
font_small = pygame.font.SysFont('sans',20)

text_plus = font.render('+', True, WHILE)
text_minus = font.render('-',True,WHILE)
text_run = font.render('Run',True,WHILE)
text_random = font.render('Random',True,WHILE)
text_algorithm = font.render('algorithm',True,WHILE)
text_reset = font.render('Reset',True,WHILE)

# value 

k = 0 
error = 0
points = [] # danh sach diem 
clusters = [] # cum ngau nhien 
labels = [] #xd mau cua tung diem 


def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+ (p1[1]-p2[1])*(p1[1]-p2[1]))

while running:

    clock.tick(60)
    screem.fill(BACKGROUND)
    mouse_x,mouse_y = pygame.mouse.get_pos()
    #draw interface


    #draw panel

    pygame.draw.rect(screem,BLACK,(50,50,700,500))
    pygame.draw.rect(screem,BACKGROUND_PANEL,(55,55,690,490))
    #k button +
    pygame.draw.rect(screem,BLACK,(850,50,50,50))
    screem.blit(text_plus,(860,50,))

    #k button - 
    pygame.draw.rect(screem,BLACK,(950,50,50,50))
    screem.blit(text_minus,(970,50,))

    
    # button RUN
    pygame.draw.rect(screem,BLACK,(850,150,150,50))
    screem.blit(text_run,(890,150,))

    # button RANDOM
    pygame.draw.rect(screem,BLACK,(850,250,150,50))
    screem.blit(text_random,(870,250,))

    # button Algorithm
    pygame.draw.rect(screem,BLACK,(850,450,150,50))
    screem.blit(text_algorithm,(860,450,))

    # button reset
    pygame.draw.rect(screem,BLACK,(850,550,150,50))
    screem.blit(text_reset,(870,550,))

    # value
    text_k = font.render("K =" + str(k),True,BLACK)
    screem.blit(text_k,(1050,50))

    # error text 
    # text_error = font.render("Error = " + str((error)),True,BLACK)
    # screem.blit(text_error,(850,350))

    # draw mouse position when mouse is in panel 
    if 50 < mouse_x < 750 and 50 < mouse_y < 550:
        text_mouse = font_small.render("(" + str(mouse_x - 50) + "," + str(mouse_y - 50) + ")", True,BLACK)
        screem.blit(text_mouse,(mouse_x + 10,mouse_y)) 
    #end draw interface
    mouse_x,mouse_y = pygame.mouse.get_pos()

    # mouse botton down 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:



            # create point on panel 
            if 50 < mouse_x < 750 and 50 < mouse_y <550:
                labels = []
                point = [mouse_x - 50,mouse_y - 50]
                points.append(point)
                print(points)
                print("press in panel ")


            #change K button +
            if 850 < mouse_x < 900 and 50 < mouse_y <100:
                if k < 9: 
                  k = k+1 
                  print("press K +")

            #change K button -
            if 950 < mouse_x < 1000 and 50 < mouse_y <100:
                if k >0:
                   k = k - 1
                print("press K -")

            #run botton 
            if 850 < mouse_x < 1000 and 150 < mouse_y <200:
                labels = []
                # assign points to closet clusters / gan cac diem vao cluster gan nhat 
                if clusters == []:
                    continue 

                for p in points:
                    distances_to_cluster = []

                    for c in clusters :
                        dis = distance(p,c)
                        distances_to_cluster.append(dis)
                        # tinh dc toan bo khoang cach

                    # tim kc nho nhat 
                    min_distances = min(distances_to_cluster)
                    label = distances_to_cluster.index(min_distances)
                    #index tra ve vi tri co gia tri nho nhat 
                    labels.append(label) #labels of n

                # update clusters\
                for i in range(k):
                    sum_x = 0
                    sum_y = 0
                    count = 0
                    for j in range(len(points)):
                        if labels[j] == i:
                            sum_x += points[j][0]
                            sum_y += points[j][1]
                            count += 1

                    if count  != 0:  
                        new_cluster_x = sum_x/count 
                        new_cluster_y = sum_y/count 
                        clusters[i] = [new_cluster_x,new_cluster_y ]


                print("press RUN")

            #random botton 
            if 850 < mouse_x < 1000 and 250 < mouse_y <300:
                labels = []
                clusters = []

                for i in range(k):
                    random_point = [randint(0,700),randint(0,500)]
                    clusters.append(random_point)

                print("press Random")

            #reset botton 
            if 850 < mouse_x < 1000 and 550 < mouse_y <600:
                print("press Reset")
                points = []
                labels = []
                error = []
                clusters = []

            # algorithm botton
            # if 850 < mouse_x < 1000 and 450 < mouse_y <500:
            #     print("press algorithm ")



    #draw cluster
    for i in range(len(clusters)):
        pygame.draw.circle(screem,colors[i],(clusters[i][0]+50,clusters[i][1]+50),10)[i]

    #draw points
    for i in range(len(points)):
        pygame.draw.circle(screem,BLACK,(points[i][0] + 50,points[i][1] + 50),5)

        if labels ==[]:
           pygame.draw.circle(screem,WHILE,(points[i][0] + 50,points[i][1] + 50),4)
        else :
            pygame.draw.circle(screem,colors[labels[i]],(points[i][0] + 50,points[i][1] + 50),4)


    # calculate and draw error/ tinh loi khi da co labels va clusters
    error = 0
    if clusters != [] and labels != []:
        for i in range(len(points)):
            error += distance(points[i],clusters[labels[i]])

    text_error = font.render("Error = " + str(int(error)),True,BLACK)
    screem.blit(text_error,(850,350))

    pygame.display.flip()
pygame.quit()
