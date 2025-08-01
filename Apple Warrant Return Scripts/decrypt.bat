for %%f in (*.gpg) do (
    gpg --batch --yes --passphrase [insert_passphrase_here] --output "%%~nf" --decrypt "%%f"
)