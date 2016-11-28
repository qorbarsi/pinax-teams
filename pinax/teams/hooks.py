from django.db.models import Q

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


MESSAGE_STRINGS = {
    "joined-team": _('Joined team.'),
    "left-team": _('Left team.'),
    "applied-to-join": _('Applied to join team.'),
    "accepted-application": _('Accepted application.'),
    "rejected-application": _('Rejected application.'),
    "slug-exists": _('Team with this name already exists'),
    "on-team-blacklist": _('You can not create a team by this name.'),
    "user-member-exists": _('User already on team.'),
    "invitee-member-exists": _('Invite already sent.'),
}


class TeamDefaultHookset(object):

    # allows the search field in the Membership admin
    # to be overridden if the custom user model does
    # not have a username field
    membership_search_fields = ["user__username"]

    def build_team_url(self, url_name, team_slug):
        return reverse(url_name, args=[team_slug])

    def get_autocomplete_result(self, user):
        return {"pk": user.pk, "email": user.email, "name": user.get_full_name()}

    def search_queryset(self, query, users):
        return users.filter(
            Q(email__icontains=query) |
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    def get_message_strings(self):
        return MESSAGE_STRINGS

    def user_is_staff(self, user):
        # @@@ consider staff users managers of any Team
        return getattr(user, "is_staff", False)


class HookProxy(object):

    def __getattr__(self, attr):
        from pinax.teams.conf import settings
        return getattr(settings.TEAMS_HOOKSET, attr)


hookset = HookProxy()
