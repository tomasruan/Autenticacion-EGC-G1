from passlib.hash import phpass
from wp_hash.hash import crypt_private

# OPCION 1
# USANDO passlib
# https://passlib.readthedocs.io/en/stable/narr/hash-tutorial.html#password-hash-examples
print("OPCION 1")

hash = phpass.hash("hola")
print(hash)
print(phpass.verify("hola", hash))


# OPCION 2
# USANDO clase hash
# https://gist.github.com/romke/61dd1313c6ab112186ac
#print("\n")
#print("OPCION 2")

#hash = crypt_private("hola")
#print(hash)