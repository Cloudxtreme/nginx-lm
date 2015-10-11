dir=$(mktemp -d) && \
cd $dir && \
wget -qO- -O tmp.zip https://github.com/awalGarg/nginx-lm/archive/master.zip && \
unzip tmp.zip && \
cd nginx-lm-master && \
python3 setup.py install && \
cd ../.. && \
rm -rf $dir && \
echo "Completed..."
