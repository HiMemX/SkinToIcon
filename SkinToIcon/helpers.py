def floatrange(start, stop, step):
    return [i/10000 for i in range(start*10000, stop*10000, round(step*10000))]

def average_element(matrix):
    avrgs = [0, 0, 0, 0]
    for array in matrix:
        for element in array:
            for index in range(len(element)):
                avrgs[index] += element[index]/(len(array)*len(matrix))
    return avrgs

def get_matrix_section(matrix, x, y, xsize, ysize):
    return [array[x:xsize+x] for array in matrix[y:ysize+y]]

def clamp(num, minim, maxim):
    if num < minim: num = minim
    elif num > maxim: num = maxim
    return num

def listmul(vec, factor):
    return [element*factor for element in vec]

def listadd(vec1, vec2):
    return [vec1[index] + vec2[index] for index in range(len(vec1))]