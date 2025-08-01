# Apple Warrant Return Scripts

**download.bat** - Used to download all *.gpg* files from an Apple Warrant Return.

1. Place download.bat in an empty folder.
2. Add a links.txt file which conaints a list of all the download urls (which can be found in the \<id\>-account-download-details.csv.
3. Double click the download.bat file.
4. Files will begin to download into the folder.

**decrypt.bat**- Used to decrypt all *.gpg* files from an Apple Warrant Return.

1. Place decrypt.bat in folder containing the encrypted *.gpg* files.
2. Edit decrypt.bat by changing the passcode for the encrypted files.
3. Double click the decrypt.bat file.
4. This will create decrypted *.zip* files in the same directory.
5. Once complete, seperate the encrypted/decrypted files into their own folders.
6. When processing the data, use Cellebrite Inseyets PA's Apple Warrant Return type, and select the folder containing JUST the .zip file.