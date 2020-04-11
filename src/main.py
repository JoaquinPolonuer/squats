import cv2
import sys

arg = sys.argv[1]
try:
    im = cv2.imread(arg)
    cv2.imshow('Hola', im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except Exception as e:
    print('ERROR:',e)
