import pycurl
from io import BytesIO

file_path = "./file.txt"
upload_url = 'http://127.0.0.1:8000/api/upload/'
token = '93cd37dceaff82b3c7dc12681d46a8e545962bd0'

# Read file contents
with open(file_path, 'rb') as file:
    file_contents = file.read()
    print(file_contents)

c = pycurl.Curl()
c.setopt(c.URL, upload_url)
c.setopt(c.HTTPHEADER, ['Authorization: Token ' + token])
c.setopt(c.POST, 1)
c.setopt(c.HTTPPOST, [('file', (c.FORM_BUFFER, file_path, c.FORM_BUFFERPTR, file_contents))])

# Buffer to store response
response_buffer = BytesIO()
c.setopt(c.WRITEDATA, response_buffer)

try:
    # Perform the request
    c.perform()

    # Check response
    response_code = c.getinfo(c.RESPONSE_CODE)
    response_data = response_buffer.getvalue().decode('utf-8')

    if response_code == 201:  
        print("File uploaded successfully.")
        print(response_data)  # Print response content if needed
    else:
        print("Failed to upload file:", response_data)

except pycurl.error as e:
    # Catch any pycurl errors
    print("PyCurl error:", e)

except Exception as e:
    # Catch any other exceptions
    print("An error occurred:", e)

finally:
    c.close()  # Close curl connection
