from core.actions.action import Action


class ActionGetGrade(Action):

    def run(self, dialog, tracker):
        """Return result message)"""

        subject = dialog["slots"]["slot_subject"]

        return "Get " + subject + " grade successfully!"
