from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive.file']  # Adjusted scope to be more specific
SERVICE_ACCOUNT_FILE = 'service_account.json'  # Path to your service account JSON file
PARENT_FOLDER_ID = '1t1jvQj_VW8CIrdAf7E6EssovWNPAPOwN'  # Replace with your Google Drive folder ID


def authenticate():
    """
    Authenticate with Google Drive using a service account.
    """
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        return creds
    except Exception as e:
        raise Exception(f"Failed to authenticate: {e}")


def upload_images(file_path):
    """
    Upload an image file to Google Drive and return the public URL.
    
    Args:
        file_path (str): Path to the image file to upload.
        
    Returns:
        str: Public URL of the uploaded file.
    """
    try:
        # Authenticate and initialize the Google Drive API service
        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)

        # Extract the file name from the file path
        file_name = file_path.split('/')[-1]

        # Prepare metadata for the file
        file_metadata = {
            'name': file_name,  # Name of the file in Google Drive
            'parents': [PARENT_FOLDER_ID],  # Folder ID where the file will be stored
        }

        # Prepare the media content for upload
        media = MediaFileUpload(file_path, mimetype='image/jpeg')  # Adjust MIME type if needed

        # Upload the file
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'  # Only fetch the file ID after upload
        ).execute()

        # Generate the public URL for the uploaded file
        file_id = uploaded_file.get('id')
        if file_id:
            # Update file permissions to make it publicly accessible
            service.permissions().create(
                fileId=file_id,
                body={
                    'role': 'reader',
                    'type': 'anyone'
                }
            ).execute()

            # Return the public URL of the file
            public_url = f"https://drive.google.com/uc?id={file_id}"
            print(f"File uploaded successfully: {public_url}")
            return public_url
        else:
            raise Exception("File ID not returned by Google Drive API.")
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None


