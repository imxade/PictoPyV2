import cv2
from yolov8 import detectClasses
from typing import Generator, Tuple, Set

def extractFrames(inputPath: str, skip: int = 6) -> Generator:
    """
    Extract frames from a video file.

    Args:
    - inputPath: Path to the input video file.
    - skip: Number of frames to skip between extracted frames (default is 6).

    Returns:
    - Generator: Yields frames from the video file.
    """
    cap = cv2.VideoCapture(inputPath)
    frameCount = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frameCount % skip == 0:
            yield frame
        frameCount += 1
    cap.release()

def processFrames(frames: Generator, modelPath: str) -> Generator:
    """
    Process frames using a detection model.

    Args:
    - frames: Generator yielding frames.
    - modelPath: Path to the detection model.

    Yields:
    - Generator: Yields detected classes for each frame.
    """
    for frame in frames:
        yield detectClasses(frame, modelPath)

def saveVideo(outputPath: str, frames: Generator, fps: float, frameSize: Tuple[int, int]):
    """
    Save frames as a video file.

    Args:
    - outputPath: Path to save the output video file.
    - frames: Generator yielding frames to save.
    - fps: Frames per second (FPS) of the output video.
    - frameSize: Size of each frame (width, height).
    """
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(outputPath, fourcc, fps, frameSize)
    for frame in frames:
        out.write(frame)
    out.release()

def videoClasses(inputPath: str, modelPath: str, outputPath: str = None) -> Set[str]:
    """
    Extract and save video classes.

    Args:
    - inputPath: Path to the input video file.
    - modelPath: Path to the detection model.
    - outputPath: Optional path to save the output video file.

    Returns:
    - Set[str]: Set of unique classes detected across all frames.
    """
    frames = extractFrames(inputPath)
    fps = cv2.VideoCapture(inputPath).get(cv2.CAP_PROP_FPS)
    firstFrameClasses, firstFrame = next(processFrames(frames, modelPath))

    def combinedFrames() -> Generator:
        yield firstFrame
        for _, frame in processFrames(frames, modelPath):
            yield frame

    if outputPath:
        height, width, _ = firstFrame.shape
        frameSize = (width, height)

        # Save the first frame and the rest of the processed frames
        saveVideo(outputPath, combinedFrames(), fps, frameSize)

    # Collect and return combined classes from each frame of the video
    allClasses = set(firstFrameClasses)
    for classes, _ in processFrames(frames, modelPath):
        allClasses.update(classes)
    
    return allClasses
