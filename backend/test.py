import secrets

# 生成32字节(256bit)的安全随机密钥，返回base64字符串，适合HS256
jwt_secret_key = secrets.token_urlsafe(32)
print(jwt_secret_key)