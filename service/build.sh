docker build -t csvinsertion .
docker tag csvinsertion ncar-im-0.rc.unr.edu/csvinsertion 
docker push ncar-im-0.rc.unr.edu/csvinsertion:latest