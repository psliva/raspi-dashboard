# Force a screen refresh every 5 mins (display won't update in some cases)
for (( ; ; ))
do
    xrefresh
    sleep 300
done
