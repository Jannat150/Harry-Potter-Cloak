import cv2
import numpy as np


def hello(x):
    pass



cap = cv2.VideoCapture(0)

cv2.namedWindow("bars")


# HSV for dark brown cloth
cv2.createTrackbar("LH", "bars", 0, 180, hello)
cv2.createTrackbar("LS", "bars", 40, 255, hello)
cv2.createTrackbar("LV", "bars", 15, 255, hello)

cv2.createTrackbar("UH", "bars", 25, 180, hello)
cv2.createTrackbar("US", "bars", 255, 255, hello)
cv2.createTrackbar("UV", "bars", 255, 255, hello)



print("Move away from camera...")
cv2.waitKey(3000)

ret, init_frame = cap.read()

if not ret:
    print("Camera error")
    cap.release()
    exit()

init_frame = cv2.flip(init_frame, 1)

print("Background captured!")




fourcc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter(
    'invisibility_cloak.avi',
    fourcc,
    20.0,
    (640, 480)
)

recording = False




while True:

    ret, frame = cap.read()

    if not ret:
        break


    frame = cv2.flip(frame, 1)

    # Make sure frame is 640 x 480
    frame = cv2.resize(frame, (640, 480))

    height, width, _ = frame.shape


    # Convert to HSV
    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV
    )


 

    lh = cv2.getTrackbarPos("LH", "bars")
    ls = cv2.getTrackbarPos("LS", "bars")
    lv = cv2.getTrackbarPos("LV", "bars")

    uh = cv2.getTrackbarPos("UH", "bars")
    us = cv2.getTrackbarPos("US", "bars")
    uv = cv2.getTrackbarPos("UV", "bars")


    lower_brown = np.array([lh, ls, lv])
    upper_brown = np.array([uh, us, uv])



    mask = cv2.inRange(
        hsv,
        lower_brown,
        upper_brown
    )



    kernel = np.ones((7, 7), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel,
        iterations=1
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    mask = cv2.dilate(
        mask,
        kernel,
        iterations=1
    )



    face_protection_height = int(height * 0.45)

    mask[0:face_protection_height, :] = 0




    mask_inv = cv2.bitwise_not(mask)


    # Keep everything except brown cloth
    person = cv2.bitwise_and(
        frame,
        frame,
        mask=mask_inv
    )


    # Put background where brown cloth exists
    background = cv2.bitwise_and(
        init_frame,
        init_frame,
        mask=mask
    )


    # Final invisibility effect
    final = cv2.add(
        person,
        background
    )



    if recording:
        out.write(final)

        # Recording indicator
        cv2.putText(
            final,
            "REC",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )


    cv2.imshow(
        "Brown Cloth Mask",
        mask
    )

    cv2.imshow(
        "Dark Brown Invisibility",
        final
    )



    key = cv2.waitKey(1) & 0xFF


    # R → Start recording
    if key == ord('r'):

        recording = True

        print("Recording started...")


    # S → Stop recording
    elif key == ord('s'):

        recording = False

        print("Recording stopped!")


    # Q → Quit
    elif key == ord('q'):

        break




cap.release()
out.release()
cv2.destroyAllWindows()

print("Video saved as invisibility_cloak.avi")