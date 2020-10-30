ansible-playbook -i hosts role/init_os.yaml --limit test
ansible-playbook -i hosts role/init_os.yaml --limit k8s 

ansible k8s -i hosts -m shell -a 'cat /etc/resolve.conf'
