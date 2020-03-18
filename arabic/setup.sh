CURR_PATH=`cd $(dirname $0);pwd;`
cd $CURR_PATH

url="https://bakrianoo.sfo2.digitaloceanspaces.com/aravec/full_grams_cbow_100_wiki.zip"
f="models/full_grams_cbow_100_wiki.zip"
if [ ! -f $f ];
then
    mkdir models
    wget $url -O $f
    cd models
    unzip full_grams_cbow_100_wiki.zip
fi
