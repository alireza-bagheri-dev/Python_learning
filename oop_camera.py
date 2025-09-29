import cv2
import os
from datetime import datetime
from typing import Optional


class Camera:
    """
    Camera class for managing video capture devices.

    Responsibilities:
        - Open a video source (webcam or video file)
        - Capture frames from the source
        - Release resources when finished

    Attributes:
        index (int): The camera index (default=0 for primary webcam).
        cap (cv2.VideoCapture): The OpenCV capture object.
    """

    def __init__(self, index: int = 0):
        """
        Initialize the Camera.

        Args:
            index (int): The index of the camera device (default=0).

        Raises:
            ValueError: If the camera cannot be opened.
        """
        self.index = index
        self.cap = cv2.VideoCapture(index)

        if not self.cap.isOpened():
            raise ValueError(f"❌ Cannot open camera with index={index}")

    def get_frame(self):
        """
        Capture a single frame from the camera.

        Returns:
            ndarray | None: The captured frame, or None if capture failed.
        """
        ret, frame = self.cap.read()
        return frame if ret else None

    def release(self):
        """Release the camera resource."""
        self.cap.release()


class ImageSaver:
    """
    ImageSaver class for storing frames as image files.

    Responsibilities:
        - Save images to a given directory
        - Generate unique filenames when needed

    Attributes:
        directory (str): The directory where images will be saved.
    """

    def __init__(self, directory: str = "captures"):
        """
        Initialize the ImageSaver.

        Args:
            directory (str): The directory to save images in. Defaults to "captures".
        """
        self.directory = directory
        os.makedirs(directory, exist_ok=True)

    def save(self, frame, filename: Optional[str] = None) -> str:
        """
        Save an image frame to disk.

        Args:
            frame (ndarray): The image data to be saved.
            filename (str, optional): The filename. If None, a timestamped filename is used.

        Returns:
            str: The path to the saved image file.
        """
        if filename is None:
            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"

        filepath = os.path.join(self.directory, filename)
        cv2.imwrite(filepath, frame)
        return filepath


class App:
    """
    App class for running the main program loop.

    Responsibilities:
        - Display camera frames
        - Handle user input (e.g., 's' to save, 'q' to quit)
        - Coordinate between Camera and ImageSaver
    """

    def __init__(self, camera_index: int = 0):
        """
        Initialize the App with a Camera and ImageSaver.

        Args:
            camera_index (int): The index of the camera device. Defaults to 0.
        """
        self.camera = Camera(camera_index)
        self.saver = ImageSaver()

    def run(self):
        """
        Start the main application loop.

        - Press 's' to save a snapshot.
        - Press 'q' to quit the program.
        """
        print("▶ Program started. Press 's' to save an image, 'q' to quit.")

        while True:
            frame = self.camera.get_frame()
            if frame is None:
                print("⚠ No frame received. Exiting.")
                break

            cv2.imshow("Camera", frame)

            key = cv2.waitKey(1)
            if key == ord("s"):
                path = self.saver.save(frame)
                print(f"📸 Image saved: {path}")
            elif key == ord("q"):
                print("⏹ Exiting program.")
                break

        self.camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = App()
    app.run()