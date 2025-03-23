class UserNotFoundError(Exception):
    pass

class WrongPasswordError(Exception):
    pass

class UserAuth:
    def __init__(self,slownik):
        self.slownik = slownik
    
    def login(self, username, password):
        if username in self.slownik:
            if self.slownik[username] == password:
                return True
            else:
                raise WrongPasswordError("Niepoprawne hasło")
        else:
            raise UserNotFoundError("Niepoprawny login")

userAuth = UserAuth({"admin":"1234","user":"abcd"})

for username, password in [("admin", "1234"), ("user", "wrongpass"), ("Unknown", "pass")]:
    try:
        userAuth.login(username, password)
    except (UserNotFoundError, WrongPasswordError) as e:
        print(f"Błąd: {e}")