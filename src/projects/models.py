from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
  title = models.CharField(max_length=128)
  description = models.TextField(max_length=1000)
  type = models.CharField(max_length=128)
  author = models.ForeignKey(
      to=User, on_delete=models.CASCADE, related_name='author_project'
  )
  contributors = models.ManyToManyField(User, through="Contributor")
  created_time = models.DateTimeField(auto_now_add=True)
  
  def issues(self):
    return Issue.objects.filter(project=self)

  class Meta:
    ordering = ["-created_time"]
    verbose_name = "Project"

  def __str__(self):
    return str(self.title)


class Contributor(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  project = models.ForeignKey(Project, on_delete=models.CASCADE)
  role = models.CharField(max_length=128)

  class Meta:
    unique_together = ('user', 'project')

  def __str__(self):
    return str(self.user)


class Issue(models.Model):
  title = models.CharField(max_length=128)
  description = models.TextField(max_length=1000)
  tag = models.CharField(max_length=128)
  priority = models.CharField(max_length=128)
  status = models.CharField(max_length=128)
  created_time = models.DateTimeField(auto_now_add=True)
  author = models.ForeignKey(
      to=User, on_delete=models.CASCADE, related_name='author_issue'
  )
  assignee = models.ForeignKey(
      to=User, on_delete=models.CASCADE, related_name='assignee'
  )
  project = models.ForeignKey(
    to=Project, on_delete=models.CASCADE, related_name='issue')

  class Meta:
    ordering = ["-created_time"]
    verbose_name = "Issue"

  def __str__(self):
    return str(self.title)


class Comment(models.Model):
  description = models.TextField(max_length=1000)
  author = models.ForeignKey(
      to=User, on_delete=models.CASCADE, related_name='author_comment'
  )
  issue = models.ForeignKey(
    to=Issue, on_delete=models.CASCADE, related_name='comment')
  created_time = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ["-created_time"]
    verbose_name = "Comment"
