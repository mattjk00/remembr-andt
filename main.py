import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def array_as_color(a):
    color = a[3]
    color += a[2] << 8
    color += a[1] << 16
    color += a[0] << 24
    return color

def color_as_array(c):
    arr = np.zeros(4, dtype=np.uint8)
    arr[3] = c & 0x000000FF
    arr[2] = (c & 0x0000FF00) >> 8
    arr[1] = (c & 0x00FF0000) >> 16
    arr[0] = (c & 0xFF000000) >> 24
    return arr

width = 0
height = 0
target = 0
palette = 0
population = 0
pop_size = 10

def random_img(w, h):
    img = np.zeros((w, h, 4), dtype=np.uint8)

    for i in range(len(img)):
        car = color_as_array(palette[np.random.randint(0, len(palette))])
        for j in range(len(img[i])):
            
            img[i][j] = car
    
    return img

def fitness_score(img):
    score = 0
    for i in range(len(img)):
        for j in range(len(img[i])):
            icolor = array_as_color(img[i][j])
            tcolor = array_as_color(target[i][j])
            tscore = abs(icolor - tcolor)
            score += tscore
            
    return score # lower better

def pick_best_two():
    best = [0, 1]
    fsbest = fitness_score(population[0])
    fsbest2 = fitness_score(population[1])

    for i in range(len(population)):
        fs = fitness_score(population[i])
        if fs < fsbest:
            fsbest2 = fsbest
            best[1] = best[0]
            best[0] = i
            fsbest = fs
        elif fs < fsbest2:
            fsbest2 = fs
            best[1] = i
    
    return best

def collage(img1, img2, cpointx, cpointy):
    img3 = np.copy(img1)
    for i in range(cpointy, len(img2)):
        for j in range(cpointx, len(img2[i])):
            img3[i][j] = img2[i][j]
    return img3

'''
Right now just picks best two and creates children of the two spliced.
'''
def evolution_routine():
    best = pick_best_two()

    best_img = population[best[0]]
    best_img2 = population[best[1]]

    child1 = collage(best_img, best_img2, 0, height//2)
    child2 = collage(best_img2, best_img, 0, height//2)

    population.clear()
    population.extend([best_img, best_img2, child1, child2])

    for i in range(pop_size - 4, pop_size):
        childn = np.copy(child2)
        if i % 2 == 0:
            childn = np.copy(child1)
        
        for x in range(width//10):
            rx = np.random.randint(0, width)
            ry = np.random.randint(0, height)
            ccolor = childn[ry][rx]
            childn[ry][rx] = color_as_array(palette[np.random.randint(0, len(palette))])
        
        population.append(childn)
    
    return best



def main():
    global width, height, target, palette, population
    target_img = Image.open('./img/dog3.png')
    
    target = np.asarray(target_img)
    width = len(target)
    height = len(target[0])
    
    palette = []

    for i in range(0, len(target)):
        for j in range(0, len(target[i])):
            color = array_as_color(target[i][j])
            palette.append(np.uint32(color))
    palette = list(set(palette))
    
    print(len(palette))

    population = []
    
    for i in range(pop_size):
        img = random_img(width, height)
        
        population.append(img)
    
    best = 0
    for n in range(500):
        best2 = evolution_routine()
        #print(best2)
        if best2[0] < len(population):
            best = population[best2[0]]
    

    save_img = Image.fromarray(best)
    save_img.save('./img/out/dogBEST.png')

if __name__ == '__main__':
    main()