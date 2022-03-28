import cv2
import numpy as np


def draw_reactangle_with_drag(event, x, y, flags, param):
    """
    Let's you draw a single rectangle by dragging the mouse.
    """
    global ix, iy, drawing, img1
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix = x
        iy = y


    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img_updated = cv2.imread("homography/test_imgs/book1.jpg")
            cv2.rectangle(img_updated, pt1=(ix,iy), pt2=(x, y),color=(0,255,255),thickness=10)
            img1 = img_updated

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        img_updated = cv2.imread("homography/test_imgs/book1.jpg")
        cv2.rectangle(img_updated, pt1=(ix,iy), pt2=(x, y),color=(0,255,255),thickness=10)
        img1 = img_updated


def homography(img_src, img_dst):
    """
    Homography transform between two planes.
    """

    # Four corners of the book in source image
    pts_src = np.array([[141, 131], [480, 159], [493, 630], [64, 601]])

    # Four corners of the book in destination image.
    pts_dst = np.array([[318, 256], [534, 372], [316, 670], [73, 473]])

    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)

    # Warp source image to destination based on homography
    img_out = cv2.warpPerspective(img_src, h, (img_dst.shape[1],img_dst.shape[0]))

    # Display images
    cv2.imshow("Source Image", img_src)
    cv2.imshow("Destination Image", img_dst)
    cv2.imshow("Warped Source Image", img_out)

    cv2.waitKey(0)


if __name__ == '__main__':

    # read images
    img1 = cv2.imread("homography/test_imgs/book1.jpg")
    img2 = cv2.imread("homography/test_imgs/book2.jpg")

    # variables
    ix = -1
    iy = -1
    drawing = False

    # try homography
    homography(img2, img1)

    # try rectangle with drag
    cv2.namedWindow(winname= "Rectangle Drawer")
    cv2.setMouseCallback("Title of Popup Window", draw_reactangle_with_drag)

    while True:
        cv2.imshow("Title of Popup Window", img1)
        if cv2.waitKey(10) == 27:
            break
    cv2.destroyAllWindows()