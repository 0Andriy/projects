from typing import Counter
import cv2
import numpy as np

#! *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

# def FrametoDesctop(frame):
    
#     img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Переводимо 3 канал в 1 канал -- градації сірого

#     img_g = cv2.GaussianBlur(img_gray, (19, 19), 0) # Зглажуємо 

#     # ret, thresh = cv2.threshold(img_g, 100, 255, 0) # бінарізація
#     thresh = cv2.Canny(img_g, 50, 100) # всю менше 1 значення буде ігноруватися і ставитиметься 0(чорний), коли все більше 2 значення аналогічно першому але буде ставитися 255(білий)

#     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # знаходимо контури

#     cv2.drawContours(img_gray, contours, -1, (255, 0, 0), 3)

#     cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
#     cv2.imshow("Result", img_gray)


# #! *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-


# cap = cv2.VideoCapture("../media/VID_20210901_124602.mp4")
# video = True

# count = 0
# while cap.isOpened():
#     try:
#         # Capture frame-by-frame
#         cap.set(cv2.CAP_PROP_POS_MSEC, (count * 100))
#         ret, frame = cap.read()
#         count += 1
#         if ret == False:
#             break

#         if video == True:

#             FrametoDesctop(frame)

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
        
#         else:
#             FrametoDesctop(frame)
#             cv2.waitKey(0)

#     except Exception as e:
#         pass


# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()


#! *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

def DrawCountursToImage(image, t=1):
        # 4. Рисуем контурную функцию
    # Пользовательская функция рисования контура (для упрощения операции)
    # Введите 1: winName: имя окна
    # Вход 2: изображение: исходное изображение
    # Вход 3: контуры: контуры
    # Ввод 4: draw_on_blank: метод рисования, True рисует на белом фоне, False: рисует на исходном изображении
    def drawMyContours(winName, image, contours, draw_on_blank = True):
        # cv2.drawContours(image, contours, index, color, line_width)
            # Входные параметры:
            # изображение: изображение холста того же размера, что и исходное изображение (также может быть исходным изображением)
            # контуры: контуры (список питонов)
            # index: индекс контура (при значении -1 нарисуйте все контуры)
            # цвет: цвет линии,
            # line_width: толщина линии
            # Вернуть контурное изображение
            if (draw_on_blank): # нарисовать контур на белом фоне
                temp = np.ones(image.shape, dtype=np.uint8) * 255
                cv2.drawContours(temp, contours, -1, (0, 0, 0), 2)
            else:
                temp = image.copy()
                cv2.drawContours(temp, contours, -1, (0, 0, 255), 2)
            
            cv2.imshow(winName, temp)
            # cv2.waitKey()
    


    # Пользовательская функция: используется для удаления контура указанного порядкового номера в списке
    # Вход 1: контуры: исходные контуры
    # Ввод 2: delete_list: список номеров контуров, которые нужно удалить
    # Возвращаемое значение: контуры: отфильтрованные контуры
    def delet_contours(contours, delete_list):
        delta = 0
        for i in range(len(delete_list)):
            # print("i= ", i)
            del contours[delete_list[i] - delta]
            delta = delta + 1
        return contours



    # 1. Загрузить изображение
    # image = cv2.imread("../media/photos_with_video/frame15.jpg", 1)
    # print(image.shape)
    height, width, channel = image.shape
    image = cv2.resize(image, (int(0.5*width), int(0.5*height)), interpolation=cv2.INTER_CUBIC)
    # cv2.imshow("original", image)
    # cv2.waitKey()

    # 2. Предварительная обработка
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # print(gray.shape)
    # cv2.imshow("gray", gray)
    
    gray = cv2.GaussianBlur(gray, (3, 3), 1)
    ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow("binary", binary)
    
    element = cv2.getStructuringElement (cv2.MORPH_RECT, (3, 3)) # 3 * 3 квадрат, 8-битный тип uchar, все 1 структурные элементы
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, element)
    
    # cv2.imshow("morphology", binary)
    # cv2.waitKey()

    # 3. Найти контуры
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("find", len(contours), "contours")

    # 4. Нарисуйте оригинальный контур
    # drawMyContours("find contours", image, contours, True)

    # 5.Фильтры контуров
    # 5.1 Фильтрация контуров с использованием иерархии
    # hierarchy[i]: [Next，Previous，First_Child，Parent]
    # Не требует родительского контура
    delete_list = [] # Создать список номеров контуров для удаления
    c, row, col = hierarchy.shape
    for i in range(row):
        if hierarchy [0, i, 2]> 0: # имеет дочерний контур
            delete_list.append(i)

    # Удалить контуры, которые не соответствуют требованиям, согласно номеру списка
    # contours = delet_contours(contours, delete_list)
    
    print(len(contours), "contours left after hierarchy filter")
    # drawMyContours("contours after hierarchy filtering", image, contours, True)
    

    # 5.2 Использовать фильтрацию по длине контура
    min_size = 100
    max_size = 1000
    delete_list = []
    for i in range(len(contours)):
        if (cv2.arcLength(contours[i], True) < min_size) or (cv2.arcLength(contours[i], True) > max_size):
            delete_list.append(i)
    
    # Удалить контуры, которые не соответствуют требованиям, согласно номеру списка
    contours = delet_contours(contours, delete_list)
    
    print(len(contours), "contours left after length filter")
    # drawMyContours("contours after length filtering", image, contours, False)

    # 6. Дескриптор формы
    # 6.1 минимальный покрывающий прямоугольник
    result = image.copy()
    # for i in range(len(contours)):
    #     x, y, w, h = cv2.boundingRect (contours[i]) # (x, y) - координата левого верхнего угла прямоугольника, а (w, h) - ширина и высота прямоугольника.
    #     cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 1)
    
    # 6.2 Выпуклый корпус
    # for i in range(len(contours)):
    #     hull = cv2.convexHull(contours[i])
    #     cv2.polylines(result, [hull], True, (0, 255, 0), 1)

    # 6.3  Наименьший покрывающий круг
    for i in range(len(contours)):
        ((x, y), radius) = cv2.minEnclosingCircle(contours[i])
        cv2.circle(result, (int(x), int(y)), int(radius), (0, 255, 255), 2)

    cv2.imshow("center", result)

    # cv2.waitKey(t) 



#? For video
cap = cv2.VideoCapture("../media/VID_20210901_124602.mp4")

count = 0
while cap.isOpened():
    try:
        # Capture frame-by-frame
        cap.set(cv2.CAP_PROP_POS_MSEC, (count * 100))
        ret, frame = cap.read()
        count += 1
        if ret == False:
            break

        DrawCountursToImage(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        pass

#? For image
# img = cv2.imread("../media/photos_with_video/frame15.jpg", 1)
# DrawCountursToImage(img, 0)