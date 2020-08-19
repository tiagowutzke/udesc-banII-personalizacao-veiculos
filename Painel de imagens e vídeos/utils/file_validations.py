def allowed_file(filename, media):
    ALLOWED_EXTENSIONS = {
        'audios': ['mp3', 'wav', 'webm', 'ogg'],
        'videos': ['mp4', 'kmv', 'wmv', 'mov'],
        'images': ['jpg', 'jpeg', 'png', 'gif'],
    }
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[media]