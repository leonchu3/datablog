def get_md5(v):
    import hashlib
    # Message Digest Algorithm MD5（中文名为消息摘要算法第五版）为计算机安全领域广泛使用的一种散列函数，用以提供消息的完整性保护
    md5 = hashlib.md5()  # md5对象，md5不能反解，但是加密是固定的，就是关系是一一对应，所以有缺陷，可以被对撞出来

    ## update需要一个bytes格式参数
    md5.update(v.encode('utf-8'))  # 要对哪个字符串进行加密，就放这里
    value = md5.hexdigest().upper()  # 拿到加密字符串

    return value

#
# p_m = hashlib.md5()
# p_m.update(password_1.encode())  # 字符转成字节
# # p_m.hexdigest() 16进制存储
# UserProfile.objects.create(username=username, nickname=username, password=p_m.hexdigest(), email=email, phone=phone)

print(get_md5('chuchu'))