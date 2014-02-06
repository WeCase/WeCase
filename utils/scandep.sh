for file in $(ls | grep py | egrep -v "rc|pyc|ui"); do
    echo $file
    cat $file | egrep "^import|^from"
    printf "\n"
done
