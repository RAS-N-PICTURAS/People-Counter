import cv2
from .core.tool import Tool
from .people_counter_request_message import PeopleCounterParameters


class PeopleCounterTool(Tool):

    def __init__(self) -> None:
        """
        Initialize the PeopleCounterTool with the pre-trained HOG descriptor.
        """
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def apply(self, parameters: PeopleCounterParameters):
        """
        Detect people in the input image and save an annotated output image.

        Args:
            parameters (PeopleCounterParameters): Parameters containing the input and output image URIs.

        Returns:
            int: The number of people detected in the image.
        """
        # Load the input image
        input_image = cv2.imread(parameters.inputImageURI)

        if input_image is None:
            raise FileNotFoundError(f"Input image not found at {parameters.inputImageURI}")

        # Detect people using HOG descriptor
        boxes, _ = self.hog.detectMultiScale(
            input_image,
            winStride=(8, 8),
            padding=(16, 16),
            scale=1.05
        )

        # Annotate the image with bounding boxes
        for (x, y, w, h) in boxes:
            cv2.rectangle(input_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Save the annotated image
        cv2.imwrite(parameters.outputImageURI, input_image)

        # Return the count of detected people
        return len(boxes)
