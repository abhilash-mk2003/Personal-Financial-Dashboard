
class UserAuthentication:
    def __init__(self):
        self.valid_email = "charan@fin404.com"
        self.valid_password = "charan"

    def authenticate_user(self, email, password):
        if email == self.valid_email and password == self.valid_password:
            return True
        else:
            return False

def main():
    authentication_manager = UserAuthentication()

    while True:
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        if authentication_manager.authenticate_user(email, password):
            print("Login successful!")
            break
        else:
            print("Invalid email or password. Please try again.")

if __name__ == "__main__":
    main()