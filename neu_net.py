import copy
import numpy
import math
from PIL import Image, ImageDraw

PIX_AMOUNT = 255

def major_operation():
    name = input("name of pic to recognize: ")
    pic_sequence = ["actual_image/img_darvin.png", "actual_image/img_kitty.png", "actual_image/img_doggy.png"]
    N = img_pack([f"damaged_images/{name}.png"])
    P = img_pack(pic_sequence)
    W = sum_up_heaviness(P)
    steps_number = 0
    cont = True
    while(cont):
        steps_number = steps_number + 1
        if steps_number >= 120:
            print("anable to recover pic")
            break
        
        N = value_function(W, N)
        N_new = transformation_one(N)
        if is_identical(N_new, P) is cont:
            print("improved pic: image_result/img.png")
            draw_image(f"image_result/img.png", N[0])
            cont = False


def transformation_one(N):
    s = len(N[0])
    N_new = copy.deepcopy(N)
    for i in range(s):
        if N[0][i][0] < 0:
            N_new[0][i][0] = -1
        else:
            N_new[0][i][0] = 1
    return N_new


def is_identical(N, P):
    p = 0
    size_P = len(P)
    for value_num in range(size_P):
        p = 0
        size_N = len(N[0])
        for column in range(size_N):
            if N[0][column][0] == P[value_num][column][0]:
                p =  p + 1 
        if p == size_N:
            return True

    return False

    
def draw_image(path, N):
    width = 32
    picture = Image.new('1', (width, width), "white")
    draw_pic = ImageDraw.Draw(picture)
    p = 0
    for string in range(width):
        for column in range(width):
            if N[p][0] > 0:
                color = 1
            else:
                color = 0
            p = p + 1
            draw_pic.point((string, column), color)
    picture.save(path)


def value_function(W, N):
    N = (W @ N[0])
    l_y = len(N)
    l_y_i = len(N[i])
    for i in range(l_y):
        for j in range(l_y_i):
            x = N[i][j]
            first_expression = math.exp(2*x -1)
            second_expression = math.exp(2*x + 1)
            value = (first_expression / second_expression )
            N[i][j] = value
    final_Y = [N]
    return final_Y



def sum_up_heaviness(P):
    l_x = len(P)
    W = numpy.zeros((64, 64))
    for i in range(l_x):
        condition_first = W @ P[i] - P[i]
        condition_second = (W @ P[i] - P[i]).T
        ups = condition_first @ condition_second
        W = W + (ups / (P[i].T @ P[i] - P[i].T @ W @ P[i]))
    return W


def img_pack(pic_sequence):
    width = 32
    w_1 = pow(width, 2)
    pic_amount = len(pic_sequence) 
    P = list()
    for a in range(pic_amount):
        x = numpy.zeros((w_1, 1))
        img = Image.open(pic_sequence[a])
        pic_element = img.load()
        p = 0
        for string in range(width):
            for column in range(width):
                if pic_element[string, column][0] == PIX_AMOUNT:
                    required_pixel = 1
                else:
                    required_pixel = required_pixel - 1
                x[p] = required_pixel
                p = p + 1
        P.append(x)

    return P

