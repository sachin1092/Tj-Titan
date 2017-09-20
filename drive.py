from httplib2 import Http

from oauth2client.service_account import ServiceAccountCredentials

from apiclient.discovery import build
from apiclient.http import MediaFileUpload

import os

def upload_data(path, file_type="image"):

	scopes = ['https://www.googleapis.com/auth/drive']

	credentials = ServiceAccountCredentials.from_json_keyfile_name(
	    'keys/Tj-titan-9843c85fd4bb.json', scopes=scopes)
	delegated_credentials = credentials.create_delegated('me@sachinshinde.com')


	http_auth = delegated_credentials.authorize(Http())


	drive = build('drive', 'v3', http=http_auth)

	file_metadata = {'name': path.split("/")[-1]}
	media = MediaFileUpload(path,
	                        mimetype='image/jpeg' if file_type=="image" else 'video/h264')
	file = drive.files().create(body=file_metadata,
	                                    media_body=media,
	                                    fields='id').execute()
	return file.get('id')

def upload_and_delete(path, file_type="image"):
	upload_data(path, file_type)
	os.remove(path)

if __name__ == '__main__':
	upload_data("files/videos/video.h264", "video")