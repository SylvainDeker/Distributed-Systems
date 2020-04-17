exit 0
# 1st time:
docker build -t distributed-systems-ubuntu .

#step 1
docker run -t -d -v `pwd`:/root/Distributed-Systems distributed-systems-ubuntu
# step 2
docker exec -ti 5e2a08f0c3683375088fb3476d9afb940c813788027ce040943e71cb6103be3d bash
