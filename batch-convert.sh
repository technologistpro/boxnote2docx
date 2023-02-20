USER=$1

mkdir converted/boxnotes-${USER}

find ../boxsdk/boxnotes/${USER} -type f -name '*.boxnote' -print0 |                                        
while IFS= read -r -d '' file; do
    ./boxnote2docx -b "$file" -d converted/boxnotes-${USER} 2>&1
done | tee ${USER}.log

cp ../boxsdk/boxnotes/${USER}/inventory.csv converted/boxnotes-${USER}/