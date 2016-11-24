# Docker for flansible

### Description

[Flansible](https://github.com/trondhindenes/flansible) is a restful service which can invoke [ansible](https://github.com/ansible/ansible) command in [celery](https://github.com/celery/celery), and this is the docker container for it.

### Configuration

You need set up an flansible folder which contains two subfolders

- ansible: which contains hosts, ansible.cfg and your playbook file
- ssh: which contains your private ssh key which need for ansible to run

You can see an example in the **vol_example** folder here

### Run

You can just use `docker-compose up -d` here, or use the command below:

1. start reids 

    ```bash
    docker run -d --name=redis -v YOUR_REDIS_FOLDER:/data redis:alpine redis-server --appendonly yes
    ```

2. start celery
    
    ```bash
    docker run -d --name=celery -v YOUR_ANSIBLE_FOLDER:/data playniuniu/flansible /env/bin/celery worker -A flansible.celery --loglevel=info
    ```

3. start flansible

    ```bash
     docker run -d --name=flansible -p 8000:8000 -v YOUR_ANSIBLE_FOLDER:/data playniuniu/flansible
    ```

4. start flower (optional)

    ```bash
    docker run -d --network=picc --name=flower -p 5555:5555 playniuniu/flower
    ```

### Useage

Please refer flansible usage [here](https://github.com/trondhindenes/flansible)
