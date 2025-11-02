import sqlite3

def get_person_and_pets(person_id):
    conn = sqlite3.connect('pets.db')
    cursor = conn.cursor()

    cursor.execute("SELECT first_name, last_name, age FROM person WHERE id = ?;", (person_id,))
    person = cursor.fetchone()

    if not person:
        print("Person not found.")
        conn.close()
        return

    print(f"{person[0]} {person[1]}, {person[2]} years old")

    cursor.execute("""
        SELECT pet.name, pet.breed, pet.age, pet.dead
        FROM pet
        JOIN person_pet ON pet.id = person_pet.pet_id
        WHERE person_pet.person_id = ?;
    """, (person_id,))
    pets = cursor.fetchall()

    for pet in pets:
        status = "that was" if pet[3] == 1 else "that is"
        print(f"{person[0]} owned {pet[0]}, a {pet[1]}, {status} {pet[2]} years old")

    conn.close()

while True:
    user_input = input("Enter person ID (or 0 to exit): ")
    if user_input.strip() == "0":
        break
    if user_input.isdigit():
        get_person_and_pets(int(user_input))
    else:
        print("Please enter a valid numeric ID.")
