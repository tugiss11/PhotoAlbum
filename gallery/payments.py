import hashlib

SELLER_ID = "MemoryAlbum"
SECRET_KEY = "8911102d793a79b9930bed5a3feba201"

def generate_payment_checksum(payment_id, amount):
    checksum_string = "pid=%s&sid=%s&amount=%s&token=%s"%(payment_id, SELLER_ID, amount, SECRET_KEY)
    return hashlib.md5(checksum_string).hexdigest()

def generate_payment_succesfull_checksum(payment_id, ref):
    checksum_string = "pid=%s&ref=%s&token=%s"%(payment_id, ref, SECRET_KEY)
    return hashlib.md5(checksum_string).hexdigest()