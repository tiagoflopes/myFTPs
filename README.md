# myFTPs
A (hopefully) secure implementation of the File Transfer Protocol in python from scratch.

## Usage

### Create a SSL certificate and key
```bash
openssl req -new -x509 -days 365 -nodes -newkey rsa:2048 -out ftp_crt.pem -keyout ftp_key.pem
```