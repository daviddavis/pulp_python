from logging import getLogger

from django.db import models

from pulpcore.plugin.models import Content, Importer, Publisher
from django.contrib.postgres.fields import ArrayField

log = getLogger(__name__)


class Classifier(models.Model):
    """
    Custom tags for classifier

    Fields:

        name (models.TextField): The name of the classifier

    Relations:

        python_package_content (models.ForeignKey): The PythonPackageContent this classifier
        is associated with.

    """

    name = models.TextField()
    python_package_content = models.ForeignKey("PythonPackageContent", related_name="classifiers",
                                               related_query_name="classifier")


class PythonPackageContent(Content):
    """
    A Content Type representing Python's Distribution Package as
    defined in pep-0426 and pep-0345
    https://www.python.org/dev/peps/pep-0491/
    https://www.python.org/dev/peps/pep-0345/
    """

    TYPE = 'python'
    filename = models.TextField(unique=True, db_index=True, blank=False)
    packagetype = models.TextField(blank=False)
    name = models.TextField(blank=False)
    version = models.TextField(blank=False)
    metadata_version = models.TextField(blank=False)
    summary = models.TextField()
    description = models.TextField()
    keywords = ArrayField(models.TextField())
    home_page = models.TextField()
    download_url = models.TextField()
    author = models.TextField()
    author_email = models.TextField()
    maintainer = models.TextField()
    maintainer_email = models.TextField()
    license = models.TextField()
    requires_python = models.TextField()
    project_url = models.TextField()
    platform = models.TextField()
    supported_platform = models.TextField()
    requires_dist = ArrayField(models.TextField())
    provides_dist = ArrayField(models.TextField())
    obsoletes_dist = ArrayField(models.TextField())
    requires_external = ArrayField(models.TextField())


class PythonPublisher(Publisher):
    """
    A Publisher for PythonContent.

    Define any additional fields for your new publisher if needed.
    A ``publish`` method should be defined.
    It is responsible for publishing metadata and artifacts
    which belongs to a specific repository.
    """

    TYPE = 'python'

    def publish(self):
        """
        Publish the repository.
        """
        raise NotImplementedError


class PythonImporter(Importer):
    """
    An Importer for PythonContent.

    Define any additional fields for your new importer if needed.
    A ``sync`` method should be defined.
    It is responsible for parsing metadata of the content,
    downloading of the content and saving it to Pulp.
    """

    TYPE = 'python'

    def sync(self):
        """
        Synchronize the repository with the remote repository.
        """
        raise NotImplementedError
