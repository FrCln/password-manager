import yadisk

with open('yadisk-secret.txt') as f:
    application_id = f.readline().strip()
    application_secret = f.readline().strip()
    yadisk_token = f.readline().strip()

y = yadisk.YaDisk(token=yadisk_token)
# or
# y = yadisk.YaDisk("<application-id>", "<application-secret>", "<token>")

# Check if the token is valid
print(y.check_token())

# Get disk information
# print(y.get_disk_info())

# Print files and directories at "/some/path"
# print(list(y.listdir("/")))

# Upload "file_to_upload.txt" to "/destination.txt"
# y.upload("requirements.txt", "/destination.txt")

# Same thing
# with open("file_to_upload.txt", "rb") as f:
#     y.upload(f, "/destination.txt")

# Download "/some-file-to-download.txt" to "downloaded.txt"
# y.download("/Лекции по апологетике.docx", "downloaded.docx")

# Permanently remove "/file-to-remove"
# y.remove("/file-to-remove", permanently=True)

# Create a new directory at "/test-dir"
print(y.mkdir("/test-dir"))
