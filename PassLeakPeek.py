import hashlib
import requests

# === Startpunkt ===
print("==============================================================================")
print("Welcome to PassLeak Peek!")
print("This script will look through known leaked passwords and check if it can find\nyour password in any of the leaked lists.")
print("==============================================================================")
# Användaren skriver in ett lösenord
Userpassword = input(str("Write the password you wanna check and press enter: "))


# Function for translating password to SHA-1 hash
def hash_password(Userpassword):
    return hashlib.sha1(Userpassword.encode('utf-8')).hexdigest().upper() 

# Ta bort print när allt är klart
print("Hashed password:", hash_password(Userpassword))  

# Function checks password hash against the Have I Been Pwned API
def check_hash_with_api(Userpassword):
    sha1_hash = hash_password(Userpassword)
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    r = requests.get(url)
    if r.status_code != 200:
        print("API-fel:", r.status_code); return None
    for line in r.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            print(f"Lösenordet är läckt ({count} gånger).")
            return True
    print("Inte hittat i databasen."); return False

check_hash_with_api(Userpassword)

    # 2. Bygg URL för API-anropet
    #    → Exempel: "https://api.pwnedpasswords.com/range/<hash-prefix>"
    #    → API:t använder bara de första 5 tecknen av hash för att skydda integritet
    
    # 3. Skicka HTTP-förfrågan till API:t
    #    → Använd ett bibliotek som 'requests' för att göra GET-anrop
    
    # 4. Ta emot svaret från API:t
    #    → Svaret innehåller en lista med hash-suffix och antal förekomster
    
    # 5. Jämför om ditt lösenords hash finns i svaret
    #    → Om JA → lösenordet är läckt
    #    → Om NEJ → lösenordet är inte hittat
    
    # 6. Returnera resultatet (True/False eller ett meddelande)

# Funktion: Jämför lösenordet med en databas över kända läckta lösenord
# Om lösenordet finns i listan:
    # → Skriv ut varning om att lösenordet är läckt
    # → Erbjud användaren att generera ett nytt starkt lösenord
        # Om användaren accepterar:
            # → Generera nytt lösenord som inte finns i listorna
            # → Avsluta
        # Om användaren nekar:
            # → Avsluta

# Om lösenordet inte finns i listan:
    # === Steg 2: Kontrollera likhet med läckta lösenord ===
    # Funktion: Analysera om 70% eller mer av lösenordet matchar någon lista
    # Om JA:
        # → Skriv ut att lösenordet liknar läckta lösenord
        # → Rekommendera att göra lösenordet starkare
        # → Avsluta
    # Om NEJ:
        # === Steg 3: Kontrollera komplexitet ===
        # Funktion: Kontrollera om lösenordet har specialtecken, versaler och är längre än 12 tecken
        # Om JA:
            # → Skriv ut att lösenordet inte är läckt och verkar starkt
            # → Rekommendera att kontrollera lösenordet regelbundet
            # → Avsluta
        # Om NEJ:
            # → Skriv ut att lösenordet inte är läckt men saknar viktiga säkerhetskomponenter
            # → Rekommendera att förbättra lösenordet
            # → Avsluta