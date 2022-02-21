from cmath import e
from itertools import chain
from django.db import IntegrityError

from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter

from projects import serializers

from projects.models import Project, Contributor, Issue, Comment
from projects.serializers import ContributorSerializer, ProjectSerializer, ProjectDetailSerializer, IssueSerializer, CommentSerializer
from projects.permissions import IsCommentAuthor, IsProjectAuthorForProjectViewset, IsProjectAuthor, IsProjectAuthorOrContributor, IsIssueAuthor, IsIssueAuthorOrProjectContributorOrProjectAuthor, IsIssueAuthorOrProjectContributorOrProjectAuthorSoHeCanCreateAnIssueComment

from authentication.models import User


class MultipleSerializerMixin:

  detail_serializer_class = None

  def get_serializer_class(self):
    if self.action == 'retrieve' and self.detail_serializer_class is not None:
      return self.detail_serializer_class
    return super().get_serializer_class()


class ProjectViewSet(MultipleSerializerMixin, viewsets.ModelViewSet):
  serializer_class = ProjectSerializer
  detail_serializer_class = ProjectDetailSerializer
  permission_classes = [IsAuthenticated, IsProjectAuthorForProjectViewset]

  def get_queryset(self):
    current_user_projects = Project.objects.filter(author=self.request.user)
    current_user_projects_contributions = Project.objects.filter(
      contributors=self.request.user)
    return set(
        list(chain(current_user_projects, current_user_projects_contributions)))

  def perform_create(self, serializer):
    serializer.save(author=self.request.user)

  def update(self, request, *args, **kwargs):
    project = get_object_or_404(Project, pk=self.kwargs["pk"])
    serializer = ProjectSerializer(project, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def retrieve(self, request, *args, **kwargs):
    project = get_object_or_404(Project, pk=self.kwargs["pk"])
    return Response(ProjectDetailSerializer(project).data)

  def destroy(self, request, *args, **kwargs):
    project = get_object_or_404(Project, pk=self.kwargs["pk"])
    if project.delete():
      return Response({'message': 'Project deleted'}, status=status.HTTP_204_NO_CONTENT)


class ContributorViewSet(viewsets.ModelViewSet):
  serializer_class = ContributorSerializer
  permission_classes = [IsAuthenticated, IsProjectAuthor]

  @extend_schema(parameters=[OpenApiParameter(name='project_id', location=OpenApiParameter.QUERY, required=True)])
  def list(self, request, *args, **kwargs):
    contributions = Contributor.objects.filter(
      project__id=request.query_params.get('project_id'))
    return Response(self.serializer_class(contributions, many=True).data)

  def perform_create(self, serializer):
    request = self.request
    user = get_object_or_404(User, pk=request.data.get('user_id'))
    project = get_object_or_404(Project, pk=request.data.get('project_id'))
    if user.id == project.author_id:
      raise serializers.ValidationError(
        {'message': 'A project author cannot be a contributor to his own project'})
    try:
      serializer.save(project=project, user=user)
    except IntegrityError as e:
      raise serializers.ValidationError(
        {'message': 'This user cannot be added to this project contributor'}) from e

  def destroy(self, request, *args, **kwargs):
    contributions = Contributor.objects.get(pk=self.kwargs["pk"])
    if contributions.delete():
      return Response({'message': 'Contribution deleted'}, status=status.HTTP_204_NO_CONTENT)


class IssueViewSet(viewsets.ModelViewSet):
  serializer_class = IssueSerializer
  permission_classes = [IsAuthenticated,
                        IsProjectAuthorOrContributor, IsIssueAuthor]

  @extend_schema(parameters=[OpenApiParameter(name='project_id', location=OpenApiParameter.QUERY, required=True)])
  def list(self, request, *args, **kwargs):
    issues = Issue.objects.filter(
      project__id=request.query_params.get('project_id'))
    return Response(self.serializer_class(issues, many=True).data)

  def perform_create(self, serializer):
    project = get_object_or_404(
      Project, pk=self.request.data.get('project_id'))
    serializer.save(project=project, author=self.request.user,
                    assignee=project.author)

  def retrieve(self, request, *args, **kwargs):
    issue = get_object_or_404(
      Issue, pk=self.kwargs["pk"])
    return Response(IssueSerializer(issue).data)

  def destroy(self, request, *args, **kwargs):
    issue = get_object_or_404(
      Issue, pk=self.kwargs["pk"])
    if issue.delete():
      return Response({'message': 'Issue deleted'}, status=status.HTTP_204_NO_CONTENT)

  def update(self, request, *args, **kwargs):
    issue = get_object_or_404(Issue, pk=self.kwargs["pk"])
    serializer = IssueSerializer(issue, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
  serializer_class = CommentSerializer
  permission_classes = [IsAuthenticated, IsCommentAuthor,
                        IsIssueAuthorOrProjectContributorOrProjectAuthor,
                        IsIssueAuthorOrProjectContributorOrProjectAuthorSoHeCanCreateAnIssueComment
                        ]

  @extend_schema(parameters=[OpenApiParameter(name='issue_id', location=OpenApiParameter.QUERY, required=True)])
  def list(self, request, *args, **kwargs):
    comments = Comment.objects.filter(
      issue_id=request.query_params.get('issue_id'))
    return Response(self.serializer_class(comments, many=True).data)

  def perform_create(self, serializer):
    issue = get_object_or_404(
      Issue, pk=self.request.data.get('issue_id'))
    serializer.save(issue=issue, author=self.request.user)

  def retrieve(self, request, *args, **kwargs):
    comment = get_object_or_404(Comment, pk=self.kwargs["pk"])
    return Response(CommentSerializer(comment).data)

  def update(self, request, *args, **kwargs):
    comment = get_object_or_404(Comment, pk=self.kwargs["pk"])
    serializer = CommentSerializer(comment, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, *args, **kwargs):
    comment = get_object_or_404(
      Comment, pk=self.kwargs["pk"])
    if comment.delete():
      return Response({'message': 'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)
