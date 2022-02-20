from rest_framework import serializers

from authentication.serializers import UserSerializer
from projects.models import Project, Contributor, Issue, Comment
from rest_framework import serializers

ValidationError = serializers.ValidationError


class ContributorSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)

  class Meta:
    model = Contributor
    fields = ['id', 'user', 'role']


class CommentSerializer(serializers.ModelSerializer):
  author = UserSerializer(read_only=True)

  class Meta:
    model = Comment
    fields = ['id', 'author', 'description', 'created_time']


class IssueSerializer(serializers.ModelSerializer):
  author = UserSerializer(read_only=True)
  assignee = UserSerializer(read_only=True)
  comments = CommentSerializer(many=True, read_only=True)

  ENUM_PRIORITY = {
    'faible': 'faible',
    'moyenne': 'moyenne',
    'élevée': 'élevée',
  }

  ENUM_TAGS = {
    'bug': 'bug',
    'amélioration': 'amélioration',
    'tâche': 'tâche',
  }

  ENUM_STATUS = {
    'à faire': 'à faire',
    'en cours': 'en cours',
    'terminé': 'terminé',
  }

  def validate_priority(self, value):
    if value not in self.ENUM_PRIORITY.values():
      raise ValidationError(
        f'Priority must be one of {self.ENUM_PRIORITY.values()}')
    return value

  def validate_status(self, value):
    if value not in self.ENUM_STATUS.values():
      raise ValidationError(
        f'Status must be one of  { self.ENUM_STATUS.values()}')
    return value

  def validate_tag(self, value):
    if value not in self.ENUM_TAGS.values():
      raise ValidationError(f'Tags must be one of {self.ENUM_TAGS.values()}')
    return value

  class Meta:
    model = Issue
    fields = ['id', 'title', 'description', 'author', 'assignee', 'created_time',
              'priority', 'status', 'tag', 'comments']


class ProjectSerializer(serializers.ModelSerializer):

  issues = IssueSerializer(many=True, read_only=True)
  comments = CommentSerializer(many=True, read_only=True)
  contributors = UserSerializer(many=True, read_only=True)
  author = UserSerializer(read_only=True)

  class Meta:
    model = Project
    fields = [
        'id', 'title', 'description', 'type', 'author',
        'contributors', 'issues', 'comments',
    ]


class ProjectDetailSerializer(ProjectSerializer):
  issues = IssueSerializer(many=True, read_only=True)
  comments = CommentSerializer(many=True, read_only=True)
  contributors = UserSerializer(many=True, read_only=True)
  author = UserSerializer(read_only=True)

  class Meta:
    model = Project
    fields = [
        'id', 'title', 'description', 'type', 'author',
        'contributors', 'issues', 'comments', 'created_time',
    ]
