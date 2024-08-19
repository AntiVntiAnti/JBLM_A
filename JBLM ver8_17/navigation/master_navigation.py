# from sexy_logger import logger
from logger_setup import logger
from typing import Any


def change_mainStack(mainStack: Any, index: int) -> None:
    """
    Change the current index of the main stack.

    Args:
    mainStack (Any): The main stack object.
    index (int): The new index to set.

    Returns:
    None
    """
    try:
        mainStack.setCurrentIndex(index)
    except Exception as e:
        logger.error(f"main stack Page Change Error: {e}", exc_info=True)


def change_alpha_stack_page(stack_alpha: Any,
                            index: int) -> None:
    """
    Change the current index of the alpha stack.

    Args:
    stack_alpha (Any): The alpha stack object.
    index (int): The new index to set.

    Returns:
    None
    """
    try:
        stack_alpha.setCurrentIndex(index)
        logger.info("Alpha Stack Page Change")
    except Exception as e:
        logger.error(f"Alpha Stack Page Change Error: {e}", exc_info=True)


def change_agenda_stack_page(agenda_stack: Any,
                             index: int) -> None:
    """
    Change the current page of the agenda stack to the specified index.

    Args:
        agenda_stack (Any): The agenda stack widget.
        index (int): The index of the page to be set as the current page.

    Returns:
        None

    Raises:
        Exception: If an error occurs while changing the agenda stack page.
    """
    try:
        agenda_stack.setCurrentIndex(index)
        logger.info("Agenda Stack Page Change")
    except Exception as e:
        logger.error(f"Agenda Stack Page Change Error: {e}", exc_info=True)
