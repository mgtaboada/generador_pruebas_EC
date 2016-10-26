from random import randint
class MFiltro:
    def __init__(self, k, matriz):
        self.k = k
        self.matriz = matriz
    def id(self):
        return MFiltro(1, [[1 for i in range(3)] for j in range(3)])

class Imagen:
    def __init__(self, m, n, matriz):
        self.m = m
        self.n = n
        self.matriz=matriz

def comp(img1, img2):
    res = 0
    for i in range(len(img1.matriz)):
        for j in range(len(img1.matriz[i])):
            res += abs(img1.matriz[i][j] - img2.matriz[i][j])
    return res

def vPixel(submatriz, mfiltro):
    acc = 0
    for i in range(3):
        for j in range(3):
            acc += submatriz[i][j] * mfiltro.matriz[i][j]
    acc = int(acc/mfiltro.k)
    if acc > 255:
        return 255
    if acc < 0:
        return 0
    return acc

def subMatriz(img, i, j):
    subimg = [[0 for i in range(3)] for j in range(3)]
    if i==0 or i == img.m-1 or j == 0 or j == img.n-1:
        subimg = [[img.matriz[i][j] for k in range(3)] for l in range(3)]
    else:
        for k in [k-1 for k in range(3)]:
            for l in [l-1 for l in range(3)]:
                subimg[k+1][l+1] = img.matriz[k][l]
    return subimg
def filPixel(img, i, j, mfiltro):
    return vPixel(subMatriz(img, i, j), mfiltro)
def filtro(img, mfiltro):
    imfiltrada = [[0 for i in range(img.n)] for j in range(img.m)]
    for i in range(img.m):
        for j in range(img.n):
            imfiltrada[i][j] = filPixel(img, i, j, mfiltro)
    return Imagen(img.m, img.n,imfiltrada)
def filtRec(img, mfiltro, nCambios, nFiltrados):
   # print("nFiltrados: "+ str(nFiltrados))
    #print("actual: ")
   # en_memoria_imagen(img)
    if nFiltrados >= 10:
        print("nFiltrados: " + nFiltrados)
        return img
    aux = filtro(img, mfiltro)
    #print("cambiada: ")
   # en_memoria_imagen(aux)
    nuevoCambios = comp(aux, img)
    if nuevoCambios < nCambios:
        print("nFiltrados: " + str(nFiltrados))
        return img
    return filtRec(aux, mfiltro, nCambios, nFiltrados + 1)
def to_little_endian(num):
    res = ""
    num2=num[2:]
    if len(num2) %2 == 1:
        num2 = '0'+num2

    i = 0
    while i < len(num2):
        res = num2[i:i+2] + res
        i += 2
    res = res + (8-len(res))*'0'
    return res

def to_big_endian(num):
    res = ""
    num2=num[2:]
    if len(num2) %2 == 1:
        num2 = '0'+num2

    i = 0
    while i < len(num2):
        res = res+num2[i:i+2]
        i += 2
    res =  (8-len(res))*'0' + res
    return res

def imagen_aleatoria():
    m = randint(1,30)
    n = randint(1, 30)
    return Imagen(m, n, [[randint(0,50) for i in range(n)] for j in range(m)])
def filtro_aleatorio():
    k = randint(1,15)
    return MFiltro(k, [[randint(0,10) for i in range(3)] for j in range(3)])
def en_datos_filtro(mfiltro):
    m = ""
    for i in mfiltro.matriz:
        for j in i:
            m = m + '0x'+to_big_endian(hex(j)) + ', '

    return "data 0x"+ to_big_endian(hex(mfiltro.k))+', ' + m[:-2]
def en_memoria_imagen(imagen):
    m = "0x"
    total = ""
    con = 0
    columnas = 0
    for i in range(len(imagen.matriz)):
        for j in range(len(imagen.matriz[i])):
            if con == 4:
                total = total + ' '+to_little_endian(m)
                m = "0x"
                con = 0
                columnas +=1

            m = m +(2-(len(hex(imagen.matriz[i][j]))-2))*'0' + hex(imagen.matriz[i][j])[2:]
            con +=1


            if columnas == 4:
                total = total + "\n"
                columnas = 0

    if con != 0:
        total = total + ' '+to_little_endian(m)

    return '0x'+to_little_endian(hex(imagen.m))+ " 0x"+ to_little_endian(hex(imagen.n))+ "\n"+ total
def en_datos_imagen(imagen):
    m = "ox"
    total = ""
    con = 0
    for i in imagen.matriz:
        for j in i:
            if con < 4:
                j = int(j)
                m = m + (2-(len(hex(j))-2))*'0' +hex(j)[2:]
                con +=1
            else:
                total =total+ ", 0x"+ to_big_endian(m)
                m = "ox"
                con = 0


    if ((imagen.n * imagen.m) % 8) != 0:
        total = total+ " "+ to_big_endian(m)

    return "data 0x"+to_big_endian(hex(imagen.m))+ ", 0x"+ to_big_endian(hex(imagen.n))+ total
def en_datos_matriz(m):
    return en_datos_imagen(Imagen(len(m), len(m[0]), m))
def en_memoria_matriz(m):
    return en_memoria_imagen(Imagen(len(m), len(m[0]), m))
def datos_y_solucion_comp():
    while True:
        im1 = imagen_aleatoria()
        im2 = Imagen(im1.m, im1.n, [[randint(0,255) for i in range(im1.n)] for j in range(im1.m)])
        print("IMG1: "+ en_datos_imagen(im1))
        print("IMG2: "+ en_datos_imagen(im2))
        print("Valor esperado para la comparación: "+ str(comp(im1, im2)))
        input("Pulsar Enter para obtener otro juego de valores...")

def datos_y_solucion_valorPixel():
    while True:
        im = imagen_aleatoria()
        subimg = subMatriz(im, randint(0, im.m-1), randint(0, im.n-1))
        mf = filtro_aleatorio()
        print("SUBIMG: " + en_datos_matriz(subimg))
        print("MFIL: "+ en_datos_filtro(mf))
        print("Valor esperado para valorPixel: " + str(vPixel(subimg, mf)))
        input("Pulsar Enter para obtener otro juego de valores...")
def datos_y_solucion_subMatriz():
    while True:
        im = imagen_aleatoria()
        i = randint(0, im.m-1)
        j = randint(0, im.n-1)
        print("IMG: "+ en_datos_imagen(im))
        print("i: "+ str(i))
        print("j: "+ str(j))
        print("Valor esperado para subMatriz: "+ en_memoria_matriz(subMatriz(im, i, j)))

        input("Pulsar Enter para obtener otro juego de valores...")
def datos_y_solucion_filPixel():
    while True:
        im = imagen_aleatoria()
        mf = filtro_aleatorio()
        i = randint(0, im.m-1)
        j = randint(0, im.n-1)
        print("IMG: "+ en_datos_imagen(im))
        print("MFIL: "+ en_datos_filtro(mf))
        print("i: "+ str(i))
        print("j: "+ str(j))
        print("Valor esperado para filPixel: "+ filPixel(im, i, j, mf))
        input("Pulsar Enter para obtener otro juego de valores...")
def datos_y_solucion_filtro():
    while True:
        im = imagen_aleatoria()
        mf = filtro_aleatorio()
        print("IMG: "+ en_datos_imagen(im))
        print("MFIL: "+ en_datos_filtro(mf))
        print("Valor esperado para el filtro: ")
        print(en_memoria_imagen(filtro(im, mf)))
        input("Pulsar Enter para obtener otro juego de valores...")
def datos_y_solucion_filtrec():
    while True:
        print("\n\n\n\n\n\n\n\n")
        im = imagen_aleatoria()
        mf = filtro_aleatorio()
        nCambios = randint(300,10200)
        print("IMG: " + en_datos_imagen(im))
        print("MFIL: " + en_datos_filtro(mf))
        print("nCambios: "+ str(nCambios))
        print("\n\n\n\n")
        print("Valor esperado para la imagen tras filtrec:")
        print(en_memoria_imagen(filtRec(im,mf, nCambios, 0)))
        input("Pulsar Enter para obtener otro juego de valores...")
def main():
    print("""Generar pruebas para:
    1. Comp
    2. ValorPixel
    3. SubMatriz
    4. FilPixel
    5. Filtro
    6. FiltRec    """)
    opcion = int(input("Introducir un número\n>>> "))
    dop = {1:datos_y_solucion_comp, 2: datos_y_solucion_valorPixel, 3: datos_y_solucion_subMatriz,4:datos_y_solucion_filPixel,5:datos_y_solucion_filtro,6:datos_y_solucion_filtrec}
    dop[opcion]()
main()
