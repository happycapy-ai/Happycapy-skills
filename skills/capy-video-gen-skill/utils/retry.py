import tenacity
import traceback
import logging

def after_func(retry_state: tenacity.RetryCallState) -> None:
    if retry_state.outcome.failed:
        exc = retry_state.outcome.exception()
        logging.warning(f"Retrying {retry_state.fn.__name__} due to {repr(exc)} (Attempt {retry_state.attempt_number})")
        logging.debug(traceback.format_exception(type(exc), exc, exc.__traceback__))
