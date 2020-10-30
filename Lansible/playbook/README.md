ansible-playbook -i hosts role/init_os.yaml --limit test
ansible-playbook -i hosts role/init_os.yaml --limit k8s 
