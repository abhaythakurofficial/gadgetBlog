import os  # For file path handling
from django.db import models
from tinymce.models import HTMLField
from gadgetBlog.google_drive_service import upload_images  # Function for Google Drive upload

# Google Drive folder ID where images will be uploaded
FOLDER_ID = '1t1jvQj_VW8CIrdAf7E6EssovWNPAPOwN'


class AnimeMovie(models.Model):
    """
    Model to represent anime movies, including Google Drive integration for poster uploads.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, help_text="Title of the anime movie")
    description = HTMLField(help_text="Detailed description of the movie")
    poster_1 = models.ImageField(
        upload_to='temp_images/', 
        blank=True, 
        null=True, 
        help_text="Upload the first poster"
    )
    poster_2 = models.ImageField(
        upload_to='temp_images/', 
        blank=True, 
        null=True, 
        help_text="Upload the second poster"
    )
    poster_3 = models.ImageField(
        upload_to='temp_images/', 
        blank=True, 
        null=True, 
        help_text="Upload the third poster"
    )
    poster_1_url = models.URLField(
        blank=True, 
        null=True, 
        help_text="Google Drive URL for the first poster"
    )
    poster_2_url = models.URLField(
        blank=True, 
        null=True, 
        help_text="Google Drive URL for the second poster"
    )
    poster_3_url = models.URLField(
        blank=True, 
        null=True, 
        help_text="Google Drive URL for the third poster"
    )
    download_link = models.URLField(
        max_length=500, 
        help_text="Direct download link for the anime movie"
    )
    genre = models.CharField(
        max_length=100,
        choices=[
            ('Action', 'Action'),
            ('Comedy', 'Comedy'),
            ('Drama', 'Drama')
        ],
        help_text="Genre of the movie"
    )
    release_date = models.DateField(help_text="Release date of the anime movie")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of creation")
    author = models.CharField(
        max_length=100,
        choices=[
            ('Abhay Thakur', 'Abhay Thakur'),
            ('Ashish Ala', 'Ashish Ala')
        ],
        help_text="Author of the movie entry"
    )

    def save(self, *args, **kwargs):
        """
        Overrides save method to upload posters to Google Drive and update URLs.
        """
        poster_fields = [
            ('poster_1', 'poster_1_url'),
            ('poster_2', 'poster_2_url'),
            ('poster_3', 'poster_3_url'),
        ]

        for poster_field, poster_url_field in poster_fields:
            poster_file = getattr(self, poster_field, None)  # Get the poster file
            if poster_file and not getattr(self, poster_url_field):  # If the file exists and no URL is set
                try:
                    temp_file_path = poster_file.path  # Path to the file
                    if os.path.exists(temp_file_path):  # Check if the file exists
                        public_url = upload_images(
                            file_path=temp_file_path,
                            file_name=poster_file.name,
                            folder_id=FOLDER_ID
                        )
                        setattr(self, poster_url_field, public_url)  # Set the Google Drive URL
                        poster_file.delete(save=False)  # Delete the local file after upload
                except Exception as e:
                    print(f"Error uploading {poster_field}: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.genre}) - Released on {self.release_date} by {self.author}"
