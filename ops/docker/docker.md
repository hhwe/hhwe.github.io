1. docker中国镜像源
https://registry.docker-cn.com

2. 在get-started中不能使用kubernetes和swarm混合使用默认将使用kubernetes, 当执行docker stack 会出现问题

3. 在docker-mashine中使用docker swarm会出现问题

https://forums.docker.com/t/docker-swarm-join-with-virtualbox-connection-error-13-bad-certificate/31392
Port 2376 is the docker daemon port, not the swarmkit port. Use 2377 as the port if you want to explicitly specify it, or omit it entirely in your --advertise-addr command.

For example:

docker-machine ssh myvm1 "docker swarm leave --force"
docker-machine ssh myvm1 "docker swarm init --advertise-addr 192.168.99.101"
docker-machine ssh myvm2 "docker swarm join --token SWMTKN-1-65xbfd388nl61m4ip6qoplk0yqoze3qzq9ne9t00lmxbppt6oe-7f40hx9wn4tyu3b0nznsrqs2e 192.168.99.101"
