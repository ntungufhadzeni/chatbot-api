from ..interfaces.step_interface import StepInterface
from ..models import Step


class StepRepository(StepInterface):
    def __init__(self, user):
        self.user = user

    def get(self):
        return Step.objects.all()[0]

    def create(self):
        return Step.objects.create(user=self.user)

    def update(self, name: str, step: Step):
        step.name = name
        step.save()
        return step
