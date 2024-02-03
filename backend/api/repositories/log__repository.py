from ..interfaces.log_interface import LogInterface
from ..models import Log, Step


class LogRepository(LogInterface):
    def create(self, text: str, sender: str, step: Step):
        return Log(text=text, sender=sender, step=step).save()
