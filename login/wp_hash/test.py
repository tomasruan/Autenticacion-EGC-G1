from passlib.hash import phpass
import wp_hash

# FORMA 1
# USANDO passlib
# https://passlib.readthedocs.io/en/stable/narr/hash-tutorial.html#password-hash-examples
hash = phpass.hash("hola")
print(hash)
print(phpass.verify("hola", hash))


# FORMA 2
# USANDO wp_hash
# https://gist.github.com/romke/61dd1313c6ab112186ac
#hash = wp_hash.crypt_private("hola")
#print(hash)