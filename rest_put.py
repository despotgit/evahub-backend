import os
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from auth import verifyUser, finalizeResponse
from db_user_documents_broker import addDbUserLog
from common import getDocumentFileInfo

rest_put = Blueprint("rest_put", __name__)

# Log helper
def log_debug(msg):
    log_file = "/home/despot82/debug_upload.log"  # choose a writable path
    with open(log_file, "a") as f:
        f.write(msg + "\n")

@rest_put.before_request
@jwt_required(locations=["headers"])
def before_request():
    log_debug("🔹 In before_request")

@rest_put.route(
    "/document/document-type/<documentType>/username/<username>", methods=["PUT"]
)
def uploadDocument(documentType, username):
    try:
        with open("/home/despot82/debug_upload.log", "a") as f:
            f.write(f"UPLOAD HIT: documentType={documentType}, username={username}\n")
    except Exception as e:
        print("Logging error:", e)
        with open("/home/despot82/debug_upload.log", "a") as f:
            f.write(f"SOME SHIT HPND")

    log_debug(f"🔥 uploadDocument called for {documentType} / {username}")

    # Verify user
    v = verifyUser(username)
    if not v["verified"]:
        log_debug(f"❌ User verification failed: {v}")
        return finalizeResponse(v)
    log_debug("✅ User verified")

    # Grab file
    if "file" not in request.files:
        log_debug("❌ No file in request")
        return finalizeResponse({"authenticated": False, "status": "error", "message": "No file uploaded"})

    f = request.files["file"]
    log_debug(f"Received file: {f.filename}")

    # Determine where to save
    secureFilename, userDir, uploadLocation = getDocumentFileInfo(documentType, username, f.filename, True)

    # Ensure directory exists
    try:
        os.makedirs(userDir, exist_ok=True)
        log_debug(f"Directory ready: {userDir}")
    except Exception as e:
        log_debug(f"❌ Failed to create directory: {e}")
        return finalizeResponse({"authenticated": False, "status": "error", "message": "Cannot create directory"})

    # Save file
    try:
        f.save(uploadLocation)
        log_debug(f"✅ File saved to: {uploadLocation}")
    except Exception as e:
        log_debug(f"❌ Failed to save file: {e}")
        return finalizeResponse({"authenticated": False, "status": "error", "message": "Cannot save file"})

    # Add to DB
    try:
        addDbUserLog(secureFilename, username)
        log_debug(f"✅ Added to DB: {secureFilename}")
    except Exception as e:
        log_debug(f"❌ Failed to add DB entry: {e}")
        return finalizeResponse({"authenticated": False, "status": "error", "message": "DB error"})

    # Final response
    response = {"authenticated": True, "status": "ok", "message": "File uploaded."}
    log_debug(f"🎉 Finished successfully for {username}")
    return finalizeResponse(response)
