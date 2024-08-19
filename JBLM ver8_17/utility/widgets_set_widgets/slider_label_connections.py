from PyQt6.QtWidgets import QSlider, QLabel
from logger_setup import logger


def connect_label_to_slider(slider: QSlider, label: QLabel) -> None:
    """
    Connects a slider's valueChanged signal to a label's setValue slot and vice versa.

    Parameters:
        slider (QSlider): The slider object.
        label (QLabel): The label object.

    Returns:
        None
    """
    try:
        if slider is not None and label is not None:
            if isinstance(slider, QSlider) and isinstance(label, QLabel):
                # Connect the slider's valueChanged signal to the label's setValue slot
                slider.valueChanged.connect(label.setValue)
    except Exception as e:
        logger.error(f"Error connecting signals and slots: {e}")
