#安装环境
ansible-playbook -i hosts role/init_os.yaml --limit test
ansible-playbook -i hosts role/init_os.yaml --limit k8s 

ansible k8s -i hosts -m shell -a 'cat /etc/resolve.conf'

#安装docker
ansible-playbook -i hosts role/docker.yaml --limit test

ansible-playbook -i hosts role/docker.yaml --limit k8s
