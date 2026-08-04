from .models import WordContribution


def approve_contribution(contribution):

    contribution.status = WordContribution.STATUS_APPROVED
    contribution.save()


def reject_contribution(contribution):

    contribution.status = WordContribution.STATUS_REJECTED
    contribution.save()