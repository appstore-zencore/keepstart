cd ..
pip uninstall keepserver -y
pip install .
cd test
keepserver -c config.logFile.yaml start
