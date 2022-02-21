from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from projects.models import Comment, Issue, Project


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
  
  
class IsCommentAuthor(BasePermission):
  """
  We verify if the user is the author of the comment in case of the view action is update or destroy
  """

  def has_permission(self, request, view):
    if view.action not in ("update", "destroy", "partial_update"):
      return True
    comment = get_object_or_404(Comment, pk=view.kwargs["pk"])
    return comment.author == request.user
  
  
class IsIssueAuthorOrProjectContributorOrProjectAuthor(BasePermission):
  """
  To display a list of comments related to an issue we verify if the user is the author of the issue or if the user is a contributor or the author of the project
  """

  def has_permission(self, request, view):
    if view.action not in ('list'):
      return True
    issue = get_object_or_404(Issue, pk=request.query_params.get('issue_id'))
    return request.user in issue.project.contributors.all() or issue.author == request.user or request.user == issue.project.author
  

class IsIssueAuthorOrProjectContributorOrProjectAuthorSoHeCanCreateAnIssueComment(BasePermission):
  """
  To create a comment related to an issue we verify if the user is the author of the issue or if the user is a contributor or the author of the project
  """

  def has_permission(self, request, view):
    if view.action not in ('create'):
      return True
    issue = get_object_or_404(Issue, pk=request.data.get('issue_id'))
    return request.user in issue.project.contributors.all() or issue.author == request.user or request.user == issue.project.author