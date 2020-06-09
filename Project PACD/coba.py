import sys
import math
import cv2 as cv
import numpy as np

def main(argv):
    
    default_file = 'sudoku.png'
    filename = argv[0] if len(argv) > 0 else default_file
    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1
    
    
    dst = cv.Canny(src, 50, 200, None, 3)
    
    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    test1 = cv.GaussianBlur(src, (5, 5), 0)
    test1 = cv.Canny(test1, 50, 200, None, 3)
    test2 = np.copy(src)

    lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
    
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv.line(cdst, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
    
    
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 100, 20)
    
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv.LINE_AA)

    
    test2=cv.inRange(cdstP,(0,0,255),(0,0,255))
    test2 = cv.dilate(test2, None, iterations=10)
    test2 = cv.erode(test2,None, iterations=9)
    test2 = cv.dilate(test2, None, iterations=9)
    test2 = cv.erode(test2,None,iterations=6)
    contours, _hierarchy = cv.findContours(test2, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        cnt_len = cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, 0.02*cnt_len, True)
        if len(approx) == 4:
            (x, y, w, h) = cv.boundingRect(approx)

            cv.drawContours(test2, [cnt], -1, (0, 255, 0), 2)



    cv.imshow("Source", src)
    cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
    cv.imshow("test2", test2)
    
    cv.waitKey()
    return 0
    
if __name__ == "__main__":
    main(sys.argv[1:])