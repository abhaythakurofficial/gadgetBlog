from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from tinymce.models import HTMLField
from gadgetBlog.google_drive_service import upload_images


# Define your Google Drive folder ID
FOLDER_ID = '1t1jvQj_VW8CIrdAf7E6EssovWNPAPOwN'

class Post(models.Model):
    """
    Model for blog posts with support for image uploads to Google Drive.
    """
    category = models.CharField(
        max_length=100, 
        help_text="Main category of the post"
    )
    sub_category = models.CharField(
        max_length=100, 
        help_text="Sub-category of the post"
    )
    title = models.CharField(
        max_length=100, 
        help_text="Title of the post"
    )
    content = HTMLField(
        help_text="Content of the post"
    )
    author = models.CharField(
        max_length=50, 
        help_text="Author of the post"
    )
    image = models.ImageField(
        upload_to='temp_images/',  # Temporary folder for uploaded images
        null=True,
        blank=True,
        help_text="Upload an image for the post"
    )
    image_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL of the image (e.g., from Google Drive)"
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        help_text="Unique identifier for the post URL"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp for the last update"
    )

    def save(self, *args, **kwargs):
        """
        Override save method to upload the image to Google Drive if provided.
        """
        if self.image and not self.image_url:
            # Upload the image to Google Drive
            temp_file_path = self.image.path
            public_url = upload_images(
                file_path=temp_file_path,
                file_name=self.image.name,
                folder_id=FOLDER_ID
            )
            self.image_url = public_url

            # Delete the local file after uploading
            self.image.delete(save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} > {self.sub_category}: {self.title} by {self.author}"


class BlogComment(models.Model):
    """
    Model for managing comments on blog posts.
    """
    sno = models.AutoField(primary_key=True)
    comment = models.TextField(help_text="Comment content")
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        help_text="User who posted the comment"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        help_text="Parent comment (for nested comments)"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="Post the comment is associated with"
    )
    timestamp = models.DateTimeField(
        default=now,
        help_text="Timestamp of the comment"
    )

    def __str__(self):
        return f"{self.comment[:50]}... on '{self.post.title}' by {self.user.username}"
