This project was created to convert Box Notes to Microsoft Word Documents.
It can handle both the 'old' and 'new' Box Note formats.

```sh
boxnote2docx -b path/to/boxnote -d directory-to-place-converted-docx
```

Example of a batch run:

```sh
find /path-to/boxnotes -type f -name '*.boxnote' -print0 |
while IFS= read -r -d '' file; do
    ./boxnote2docx -b "$file" -d /path-to/converted-dir/ 2>&1
done | tee boxnote2docx.log
```
