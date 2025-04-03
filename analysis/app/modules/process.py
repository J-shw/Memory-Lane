import os, datetime, requests, magic, logging

logging.basicConfig(level=logging.INFO)


API_ENDPOINT = "http://localhost:9090/files/"

def get_file_metadata(file_path):
    try:
        stat = os.stat(file_path)
        name = os.path.basename(file_path)
        size = stat.st_size
        try:
            date_created = datetime.datetime.fromtimestamp(stat.st_birthtime)
        except AttributeError:
            logging.warning(f"st_birthtime not available for {file_path}, using st_ctime")
            date_created = datetime.datetime.fromtimestamp(stat.st_ctime)

        #date_modified = datetime.datetime.fromtimestamp(stat.st_mtime)
        try:
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(file_path)
        except Exception as e:
            logging.error(f"Error getting mime type for {file_path}: {e}")
            mime_type = None

        extension = os.path.splitext(file_path)[1][1:] #Get extension without the .
        return {
            "name": name,
            "path": file_path,
            "size": size,
            "dateCreated": date_created.isoformat(),
            "mimeType": mime_type,
            "extension": extension,
        }
    except Exception as e:
        logging.error(f"Error getting metadata for {file_path}: {e}")
        return None

def process_directory(directory):

    if not os.path.exists(directory):
        logging.error(f"Directory not found: {directory}")
        return 

    if not os.path.isdir(directory):
        logging.error(f"Not a directory: {directory}")
        return

    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            metadata = get_file_metadata(file_path)
            if metadata:
                try:
                    response = requests.post(API_ENDPOINT, json=metadata)
                    response.raise_for_status()
                    logging.info(f"File {file_path} added successfully.")
                except requests.exceptions.RequestException as e:
                    logging.error(f"Error adding file {file_path}: {e}")