import os, datetime, requests, magic, logging, shutil, platform

logging.basicConfig(level=logging.INFO)


API_ENDPOINT = "http://localhost:9090"

def get_volume_data(directory, volume_id):
    try:
        total_size = shutil.disk_usage(directory).total
        free_space = shutil.disk_usage(directory).free
        used_space = total_size - free_space
        total_files = 0
        total_folders = 0

        for root, dirs, files in os.walk(directory):
            total_files += len(files)
            total_folders += len(dirs)

        if platform.system() == 'Windows':
            mount_point = os.path.splitdrive(directory)[0]
            name = os.path.basename(os.path.splitdrive(directory)[0]) #Get drive letter as name
        else:
            mount_point = '/'
            name = os.path.basename(directory)

        return {
            "volumeId": volume_id,
            "totalSize": total_size,
            "freeSpace": free_space,
            "usedSpace": used_space,
            "totalFiles": total_files,
            "totalFolders": total_folders,
        }
    except Exception as e:
        logging.error(f"Error getting volume data for {directory}: {e}")
        return None

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
        date_modified = datetime.datetime.fromtimestamp(stat.st_mtime)
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
            "dateModified": date_modified.isoformat(),
            "mimeType": mime_type,
            "extension": extension,
        }
    except Exception as e:
        logging.error(f"Error getting metadata for {file_path}: {e}")
        return None

def process_directory(directory, volume_id):
    if not os.path.exists(directory):
        logging.error(f"Directory not found: {directory}")
        return 

    if not os.path.isdir(directory):
        logging.error(f"Not a directory: {directory}")
        return

    volume_data = get_volume_data(directory, volume_id)
    
    if volume_data:
        try:
            response = requests.post(f"{API_ENDPOINT}/volume_stats/", json=volume_data)
            response.raise_for_status()
            logging.info(f"Volume data for {directory} added successfully.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error adding volume data for {directory}: {e}")

    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            metadata = get_file_metadata(file_path)
            metadata['volumeId'] = volume_id
            if metadata:
                try:
                    response = requests.post(f"{API_ENDPOINT}/files/", json=metadata)
                    response.raise_for_status()
                    logging.info(f"File {file_path} added successfully.")
                except requests.exceptions.RequestException as e:
                    logging.error(f"Error adding file {file_path}: {e}")