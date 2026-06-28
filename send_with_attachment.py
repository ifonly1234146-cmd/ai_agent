import base64, json, subprocess, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

msg = MIMEMultipart()
msg['To'] = 'ifonly123@nate.com'
msg['From'] = 'ifonly1234146@gmail.com'
msg['Subject'] = 'Gmail 메일 작성창 화면 캡처'

msg.attach(MIMEText('안녕하세요,\n\nGmail 메일 작성창 화면 캡처 파일을 첨부드립니다.\n\n감사합니다.', 'plain', 'utf-8'))

with open(r'C:\Users\SBS\Desktop\agent02\gmail_compose.png', 'rb') as f:
    part = MIMEBase('image', 'png')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename='gmail_compose.png')
    msg.attach(part)

raw = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
payload = json.dumps({'raw': raw})

# Write payload to temp file to avoid shell escaping issues
payload_file = r'C:\Users\SBS\Desktop\agent02\mail_payload.json'
with open(payload_file, 'w') as f:
    f.write(payload)

# Use PowerShell to call gws
ps_cmd = f'gws gmail users messages send --params \'{{\"userId\":\"me\"}}\' --json (Get-Content -Raw "{payload_file}")'
result = subprocess.run(
    ['powershell', '-Command', ps_cmd],
    capture_output=True, text=True, encoding='utf-8'
)
print(result.stdout)
if result.stderr:
    print('STDERR:', result.stderr)
