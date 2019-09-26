#!/bin/sh

# Decrypt the file
mkdir $HOME/.aws
# --batch to prevent interactive command --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt --passphrase="$KEY" \
--output $HOME/.aws/credentials credentials.gpg