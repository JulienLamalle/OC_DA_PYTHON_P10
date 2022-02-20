from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from projects.models import Issue, Project


class IsProjectAuthorForProjectViewset(BasePermission):
  def has_permission(self, request, view):
    """
    if the action are update or destroy, the user must be the author of the project
    """
    if view.action not in ("update", "destroy", "partial_update"):
      return True
    project = get_object_or_404(Project, pk=view.kwargs["pk"])
    return project.author == request.user


class IsProjectAuthor(BasePermission):
  """
  we verify that the user is the author of the project
  """

  def has_object_permission(self, request, view, obj):
    return obj.author == request.user


class IsProjectAuthorOrContributor(BasePermission):
  """
  We verify if the user is the author of the project or if the user is a contributor of the project and if the action is not update or destroy
  """

  def has_object_permission(self, request, view, obj):
    if view.action not in ("update", "destroy", "partial_update"):
      return request.user in obj.contributors.all() or obj.author == request.user
    return True


class IsIssueAuthor(BasePermission):
  """
  We verify if the user is the author of the issue in case of the view action is update or destroy
  """

  def has_permission(self, request, view):
    if view.action not in ("update", "destroy", "partial_update"):
      return True
    issue = get_object_or_404(Issue, pk=view.kwargs["pk"])
    return issue.author == request.user
