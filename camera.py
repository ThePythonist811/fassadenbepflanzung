import cv2
import os
import time
import platform

# Directory for saving images
save_dir = "images"
os.makedirs(save_dir, exist_ok=True)

def capture_image_pc():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    if ret:
        return frame
    camera.release()
    return None

def capture_image_pi():
    try:
        from picamera import PiCamera
        camera = PiCamera()
        camera.start_preview()
        time.sleep(2)  # Warm-up time
        camera.capture('temp.jpg')
        camera.close()
        return cv2.imread('temp.jpg')
    except ImportError:
        return None

def run():
    try:
        try:
            # Detect system and use appropriate camera
            if platform.system() == 'Linux' and os.path.exists('/proc/device-tree/model'):
                with open('/proc/device-tree/model') as f:
                    if 'Raspberry Pi' in f.read():
                        frame = capture_image_pi()
                    else:
                        frame = capture_image_pc()
            else:
                frame = capture_image_pc()

            if frame is not None:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = os.path.join(save_dir, f"webcam_{timestamp}.jpg")
                cv2.imwrite(filename, frame)
                print(f"Image saved: {filename}")
            else:
                print("Failed to capture image")

        except Exception as e:
            print(f"An error occurred: {e}")
    except KeyboardInterrupt:
        print("Program terminated")

    finally:
        cv2.destroyAllWindows()

