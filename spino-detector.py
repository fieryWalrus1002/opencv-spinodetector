from tokenize import String
import cv2
import numpy as np
import argparse


def bbcolor(s):
    # custom type for argparse, just for fun
    try:
        b, g, r = map(int, s.split(","))
        return b, g, r
    except:
        raise argparse.ArgumentTypeError("color must be b, g, r")


def get_hsv_bounds(color: String):
    # jeez I only needed to find a skyblue dinosaur. add your own colors!
    # light blue hsv bounds (0-180, 0-255, 0-255)
    # gimp values are 0-360, 0-100, 0-100 fyi

    if color == "skyblue":
        lower_bound = (109, 41, 154)
        upper_bound = (124, 255, 255)

    if color != "skyblue":
        lower_bound = (109, 41, 154)
        upper_bound = (124, 255, 255)

    return lower_bound, upper_bound


def gimp2cv(h, s, v):
    # convert hsv values from gimp values to opencv values
    h1 = h / 2
    s1 = s / 100 * 255
    v1 = v / 100 * 255
    return (h1, s1, v1)


def get_hsv_mask(image: np.ndarray, lower_bound, upper_bound):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    return mask


def main(color: String, cam: int, bbcolor: String):
    cam = cv2.VideoCapture(0)
    img_counter = 0
    cv2.namedWindow("cam", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("cam", 1200, 900)

    # rgb of bounding box
    rect_color = (bbcolor[0], bbcolor[1], bbcolor[2])

    while True:
        ret, image = cam.read()

        # mask creation
        lower_bound, upper_bound = get_hsv_bounds(color)
        hsv_mask = get_hsv_mask(image, lower_bound, upper_bound)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        hsv_mask = cv2.morphologyEx(hsv_mask, cv2.MORPH_CLOSE, kernel)

        res = cv2.bitwise_and(image, image, mask=hsv_mask)

        res = cv2.erode(res, kernel, iterations=2)

        res = cv2.dilate(res, kernel, iterations=3)

        # find edges
        edges = cv2.Canny(res, 30, 200)

        # find contours
        cnt, hier = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # draw bounding box for contours on image
        for c in cnt:
            [x, y, w, h] = cv2.boundingRect(c)
            cv2.rectangle(image, (x, y), (x + w, y + h), rect_color, 3)

        # display image
        cv2.imshow("cam", image)

        k = cv2.waitKey(1)

        if k % 256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name = "possible_dinosaur_{}.png".format(img_counter)
            cv2.imwrite(img_name, image)
            print("{} written!".format(img_name))
            img_counter += 1
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="select dinosaur color via command line"
    )

    parser.add_argument(
        "-color",
        help="Select color of dinosaur to locate",
        type=str,
        default="skyblue",
    )

    parser.add_argument(
        "-cam",
        help="Select camera to use",
        type=int,
        default=0,
    )

    parser.add_argument(
        "-bbcolor",
        help="Select b,g,r color to use for dino bounding box",
        dest="bbcolor",
        type=bbcolor,
        default="255, 0, 255",
    )

    args = parser.parse_args()

    main(**vars(args))
