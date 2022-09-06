# How to encrypt files

## Ecrypting a file

First encrypt the file (file.name)

```
gpg --cipher-algo AES256 -c  file.name
```

Forget the password on gpg

```
gpgconf --reload gpg-agent
```

## Decrypting a file

Decrypts a file named `file.name.gpg` (good idea to forget the password later)

```
gpg file.name.gpg
```

