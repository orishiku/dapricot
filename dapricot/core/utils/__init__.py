import os

class SecretsCollectionObject:
    def __init__(self, name, base_path):
        self.__path = os.path.join(base_path, name)
        self.__load_secrets()

    def __load_secrets(self):
        self.__secrets = {}
        
        with open(self.__path, 'r') as file:
            lines = file.readlines()

            for line in lines:
                secret = line.split(':::')
                if len(secret)==2:
                    self.add_or_change_secret_value(secret[0], secret[1])

        return len(self.__secrets)

    def get_secrets(self):
        return self.__secrets
    
    def get_secret_value(self, key_name):
        return self.__secrets.get(key_name, None)

    def add_or_change_secret_value(self, key_name, value):
        self.__secrets[key_name.strip()] = value.strip()
        return self.__secrets[key_name.strip()]
    
    def delete_secret(self, key_name):
        self.__secrets[key_name.strip()]

    def save_secrets(self):        
        try:
            lines = []
            for key_name, key_value in self.__secrets.items():
                lines.append("%s ::: %s\n" % (key_name, key_value)) 

            with open(self.__path, 'w') as file:
                file.truncate(0)                 
                file.writelines(lines)

            return True

        except Exception:
            return False